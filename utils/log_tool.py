from utils import file_manage, signal_tool
import logging
from logging.handlers import BaseRotatingHandler
import os
import re
import time
import sys


class RotatingHandler(BaseRotatingHandler):
    """
    Handler for logging to a file, rotating the log file at certain timed
    intervals.

    If backupCount is > 0, when rollover is done, no more than backupCount
    files are kept - the oldest ones are deleted.
    """
    def __init__(self, filename, when='h', backupCount=0, encoding=None, delay=False):
        self.when = when.upper()
        self.backupCount = backupCount
        self.prefix = filename
        self.dir, self.base_prefix = os.path.split(self.prefix)
        # Calculate the real rollover interval, which is just the number of
        # seconds between rollovers.  Also set the filename suffix used when
        # a rollover occurs.  Current 'when' events supported:
        # S - Seconds
        # M - Minutes
        # H - Hours
        # D - Days
        # Case of the 'when' specifier is not important; lower or upper case
        # will work.
        if self.when == 'S':
            self.interval = 1 # one second
            self.suffix = "%Y-%m-%d_%H-%M-%S"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}(\.\w+)?$"
        elif self.when == 'M':
            self.interval = 60 # one minute
            self.suffix = "%Y-%m-%d_%H-%M"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}(\.\w+)?$"
        elif self.when == 'H':
            self.interval = 60 * 60 # one hour
            self.suffix = "%Y-%m-%d_%H"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}_\d{2}(\.\w+)?$"
        elif self.when == 'D':
            self.interval = 60 * 60 * 24 # one day
            self.suffix = "%Y-%m-%d"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}(\.\w+)?$"
        else:
            raise ValueError("Invalid rollover interval specified: %s" % self.when)

        self.extMatch = re.compile(self.extMatch, re.ASCII)
        self.new_filename = None

        now = time.time()
        BaseRotatingHandler.__init__(self, self._get_file_name(now), 'a', encoding, delay)

        if self.backupCount > 0:
            self.delete_batch(now)


    def _get_time_str(self, timestamp):
        return time.strftime(self.suffix, time.localtime(timestamp))

    def _get_file_name(self, timestamp):
        return "%s.%s" % (self.prefix, self._get_time_str(timestamp))

    def _get_base_file_name(self, timestamp):
        return "%s.%s" % (self.base_prefix, self._get_time_str(timestamp))

    def shouldRollover(self, record):
        self.new_filename = self._get_file_name(time.time())
        if self.new_filename != self.baseFilename:
            return True
        return False

    def deleteFile(self):
        old_time = time.time() - self.backupCount * self.interval
        old_filename = self._get_file_name(old_time)
        try:
            os.remove(old_filename)
        except FileNotFoundError:
            pass

    def delete_batch(self, now):
        old_time = now - self.backupCount * self.interval
        old_basename = self._get_base_file_name(old_time)

        fileNames = os.listdir(self.dir)
        prefix_len = len(self.base_prefix)
        for fileName in fileNames:
            if len(fileName) <= prefix_len + 1:
                continue
            if fileName[:prefix_len] != self.base_prefix or fileName[prefix_len] != '.':
                continue
            suffix = fileName[prefix_len+1:]
            if self.extMatch.match(suffix) and fileName <= old_basename:
                os.remove(os.path.join(self.dir, fileName))

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None

        if self.new_filename is None:
            self.baseFilename = self._get_file_name(time.time())
        else:
            self.baseFilename = self.new_filename
        self.new_filename = None

        if self.backupCount > 0:
            self.deleteFile()
        if not self.delay:
            self.stream = self._open()


def log_init(log_path, log_level, log_reserve, log_to_console):
    file_manage.check_path(log_path)

    file_handler = RotatingHandler(
        filename=os.path.join(log_path, signal_tool.SignalTool.get_process_name() + '.log'), when='H',
        backupCount=log_reserve, encoding='utf-8', delay=True)

    if log_to_console:
        stream_heandler = logging.StreamHandler(stream=sys.stdout)
        _handlers = (file_handler, stream_heandler)
    else:
        _handlers = (file_handler, )

    logging.basicConfig(
        level=log_level,
        handlers=_handlers,
        format='%(asctime)s[%(levelname)s]|%(name)s|%(process)d|%(threadName)s|' 
               '%(module)s:%(lineno)d(%(funcName)s)|%(message)s')

    logging.getLogger('chardet.charsetprober').setLevel(logging.WARNING)
    logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
