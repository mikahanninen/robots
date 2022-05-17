from msedge.selenium_tools import EdgeOptions
from RPA.Browser.Selenium import Selenium
from SeleniumLibrary.base import keyword
from typing import Optional

class EdgeLibrary(Selenium):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)    

    @keyword
    def get_edge_options(self, **kwargs):
        remote_port = kwargs.pop("remote_port", None)
        edge_options = EdgeOptions()
        edge_options.use_chromium = True
        edge_options.headless = bool(kwargs.pop("headless", True))
        if remote_port:
            edge_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{remote_port}")
        return edge_options

    @keyword
    def attach_edge_browser(self, port: int, alias: Optional[str] = None):
        """Attach to an existing instance of Edge.

        Requires that the browser was started with the command line
        option ``--remote-debugging-port=<port>``, where port is any
        4-digit number not being used by other applications.

        That port can then be used to connect using this keyword.

        Example:

        | Attach Edge Browser | port=9222 |
        """
        options = self.get_edge_options(remote_port=port)
        capabilities = options.to_capabilities()
        self.open_browser(browser="edge", alias=alias, desired_capabilities=capabilities)
   