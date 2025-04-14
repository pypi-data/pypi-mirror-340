import sys
import os
# 将项目根目录添加到 Python 路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import pytest
from pathlib import Path
from codertools import process_github_issues,process_github_repo

def test_process_github_repo():
    # 模拟 read_github_repo 的返回值
    tmp_path = "/Users/zhaoxuefeng/GitHub/obsidian_base/Ground/tqdm/docs"
    test_base_path = Path(tmp_path)
    test_base_path.mkdir(exist_ok=True)    
    process_github_repo(base_path=test_base_path,github_path='pydantic/pydantic')
    
    assert any(test_base_path.iterdir())


def test_process_github_issues():
    # 模拟 read_github_repo 的返回值
    tmp_path = "/Users/zhaoxuefeng/GitHub/obsidian_base/Ground/tqdm/issue"
    test_base_path = Path(tmp_path)
    test_base_path.mkdir(exist_ok=True)    
    process_github_issues(base_path=test_base_path,github_path='tqdm/tqdm')

    assert any(test_base_path.iterdir())


