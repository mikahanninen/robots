import logging
from robot.api.deco import keyword
from typing import Optional, Dict, Any

from RPA.Robocorp.Process import Process


class ExtendedProcess(Process):

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)

    @keyword(tags=["process", "get", "runs"])
    def list_run_artifacts(
        self,
        process_run_id: str,
        step_run_id: Optional[str] = None,
        process_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """List Robot run artifacts

        :param process_run_id: id of the process run
        :param step_run_id: id of the process step run
        :param process_id: specific process to which runs belongs to
        :return: the response JSON
        """
        request_url = f"{self.process_api(process_id)}/runs/{process_run_id}"
        if step_run_id:
            request_url = f"{request_url}/robotRuns/{step_run_id}/artifacts"
        self.logger.info("GET %s", request_url)            
        response = self.http.session_less_get(
            url=request_url,
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()        

    @keyword(tags=["process", "get", "runs"])
    def get_robot_run_artifact(
        self,
        process_run_id: str,
        step_run_id: str,
        artifact_id: str,
        filename: str,        
        process_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get a download URL for a process run artifact

        :param process_run_id: id of the process run
        :param step_run_id: id of the process step run
        :param artifact_id: id of the run artifact
        :param filename: filename of the run artifact
        :param process_id: specific process to which runs belongs to
        :return: url for file download
        """
        request_url = f"{self.process_api(process_id)}/runs/{process_run_id}"
        request_url = f"{request_url}/robotRuns/{step_run_id}/artifacts/{artifact_id}/{filename}"
        self.logger.info("GET %s", request_url)
        response = self.http.session_less_get(
            url=request_url,
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()        
