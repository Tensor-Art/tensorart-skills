#!/usr/bin/env python3
"""查询 TensorArt 任务状态
用法: python3 query_task.py <taskId> [--poll]
  --poll  轮询模式，3秒间隔，最多60次，状态输出到stderr，结果JSON输出到stdout
  无参数  单次查询，结果JSON输出到stdout
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
from _api import api_post

TERMINAL = {"FINISH", "EXCEPTION", "CANCELED"}

if len(sys.argv) < 2:
    print("用法: python3 query_task.py <taskId> [--poll]", file=sys.stderr)
    sys.exit(1)

task_id = sys.argv[1]
poll = "--poll" in sys.argv

def query_once():
    resp = api_post("task/query", {"taskIds": [task_id]})
    if resp.get("code") != "0":
        print(f"查询失败: {json.dumps(resp, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)
    return resp["data"]["tasks"][0]

if not poll:
    task = query_once()
    print(json.dumps(task, ensure_ascii=False))
    sys.exit(0)

for i in range(1, 61):
    task = query_once()
    status = task.get("status", "UNKNOWN")
    print(f"轮询 #{i}: {status}", file=sys.stderr)
    if status in TERMINAL:
        print(json.dumps(task, ensure_ascii=False))
        sys.exit(0 if status == "FINISH" else 1)
    time.sleep(3)

print("超时: 任务仍在处理中", file=sys.stderr)
print(json.dumps(task, ensure_ascii=False))
sys.exit(2)
