"""
The spam filter allows you to limit the distribution of messages in case of
a large number of messages in a short period of time.
"""

import time
import logging
import collections

logger = logging.getLogger(__name__)


class SpamFilter:
    SPAM_MESSAGE = "Spam detected, take a brake :)"

    def __init__(self, threshold=10, control_period=120, silence_period=1800):
        self.threshold = threshold
        self.control_period = control_period
        self.silence_period = silence_period
        self.spam_buffer = collections.deque(maxlen=self.threshold)
        self.blocked = False

    def check_block(self):
        now = time.time()

        # Not initialized yet
        if len(self.spam_buffer) < self.threshold:
            self.spam_buffer.append(now)
            logger.debug("Not a spam. Current len buffer: {}".format(len(self.spam_buffer)))

        # unblocked
        elif not self.blocked:
            self.spam_buffer.append(now)
            timeout = self.spam_buffer[-1] - self.spam_buffer[0]
            logger.debug("check_block() - not blocked. timeout: {}".format(timeout))
            if timeout < self.control_period:
                message = self.SPAM_MESSAGE
                self.blocked = True
                logger.warning("Spam detected")

        # blocked
        else:
            timeout = now - self.spam_buffer[-1]
            logger.debug("check_block() - blocked. timeout: {}".format(timeout))
            if timeout > self.silence_period:
                self.blocked = False
                self.spam_buffer = collections.deque(maxlen=self.threshold)
                self.spam_buffer.append(now)
                logger.debug("Spam filter unblock")

        return self.blocked
