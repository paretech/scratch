# Copyright 2024 All Rights Reserved - Matthew Pare

import logging

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

class SharedCounter():
    def __init__(self):
        log.info(f'Creating {self.__class__.__name__}')
        self.reset()

    def increment(self):
        log.info(f'Incrementing')
        self._counter += 1

    def reset(self):
        log.info(f'Reset')
        self._counter = 0
    
    @property
    def count(self):
        return self._counter

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[logging.StreamHandler()],
    )
    counter = SharedCounter()

    log.info('Done!')
