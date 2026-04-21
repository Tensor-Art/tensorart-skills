#!/usr/bin/env python3
"""创建 TensorArt 生成任务
用法: python3 create_task.py <toolName> '<inputs_json>'
输出: JSON {"taskId": "...", "status": "..."}
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _api import api_post

if len(sys.argv) != 3:
    print("用法: python3 create_task.py <toolName> '<inputs_json>'", file=sys.stderr)
    sys.exit(1)

tool_name = sys.argv[1]
inputs = json.loads(sys.argv[2])

resp = api_post("task", {"toolName": tool_name, "inputs": inputs})
if resp.get("code") != "0":
    print(f"创建任务失败: {json.dumps(resp, ensure_ascii=False)}", file=sys.stderr)
    sys.exit(1)

task = resp["data"]["task"]
result = {"taskId": task["id"], "status": task["status"]}
print(json.dumps(result, ensure_ascii=False))
