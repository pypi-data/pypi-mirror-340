"""
@Author: kang.yang
@Date: 2024/7/12 17:10
"""
import kytest


if __name__ == '__main__':
    kytest.main(
        path="tests/test_adr.py",  # 测试脚本目录
        app_set={
            'did': ['417ff34c', 'UQG5T20414005787'],
            'pkg': 'com.qizhidao.clientapp',
            # 'sonic_host': 'http://localhost:3000',
            # 'sonic_user': 'test',
            # 'sonic_pwd': 'wz888888',
            'run_mode': 'polling'
        }
    )



