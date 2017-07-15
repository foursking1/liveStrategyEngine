__author__ = 'foursking'

import datetime
import logging
import time
from common.Errors import StartRunningTimeEmptyError
from common.Log import WQLogger
from common.Time import Time


class BaseMultiLiveStrategyEngine(object):

    def __init__(self, strat, exchanges, timeInterval, startRunningTime, orderWaitingTime, dataLogFixedTimeWindow, dailyExitTime=None):
        self.strat = strat
        self.strat.initialize(self)
        self.startRunningTime = startRunningTime
        self.timeInterval = timeInterval  # 每次循环结束之后睡眠的时间, 单位：秒
        self.orderWaitingTime = orderWaitingTime  # 每次等待订单执行的最长时间
        self.dataLogFixedTimeWindow = dataLogFixedTimeWindow  # 每隔固定的时间打印账单信息，单位：秒
        self.dailyExitTime = dailyExitTime  # 如果设置，则为每天程序的退出时间
        self.TimeFormatForFileName = "%Y%m%d%H%M%S%f"
        self.TimeFormatForLog = "%Y-%m-%d %H:%M:%S.%f"

        self.last_data_log_time = None

        # setup timeLogger
        self.timeLogger = logging.getLogger('timeLog')
        self.timeLogger.setLevel(logging.DEBUG)
        timeLogHandler = logging.FileHandler(self.getTimeLogFileName())
        timeLogHandler.setLevel(logging.DEBUG)
        consoleLogHandler = logging.StreamHandler()
        consoleLogHandler.setLevel(logging.DEBUG)
        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        timeLogHandler.setFormatter(formatter)
        consoleLogHandler.setFormatter(formatter)
        # 给timeLogger添加handler
        self.timeLogger.addHandler(timeLogHandler)
        self.timeLogger.addHandler(consoleLogHandler)

        # setup dataLogger
        self.dataLogger = logging.getLogger('dataLog')
        self.dataLogger.setLevel(logging.DEBUG)
        dataLogHandler = logging.FileHandler(self.getDataLogFileName())
        dataLogHandler.setLevel(logging.DEBUG)
        self.dataLogger.addHandler(dataLogHandler)

        # setup context.log
        self.log = WQLogger(self.timeLogger)

        # setup context.time
        self.time = Time(self.startRunningTime)

        self.exchanges = exchanges
        # setup handle_data
        self.handle_data = self.strat.handle_data



    def getStartRunningTime(self):
        if self.startRunningTime is None:
            raise StartRunningTimeEmptyError("startRunningTime is not set yet!")
        return self.startRunningTime

    def getTimeLogFileName(self):
        return "log/%s_log_%s.txt" % (
            self.strat.__name__, self.getStartRunningTime().strftime(self.TimeFormatForFileName))

    def getDataLogFileName(self):
        return "data/%s_data_%s.data" % (
            self.strat.__name__, self.getStartRunningTime().strftime(self.TimeFormatForFileName))

    def dataLog(self, content=None):
        t = datetime.datetime.now()
        self.last_data_log_time = t
        self.dataLogger.info("%s" % str(content))

    def timeLog(self, content, level=logging.INFO):

        if level == logging.DEBUG:
            self.timeLogger.debug(content)
        elif level == logging.INFO:
            self.timeLogger.info(content)
        elif level == logging.WARN:
            self.timeLogger.warn(content)
        elif level == logging.ERROR:
            self.timeLogger.error(content)
        elif level == logging.CRITICAL:
            self.timeLogger.critical(content)
        else:
            raise ValueError("unsupported logging level %d" % level)

    def go(self):
        self.timeLog("日志启动于 %s" % self.getStartRunningTime().strftime(self.TimeFormatForLog))
        self.dataLog()
        while True:
            # check whether current time is after the dailyExitTime, if yes, exit
            if self.dailyExitTime is not None and datetime.datetime.now() > datetime.datetime.strptime(
                                    datetime.date.today().strftime("%Y-%m-%d") + " " + self.dailyExitTime,
                    "%Y-%m-%d %H:%M:%S"):
                self.timeLog("抵达每日终结时间：%s, 现在退出." % self.dailyExitTime)
                break

            self.timeLog("等待 %d 秒进入下一个循环..." % self.timeInterval)
            time.sleep(self.timeInterval)
            # TODO: to remove this line in production
            # time.sleep(5)

            # calculate the net asset at a fixed time window
            time_diff = datetime.datetime.now() - self.last_data_log_time
            if time_diff.seconds > self.dataLogFixedTimeWindow:
                self.dataLog()

            #self.updateAccountInfo()
            self.handle_data(self)