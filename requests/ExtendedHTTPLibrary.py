import requests
from requests_pkcs12 import Pkcs12Adapter
from RPA.HTTP import HTTP


class ExtendedHTTPLibrary(HTTP):
    """This library extends RPA.HTTP functionality with a
    keyword which will create request session supporting
    PKCS#12.

    All keywords provided by RPA.HTTP and RequestLibrary
    are included.

    https://robocorp.com/docs/libraries/rpa-framework/rpa-http
    """

    def __init__(self, *args, **kwargs):
        HTTP.__init__(self, *args, **kwargs)

    def create_pkcs12_session(
        self, alias: str, url: str, cert_path: str, passphrase: str
    ):
        """Creates a PKCS#12 session using Pkcs12Adapter.

        :param alias: alias to identify the session
        :param url: base url for the server
        :param cert_path: absolute filepath to the .p12 file
        :param passphrase: a byte string or unicode string that contains the password
        :return: session

        """
        session = requests.Session()
        session.mount(
            "https://",
            Pkcs12Adapter(
                pkcs12_filename=cert_path,
                pkcs12_password=passphrase,
            ),
        )
        session.url = url
        self._cache.register(session, alias=alias)
        return session
