import logging
from typing import Dict

import httpx

from pyostrap.exceptions import BiostrapApiException


class HttpxClient:
    def __init__(
        self,
        api_key: str,
        hostname: str,
        ver: str,
        ssl_verify: bool = True,
        logger: logging.Logger = None,
    ):
        """
        :param api_key: string used for authentication
        :param hostname: Normally, api-beta.biostrap.com
        :param ver: always v1
        :param ssl_verify: Normally set to True, but if having SSL/TLS cert validation issues,
        can turn off with False
        :param logger: (optional) If your app has a logger, pass it in here
        """
        self.base_url = f"https://{hostname}/{ver}/"
        self._api_key = api_key
        self._ssl_verify = ssl_verify
        self._logger = logger or logging.getLogger(__name__)
        self._headers = {"Authorization": f"APIKey {self._api_key}"}

        self.client = httpx.Client(
            http2=True,
            verify=self._ssl_verify,
            headers=self._headers,
            base_url=self.base_url,
        )

    def _do(
        self,
        http_method: str,
        endpoint: str,
        ep_params: Dict = None,
    ) -> str:
        """
        :param http_method: "GET" or "POST"
        :param endpoint: the path of the url after the base url
        :param ep_params: key value pairs of params
        :return: data in json format string
        """
        log_line_pre = (
            f"method={http_method}, url={self.base_url}{endpoint}, params={ep_params}"
        )

        # Log HTTP params and perform an HTTP request, catching and re-raising any exceptions
        try:
            self._logger.debug(msg=log_line_pre)
            request = self.client.build_request(
                method=http_method,
                url=endpoint,
                params=ep_params,
            )
            response = self.client.send(request)
            log_line = (
                f"{log_line_pre}, success={response.is_success}, "
                f"status_code={response.status_code}"
            )
        except httpx.HTTPError as e:
            log_error = (
                f"{log_line}; message={response.reason_phrase};"
                f" {response.json()["errors"][0]["title"]} "
            )

            self._logger.error(msg=f"{log_error}")
            raise BiostrapApiException(f"Request failed; {log_error}") from e

        log_line = (
            f"{log_line_pre}, success={response.is_success}, "
            f"status_code={response.status_code}"
        )

        if response.is_success:
            self._logger.debug(msg=log_line)
            return response.text

    def get(self, endpoint: str, ep_params: Dict = None) -> str:
        return self._do(http_method="GET", endpoint=endpoint, ep_params=ep_params)

    def post(self, endpoint: str, ep_params: Dict = None, data: Dict = None) -> str:
        return self._do(http_method="POST", endpoint=endpoint, ep_params=ep_params)
