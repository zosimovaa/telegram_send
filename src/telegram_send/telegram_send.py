"""
The TelegramJustSend class provides sending messages to telegram without guarantees of delivery.
"""
import os
import time
import queue
import logging
import datetime
import requests
import threading

from .spam_filter import SpamFilter


logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


class TelegramJustSend(threading.Thread):
    SILENT_TIME_EVENING = 21
    SILENT_TIME_MORNING = 9
    MAX_BUFFER_SIZE = 20
    TIMEOUT = 1
    URL = "https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}&disable_notification={3}"

    def __init__(self, chat_id, alias, api_key=None):
        threading.Thread.__init__(self, daemon=True)
        self.api_key = os.getenv("TELEGRAM_API_KEY", api_key)
        self.chat_id = chat_id
        self.alias = alias
        self.sc = SpamFilter()

        self.halt = threading.Event()
        self.queue = queue.Queue(maxsize=self.MAX_BUFFER_SIZE)

    def __send(self, message):
        blocked = self.sc.check_block()
        if not blocked:
            silent = self.check_silent()
            message = "[{0}]: {1}".format(self.alias, message)
            url = self.URL.format(self.api_key, self.chat_id, message, silent)
            resp = requests.get(url).json()
            logger.warning(resp)
        else:
            self.queue = queue.Queue(maxsize=self.MAX_BUFFER_SIZE)

    def run(self):
        logger.debug("Started")
        while True:
            try:
                message = self.queue.get()
                logger.debug("got message for send: {0}".format(message))
                self.__send(message)
            except Exception as e:
                logger.error(e)
            finally:
                time.sleep(self.TIMEOUT)

    def stop(self):
        self.halt.set()
        self.join()
        logger.warning('Stopped')

    def send(self, message):
        logger.debug("send: {}".format(message))
        self.queue.put_nowait(message)

    def check_silent(self):
        now = datetime.datetime.now()
        silent = True if (now.hour > self.SILENT_TIME_EVENING) or (now.hour < self.SILENT_TIME_MORNING) else False
        logger.debug("check_silent(): silent: {0}, hour: {1}".format(silent, now.hour))
        return silent
