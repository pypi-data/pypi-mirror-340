"""
@Author: kang.yang
@Date: 2024/7/12 17:10
"""
import kytest


if __name__ == '__main__':
    kytest.main(
        path="tests/test_ios.py",  # 测试脚本目录
        app_set={
            'did': ['00008110-0018386236A2801E', '00008110-00126192228A801E'],
            'pkg': 'com.tencent.QQMusic',  # 应用包名，针对IOS、安卓、鸿蒙
            'wda_project_path': '/Users/UI/Downloads/WebDriverAgent-master/WebDriverAgent.xcodeproj',
            'sib_path': '/usr/local/bin/sib',
            'sonic_host': 'http://localhost:3000',
            'sonic_user': 'test',
            'sonic_pwd': 'wz888888',
            'run_mode': 'full'
        }
    )



