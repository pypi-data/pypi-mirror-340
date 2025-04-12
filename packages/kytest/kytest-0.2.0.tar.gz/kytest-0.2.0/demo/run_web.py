"""
@Author: kang.yang
@Date: 2024/7/12 17:10
"""
import kytest


if __name__ == '__main__':
    kytest.main(
        path="tests/test_web.py",
        web_set={
            'host': 'https://www-test.qizhidao.com/'
        },
        run_mode={'xdist': True}
    )


