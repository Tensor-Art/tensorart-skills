#!/usr/bin/env python3
"""下载文件到本地
用法: python3 download_result.py <url> [输出路径]
默认保存到 /tmp/result_<timestamp>.<ext>
"""

import os
import sys
import time
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

if len(sys.argv) < 2:
    print("用法: python3 download_result.py <url> [输出路径]", file=sys.stderr)
    sys.exit(1)

url = sys.argv[1]

if len(sys.argv) > 2:
    output_path = sys.argv[2]
else:
    parsed = urlparse(url.split("?")[0])
    ext = Path(parsed.path).suffix or ".png"
    output_path = f"/tmp/result_{int(time.time())}{ext}"

req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urlopen(req, timeout=120) as resp:
        data = resp.read()
except HTTPError as e:
    print(f"下载失败: HTTP {e.code} {e.reason}", file=sys.stderr)
    sys.exit(1)
except URLError as e:
    print(f"连接失败: {e.reason}", file=sys.stderr)
    sys.exit(1)

os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
with open(output_path, "wb") as f:
    f.write(data)

print(f"已保存: {output_path} ({len(data)} bytes)", file=sys.stderr)
print(output_path)
