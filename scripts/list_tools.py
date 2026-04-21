#!/usr/bin/env python3
"""获取 TensorArt 可用工具列表"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _api import api_post

resp = api_post("tool/list", {})
print(json.dumps(resp, ensure_ascii=False))
