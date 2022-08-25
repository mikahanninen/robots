import os
from ExtendedProcess import ExtendedProcess
from RPA.Robocorp.Vault import Vault
from RPA.HTTP import HTTP

PROCESS = ExtendedProcess()

def main():
    secrets = Vault().get_secret("control_room_process")
    PROCESS.set_credentials(
        workspace_id=secrets["workspace_id"], 
        process_id=secrets["process_id"],
        apikey=secrets["api_key"])
    work_items = PROCESS.list_process_work_items()
    for item in work_items:
        artifacts = PROCESS.list_run_artifacts(
            process_run_id=item["processRunId"],
            step_run_id=item["activityRunId"]            
        )
        for artifact in artifacts:
            if ".xlsx" in artifact["fileName"]:
                download_link = PROCESS.get_robot_run_artifact(
                    process_run_id=item["processRunId"],
                    step_run_id=item["activityRunId"],
                    artifact_id=artifact["id"],
                    filename=artifact["fileName"]
                )
                target_filepath = os.path.join(
                    os.getenv("ROBOT_ARTIFACTS"), 
                    f"xx_run_{item['processRunNo']}_{artifact['fileName']}"
                )
                HTTP().download(
                    url=download_link,
                    target_file=target_filepath,
                    overwrite=True,
                    stream=True
                )

if __name__ == "__main__":
    main()