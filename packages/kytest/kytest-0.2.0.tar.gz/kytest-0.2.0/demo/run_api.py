"""
@Author: kang.yang
@Date: 2024/7/12 17:10
"""
import kytest
from data.login_data import get_headers


if __name__ == '__main__':
    kytest.main(
        path="tests/test_api.py",  # 测试脚本目录
        api_set={
            'host': 'https://app-test.qizhidao.com/',
            'headers': get_headers()
        },
        run_mode={'xdist': True}
    )



