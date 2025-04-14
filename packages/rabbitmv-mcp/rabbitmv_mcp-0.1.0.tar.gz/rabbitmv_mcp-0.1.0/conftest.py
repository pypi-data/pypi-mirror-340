"""
Pytest 配置文件
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
root_dir = Path(__file__).parent
sys.path.append(str(root_dir))
