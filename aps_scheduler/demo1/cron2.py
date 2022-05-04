from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime
from time import sleep

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.blocking import BlockingScheduler


def my_listener(event):
    if event.exception:
        print('The job crashed :(')
    else:
        print('The job worked :)')


def test_tick():
    print(f'The time is: {datetime.now()}')
    sleep(10)


if __name__ == '__main__':
    job_defaults = {'max_instances': 2}

    executors = {
        'default': ThreadPoolExecutor(1),
        'processpool': ProcessPoolExecutor(2)
    }

        # scheduler = BlockingScheduler()
    # 配置最大实例为2个
    scheduler = BlockingScheduler(timezone='MST', job_defaults=job_defaults)

    # 定时轮询
    scheduler.add_job(test_tick, 'interval', seconds=5)
    scheduler.add_job(test_tick, 'interval', seconds=5)
    scheduler.add_job(test_tick, 'interval', seconds=5)

    # 添加监听器
    scheduler.add_listener(my_listener, mask=EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
