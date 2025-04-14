import sys
import os
# 将项目根目录添加到 Python 路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest

from pathlib import Path
from obragtools.reader import process_github_issues,process_github_repo,get_comments
import shutil

@pytest.fixture
def active_path():
    tmp_path = "/Users/zhaoxuefeng/GitHub/obsidian_base/Ground/tqdm/test"
    test_base_path = Path(tmp_path)
    test_base_path.mkdir(exist_ok=True)
    yield tmp_path
    # 删除 文件
    try:
        shutil.rmtree(test_base_path)
        print(f"成功删除目录及其所有内容: {test_base_path}")
    except Exception as e:
        print(f"删除目录时出错: {e}")


def test_process_github_repo(active_path):
    process_github_repo(base_path=active_path,github_path='pydantic/pydantic')
    # active_path


def test_process_github_issues(active_path):
    process_github_issues(base_path=active_path,github_path='tqdm/tqdm')
    # active_path


def test_get_comments():
    http_ = "https://api.github.com/repos/tqdm/tqdm/issues/13/comments"
    result = get_comments(http_)
    assert result is not None

    

