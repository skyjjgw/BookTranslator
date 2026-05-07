from loguru import logger
import os,sys

# 获取绝对路径目录
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


log_dir = os.path.join(root, 'logs')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

LOG_FILE = 'translation.log'
#trace debug info warning error critical success等级日志输出
class Logger:
    def __init__(self):
        log_file_path = os.path.join(log_dir, LOG_FILE)
        self.logger = logger
        self.logger.remove()

        #添加控制台输出的格式，sys.stdout为输出到屏幕；
        self.logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")

        #添加文件输出的格式，log_file_path为输出到文件；
        self.logger.add(log_file_path, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>", rotation="10 MB", retention="10 days")
    def get_logger(self):
        return self.logger
log = Logger().get_logger()#放这里是为了在其他模块中直接导入log对象使用，避免每次都需要创建Logger实例并调用get_logger方法获取日志对象
if __name__ == "__main__":
    log = Logger().get_logger()
    log.debug("这是一个debug日志")
    log.info("这是一个info日志")
    log.warning("这是一个warning日志")
    log.error("这是一个error日志")
    log.critical("这是一个critical日志")