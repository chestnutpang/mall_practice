import os
import sys
import signal
import time
import platform
from utils import file_manage
system_type = 0 if platform.system() == 'Windows' else 1
if system_type:
    import fcntl


class SignalTool:
    """
    进程信号处理
    读取应用的进程号，根据命令对进程进行处理
    启动/重启时更新应用存储的进程号
    """
    # 自定义命令
    CMD_STOP = 'stop'
    CMD_RESTART = 'restart'
    CMD_RELOAD = 'reload'
    CMD_STATE = 'state'

    __pid_path = None

    @classmethod
    def init(cls, pid_path):
        """对进程获取到的信号进行处理"""
        file_manage.check_path(pid_path)
        cls.__pid_path = pid_path
        cls.process_cmd()
        cls.daemonize()
        cls.write_pid_file()

    @classmethod
    def write_pid_file(cls):
        """将新的进程号写入文件"""
        if system_type:
            file_name = cls.get_pid_file_name()
            try:
                f = open(file_name, 'a+')
                fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                f.truncate(0)
                pid = os.getpid()
                f.write(str(pid))
                f.flush()
                cls.PID_FP = f
            except FileNotFoundError:
                sys.stderr.write(f'open pidfile: {file_name} failed\n')
                raise
            except BlockingIOError:
                sys.stderr.write(f'lock pidfile: {file_name} failed\n')
                raise

    @classmethod
    def daemonize(cls):
        """守护进程"""
        if system_type:
            pid = os.fork()
            try:
                if pid > 0:
                    sys.exit(0)
            except OSError as e:
                sys.stderr.write(f"fork #1 failed:{e.errno} ({e.strerror}\n)")
                raise
            os.setsid()
            os.umask(0)

            try:
                pid = os.fork()
                if pid > 0:
                    sys.exit(0)
            except OSError as e:
                sys.stderr.write(f"fork #2 failed:{e.errno} ({e.strerror}\n)")
                raise

    @classmethod
    def process_cmd(cls):
        """处理信号"""
        if len(sys.argv) != 2:
            return
        cmd = sys.argv[1]
        if cmd == cls.CMD_STOP:
            cls.kill_process(signal.SIGTERM)
            sys.exit(0)
        elif cmd == cls.CMD_RESTART:
            cls.kill_process(signal.SIGTERM)
            time.sleep(1)
        elif cmd == cls.CMD_RELOAD:
            cls.kill_process(signal.SIGUSR1)
            sys.exit(0)
        elif cmd == cls.CMD_STATE:
            sys.exit(0)
        else:
            pass

    @classmethod
    def kill_process(cls, sig):
        """终止进程运行"""
        pid = cls.get_current_pid()
        if pid > 0:
            try:
                os.kill(pid, sig)
            except ProcessLookupError:
                sys.stderr.write(f'no such process:{pid}\n')
        else:
            sys.stderr.write('process not running\n')

    @classmethod
    def get_current_pid(cls):
        """获取当前应用进程号"""
        try:
            with open(cls.get_pid_file_name()) as f:
                pid = int(f.read())
        except FileNotFoundError:
            pid = 0
        return pid

    @classmethod
    def get_pid_file_name(cls):
        """获取应用pid文件路径"""
        return os.path.join(cls.__pid_path, f'{cls.get_process_name()}.pid')

    @classmethod
    def get_process_name(cls):
        """获取进程/应用名"""
        return os.path.basename(sys.argv[0]).split('.')[0]


if __name__ == '__main__':
    # signal.alarm()
    print(os.path.basename('./mall_search_application.py'))
