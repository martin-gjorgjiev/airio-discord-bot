import logging
import subprocess
logger=logging.getLogger(__name__)
logging.basicConfig(filename='log.txt', level=logging.NOTSET,format='%(asctime)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

def start_airio():
    logger.info(subprocess.run(["./sh start_system.sh"]))

def stop_airio():
    logger.info(subprocess.run(["./sh stop_system.sh"]))
