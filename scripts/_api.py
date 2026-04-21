"""TensorArt OpenAPI 共享模块"""

import json
import os
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

BASE_URL = "https://openapi.tensor.art/openworks/v1"


def get_access_key() -> str:
    path = os.path.expanduser("~/.tensor_access_key")
    try:
        with open(path) as f:
            key = f.read().strip()
    except FileNotFoundError:
        print("错误: 未找到 ~/.tensor_access_key", file=sys.stderr)
        print("请先配置: echo \"你的access-key\" > ~/.tensor_access_key", file=sys.stderr)
        sys.exit(1)
    if not key:
        print("错误: ~/.tensor_access_key 内容为空", file=sys.stderr)
        sys.exit(1)
    return key


def api_post(path: str, data: dict, access_key: str | None = None) -> dict:
    if access_key is None:
        access_key = get_access_key()
    url = f"{BASE_URL}/{path}"
    body = json.dumps(data).encode()
    req = Request(url, data=body, method="POST", headers={
        "Content-Type": "application/json",
        "Echo-Access-Key": access_key,
    })
    try:
        with urlopen(req) as resp:
            return json.loads(resp.read())
    except HTTPError as e:
        err_body = e.read().decode(errors="replace")
        print(f"API 错误: HTTP {e.code} {e.reason}", file=sys.stderr)
        print(err_body, file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"连接失败: {e.reason}", file=sys.stderr)
        sys.exit(1)
