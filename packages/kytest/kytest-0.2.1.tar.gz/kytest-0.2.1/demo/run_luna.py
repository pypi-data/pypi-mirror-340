"""
@Author: kang.yang
@Date: 2025/4/14 09:45
"""
import kytest


if __name__ == '__main__':
    kytest.main(
        path='tests/test_luna.py',
        app_set={'did': 'FMR0223824022829', 'pkg': 'com.luna.music'}
    )

