import datetime
import pathlib
import site
from pprint import pprint
import time

# site.addsitedir("../src")

from pingintel_api.utils import set_verbosity
from pingintel_api.pingvision import types as t
from pingintel_api import PingVisionAPIClient


# These are subject to change based on how we configure your workflow
# TEAM_UUID = 11
# DIVISION_SHORT_NAME = "WKFC"
# TEAM_SHORT_NAME = "WKFC"
# WORKFLOW_STATUS_PLEASE_SCRUB = 3
# WORKFLOW_STATUS_DECLINE = 7

set_verbosity(2)
# api_client = PingVisionAPIClient(environment="dev")
api_client = PingVisionAPIClient(environment="local", api_url="http://localhost:8002")


def find_my_ids():
    ret = api_client.list_teams()
    pprint(ret)
    TEAM_UUID = ret[0]["team_uuid"]
    DIVISION_UUID = ret[0]["division_uuid"]

    statuses = api_client.list_submission_statuses(division=DIVISION_UUID)
    pprint(statuses)

    WORKFLOW_STATUS_PLEASE_SCRUB = next(_["uuid"] for _ in statuses if _["name"] == "Waiting for scrubbing")
    WORKFLOW_STATUS_DECLINE = next(_["uuid"] for _ in statuses if _["name"] == "Cancelled")
    return {
        "team_uuid": TEAM_UUID,
        "division_uuid": DIVISION_UUID,
        "workflow_status_please_scrub": WORKFLOW_STATUS_PLEASE_SCRUB,
        "workflow_status_decline": WORKFLOW_STATUS_DECLINE,
    }


def generate_some_test_data(settings):
    current_time = datetime.datetime.now()
    SCRIPT_DIR = pathlib.Path(__file__).parent
    ret = api_client.create_submission(
        filepaths=[SCRIPT_DIR / "test_sov.xlsx"],
        delegate_to_team=settings["team_uuid"],
    )
    pingid = ret["id"]
    url = ret["url"]

    print(f"pingid: {ret['id']}")


global _cursor_id
_cursor_id = None


def get_persisted_cursor() -> str | None:
    # This function retrieves the cursor ID from a file or database...
    return _cursor_id


def persist_cursor_forever(cursor_id: str):
    # This function would save the cursor ID to a file or database...
    global _cursor_id
    cursor_id = cursor_id


def start_listening(as_of_time: datetime.datetime | None, settings):
    # This function is called when the script starts running
    # It sets the start time for the event listening loop
    cursor_id = get_persisted_cursor()
    start = as_of_time

    while True:
        ret = api_client.get_submission_events(
            page_size=10, team=settings["team_uuid"], cursor_id=cursor_id, start=start
        )
        cursor_id = ret["cursor_id"]

        for event in ret["results"]:
            event_type = event["event_type"]
            new_value = event["new_value"]
            print(f"Event: {event_type}")

            if (
                event_type == t.SUBMISSION_EVENT_LOG_TYPE.SUBMISSION_STATUS_CHANGE
                and new_value == settings["workflow_status_please_scrub"]
            ):
                perform_declination_logic(event["pingid"], settings)

        time.sleep(1.0)

        persist_cursor_forever(cursor_id)


def perform_declination_logic(pingid: str, settings):
    ## TODO: maybe replace 'activity querying' with accessor for downloading 'current building data' filtered by fields, etc?
    submission_detail = api_client.list_submission_activity(pingid=pingid)
    submission_ret = submission_detail["results"][0]

    for document in submission_ret["documents"]:
        if document["document_type"] == "SOVFIXER_JSON":
            filename = document["filename"]
            document_url = document["url"]
            break
    else:
        raise ValueError("No JSON document found")

    output_filename = "downloaded-" + filename
    api_client.download_document(output_filename, document_url=document_url)

    print(f"Downloaded file to {output_filename}")

    # Process "output_filename" and make some decisions...

    print("Valid actions:")
    pprint.pprint(submission_ret["actions"]["transition_to"])

    api_client.add_data_items(
        pingid,
        t.DATA_ITEM_ACTIONS.UPSERT,
        {"uw_declination_reason": "test reason", "broker_declination_reason": "test reason", "should_run_cytora": True},
    )

    api_client.change_status(pingid=pingid, workflow_status_id=settings["workflow_status_decline"])


settings = find_my_ids()

# start separate thread to occasionally send submissions in.
import threading


def generate_test_data_every_few_seconds():
    while True:
        generate_some_test_data(settings)
        time.sleep(5)


threading.Thread(target=generate_test_data_every_few_seconds).start()
start_listening(None, settings)
