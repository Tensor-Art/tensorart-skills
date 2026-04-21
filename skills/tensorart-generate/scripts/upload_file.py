#!/usr/bin/env python3
"""上传本地文件到 Cloudflare R2
用法: python3 upload_file.py <本地文件路径> [文件名]
输出: JSON {"displayUrl": "...", "accessUrl": "..."}
"""

import json
import mimetypes
import os
import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

sys.path.insert(0, os.path.dirname(__file__))
from _api import api_post, get_access_key

if len(sys.argv) < 2:
    print("用法: python3 upload_file.py <本地文件路径> [文件名]", file=sys.stderr)
    sys.exit(1)

file_path = sys.argv[1]
filename = sys.argv[2] if len(sys.argv) > 2 else Path(file_path).name

with open(file_path, "rb") as f:
    data = f.read()

print(f"文件大小: {len(data)} bytes", file=sys.stderr)

# 1. 获取上传地址
access_key = get_access_key()
resp = api_post("file/upload", {"filename": filename}, access_key)
if resp.get("code") != "0":
    print(f"获取上传地址失败: {json.dumps(resp, ensure_ascii=False)}", file=sys.stderr)
    sys.exit(1)

upload_url = resp["data"]["uploadUrl"]
display_url = resp["data"].get("displayUrl", "")
access_url = resp["data"].get("accessUrl", "")

# 2. PUT 上传到 Cloudflare
content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
req = Request(upload_url, data=data, method="PUT", headers={"Content-Type": content_type})
try:
    with urlopen(req) as r:
        if r.status == 200:
            print("上传成功", file=sys.stderr)
        else:
            print(f"上传失败: HTTP {r.status}", file=sys.stderr)
            sys.exit(1)
except HTTPError as e:
    print(f"上传失败: HTTP {e.code} {e.reason}", file=sys.stderr)
    sys.exit(1)
except URLError as e:
    print(f"连接失败: {e.reason}", file=sys.stderr)
    sys.exit(1)

# 输出结果
result = {"displayUrl": display_url, "accessUrl": access_url}
print(json.dumps(result, ensure_ascii=False))
