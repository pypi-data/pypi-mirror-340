import shutil

from .executor import _serial_execute, _parallel_execute

from kytest.running.conf import App
from kytest.utils.log import logger
from kytest.utils.config import FileConfig


class TestMain(object):
    """
    测试框架入口
    """

    def __init__(
            self,
            path: str = None,
            report: str = 'report',
            api_set: dict = None,
            web_set: dict = None,
            app_set: dict = None,
            run_mode: dict = None,
    ):
        """
        @param path: 用例路径
        @param report: 报告路径
        @param api_set: 接口测试配置
            {
                'host': 'xxx',
                'headers': 'xxx'
            }
        @param web_set: web测试配置
            {
                'host': 'xxx',
                'headers': 'xxx'
            }
        @param app_set: app测试配置
            {
                'did': '设备id，可以是单个设备id，也可以是设备id列表',
                'pkg': '应用包名',
                'ability': '鸿蒙应用入口，通过hdc shell aa dump -l 获取',
                'wda_bundle_id': '手机安装的wda的bundle_id',
                'wda_project_path': 'wda项目的主入口文件路径，/Users/UI/Downloads/WebDriverAgent-master/WebDriverAgent.xcodeproj',
                'sib_path': 'sib文件路径，不知道为啥shutil.which拿不到，只好传入，/usr/local/bin/sib',
                'sonic_host': 'sonic服务域名',
                'sonic_user': 'sonic服务用户名',
                'sonic_pwd': 'sonic服务密码',
                'run_mode': '多设备执行模式，full（每个设备执行全用例）、polling（设备轮询获取用例）、默认None'
            }
        @param run_mode: 执行相关设置
            {
                'xdist': '是否启用xdist插件，True、False，默认False',
                'rerun_fails': '失败重试次数，默认0',
                'repeat_times': '重复执行次数，默认0'
            }
        """
        if run_mode is None:
            run_mode = {}
        logger.info("kytest start.")
        # 接口测试设置
        if api_set is not None:
            FileConfig.set_api('base_url', api_set.get('host', None))
            FileConfig.set_api('headers', api_set.get('headers', None))
        # web测试设置
        if web_set is not None:
            FileConfig.set_web('web_url', web_set.get('host', None))
            FileConfig.set_web('headers', web_set.get('headers', None))
        # app测试设置
        if app_set is not None:
            App.did = app_set.get('did', None)
            App.pkg = app_set.get('pkg', None)
            App.ability = app_set.get('ability', None)
            App.wda_bundle_id = app_set.get('wda_bundle_id', None)
            App.wda_project_path = app_set.get('wda_project_path', None)
            App.sib_path = app_set.get('sib_path', None)
            App.sonic_host = app_set.get('sonic_host', None)
            App.sonic_user = app_set.get('sonic_user', None)
            App.sonic_pwd = app_set.get('sonic_pwd', None)
        # 执行相关设置
        if run_mode is None:
            xdist = False
            rerun_fails = 0
            repeat_times = 0
        else:
            xdist = run_mode.get('xdist', False)
            rerun_fails = run_mode.get('rerun_fails', 0)
            repeat_times = run_mode.get('repeat_times', 0)

        if not path:
            raise KeyError('测试用例路径不能为空')

        cmd_str = f'{path} -sv --reruns {str(rerun_fails)} --alluredir {report} --clean-alluredir'
        if xdist:
            cmd_str += ' -n auto'
        if repeat_times:
            cmd_str += f' --count {repeat_times}'

        print('开始执行用例')
        if isinstance(App.did, list):
            if not App.did:
                _serial_execute(path, cmd_str)
            elif len(App.did) == 1:
                App.did = App.did[0]
                _serial_execute(path, cmd_str)
            else:
                # 清空上次执行的目录
                shutil.rmtree(report, ignore_errors=True)
                # 多进程执行
                _parallel_execute(path, report, app_set)

        else:
            # 串行执行
            _serial_execute(path, cmd_str)

        # 文件参数重置
        FileConfig.reset()
        # App参数重置
        App.did = None
        App.pkg = None
        App.ability = None
        App.wda_bundle_id = None
        App.wda_project_path = None
        App.sib_path = None
        App.sonic_host = None
        App.sonic_user = None
        App.sonic_pwd = None


main = TestMain

if __name__ == '__main__':
    main()
