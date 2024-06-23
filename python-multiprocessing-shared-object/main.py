# Copyright 2024 All Rights Reserved - Matthew Pare

import logging
import logging.config
import multiprocessing.managers
import os

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

class SharedCounter():
    def __init__(self):
        print(f'Creating {self.__class__.__name__} from PID={os.getpid()}')
        self.reset()

    def increment(self):
        print(f'Incrementing from PID={os.getpid()}')
        self._counter += 1

    def reset(self):
        print(f'Reset from PID={os.getpid()}')
        self._counter = 0
    
    @property
    def count(self):
        print(f'Get count from PID={os.getpid()}')
        return self._counter

class MyManager(multiprocessing.managers.BaseManager):
    pass

MyManager.register('SharedCounter', SharedCounter)

def start_manager():
    manager = MyManager()
    manager.start()
    return manager

def create_shared_object(manager):
    shared_object = manager.SharedCounter()
    return shared_object

if __name__ == '__main__':
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - PID: %(process)d - %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'level': 'DEBUG',
            },
            'file': {
                'class': 'logging.FileHandler',
                'formatter': 'standard',
                'filename': 'proc.log',
                'level': 'DEBUG',
            },
        },
        'loggers': {
            '__main__': {  # root logger
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True
            },
            'SharedCounter': {
                'handlers': ['console','file'],
                'level': 'DEBUG',
                'propagate': False
            },
        }
    })

    log.info('Master process started')

    multiprocessing.freeze_support()
    
    manager = start_manager()
    shared_counter = create_shared_object(manager)

    log.info('Done!')
