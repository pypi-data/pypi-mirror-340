import dataclasses
import datetime
import logging
import re
import time
from typing import Any, Optional, cast

import requests

logger = logging.getLogger(__name__)


class AzureApiCall:
    def __init__(self, azure_requests, method, url):
        self.azure_requests = azure_requests
        self.method = method
        self.url = url

    def request(self, *args, **kwargs):
        return self.azure_requests.request(self.method, self.url, *args, **kwargs)


class AzureRequests:
    def __init__(
        self,
        pat: str,
        organization: str,
        project: Optional[str] = None,
        team: Optional[str] = None,
    ):
        self.auth = (pat, pat)
        self.organization = organization
        self.project = project
        self.team = team
        self.rate_info: Optional[RateLimit] = None

    def call(self, azure_url, params=None, data=None, result_key=None):
        api_call = self.api(azure_url, **(params or {}))
        if data is None:
            response = api_call.request()
        else:
            response = api_call.request(json=data)
        if result_key is None:
            return response
        else:
            return response[result_key]

    def api(self, azure_url, **url_params):
        params = dict(
            organization=self.organization,
            project=self.project or "",
            team=self.team or "",
        )
        params.update(url_params)
        method, _, raw_url = azure_url.partition(" ")
        url = raw_url.format(**params)
        return AzureApiCall(self, method, url)

    def get(self, url: str, *args, **kwargs) -> Any:
        return self.request("get", url, *args, **kwargs)

    def post(self, url: str, *args, **kwargs) -> Any:
        return self.request("post", url, *args, **kwargs)

    def put(self, url: str, *args, **kwargs) -> Any:
        return self.request("put", url, *args, **kwargs)

    def patch(self, url: str, *args, **kwargs) -> Any:
        return self.request("patch", url, *args, **kwargs)

    def delete(self, url: str, *args, **kwargs) -> Any:
        return self.request("delete", url, *args, **kwargs)

    def request(self, method: str, url: str, *args, **kwargs) -> Any:
        kwargs.setdefault("headers", {})
        if "json" in kwargs:
            if isinstance(kwargs["json"], list):
                kwargs["headers"]["Content-type"] = "application/json-patch+json"
            else:
                kwargs["headers"]["Content-type"] = "application/json"

        url_params = {
            "organization": self.organization,
            "project": self.project,
            "team": self.team,
        }
        url_params.update(kwargs.pop("url_params", {}))
        for key, value in url_params.items():
            to_replace = str(value or "")
            url = url.replace("{" + key + "}", to_replace)

        kwargs["auth"] = self.auth

        if self.rate_info:
            if self.rate_info.remaining:
                waiting = max(0, 30 - self.rate_info.remaining)
            else:
                waiting = self.rate_info.retry_after
            if waiting:
                log_level = logging.WARNING
            else:
                log_level = logging.DEBUG
            logger.log(
                log_level,
                "Rate limit info: "
                + f"remaining={self.rate_info.remaining} "
                + f"delay={self.rate_info.delay:.2f} "
                + f"retry={self.rate_info.retry_after} "
                + f"limit={self.rate_info.limit} "
                + f"reset={self.rate_info.to_sleep.total_seconds()/60:.1f}min "
                + f"resource={self.rate_info.resource}. "
                + f"Waiting {waiting} sec.",
            )
            if waiting:
                time.sleep(waiting)
        try:
            response = requests.request(method, url, *args, **kwargs)
        except requests.exceptions.ProxyError as ex:
            logger.warning(f"Proxy error ({ex}). Retrying later...")
            time.sleep(15)
            return self.request(method, url, *args, **kwargs)
        if not response.ok:
            additional_info = ""
            if response.status_code // 100 == 5:
                logger.warning(
                    f"Azure DevOps server error ({response.status_code}). Retrying later..."
                )
                time.sleep(15)
                return self.request(method, url, *args, **kwargs)
            elif response.status_code // 100 == 4:
                logger.debug("Azure DevOps API error: " + response.text)
                if response.headers.get("Content-Type") == "text/html":
                    if match := re.search(r"<title[^>]*>(.*?)</title>", response.text):
                        additional_info = match.group(1)
            else:
                logger.error("Azure DevOps API error: " + response.text)
            msg = f"{response.status_code}: {response.reason}"
            if additional_info:
                msg = f"{msg} // {additional_info}"
            raise requests.HTTPError(msg, response=response)
        if "X-RateLimit-Remaining" in response.headers:
            self.rate_info = RateLimit(
                resource=cast(str, response.headers.get("X-RateLimit-Resource")),
                delay=float(response.headers.get("X-RateLimit-Delay", "0")),
                remaining=int(cast(str, response.headers.get("X-RateLimit-Remaining"))),
                limit=int(cast(str, response.headers.get("X-RateLimit-Limit"))),
                reset=datetime.datetime.fromtimestamp(
                    int(cast(str, response.headers.get("X-RateLimit-Reset")))
                ),
                retry_after=int(response.headers.get("Retry-After", "0")),
            )
        else:
            self.rate_info = None
        if "application/json" in response.headers.get("content-type"):
            return response.json()
        else:
            return response


@dataclasses.dataclass
class RateLimit:
    resource: str
    remaining: int
    delay: float
    retry_after: int
    limit: int
    reset: datetime.datetime

    @property
    def to_sleep(self) -> datetime.timedelta:
        return self.reset - datetime.datetime.now()
