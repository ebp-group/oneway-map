# -*- coding: utf-8 -*-
import logging
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

log = logging.getLogger(__name__)


def _download_request(url, params={}, extra_headers={}, verify=True):
    retry_strategy = Retry(
        total=5,
        backoff_factor=2,
        status_forcelist=[403, 429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)
    headers = {
        "user-agent": "Mozilla Firefox Mozilla/5.0; metaodi jupyter-playground",
        "accept-language": "de-CH",
    }
    headers.update(extra_headers)
    r = http.get(url, params=params, headers=headers, timeout=20, verify=verify)
    log.debug(f"HTTP Request URL: {r.request.url}")
    log.debug(f"HTTP response: {r.status_code}")
    r.raise_for_status()
    return r


def download(url, params={}, encoding="utf-8", verify=True):
    r = _download_request(url, params=params, verify=verify)
    if encoding:
        r.encoding = encoding
    return r.text


def download_content(url, params={}, verify=True):
    r = _download_request(url, params=params, verify=verify)
    return r.content


def jsondownload(url,  params={}, verify=True):
    r = _download_request(url, params=params, verify=verify)
    return r.json()


def download_file(url, path, params={}, verify=True):
    r = _download_request(url, params=params, verify=verify)
    with open(path, "wb") as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)