import gevent


def foo():
    print('running in foo')
    gevent.sleep(2)
    print('com back from bar in to foo')


def bar():
    print('running in bar')
    gevent.sleep(2)
    print('com back from foo in to bar')


if __name__ == '__main__':
    gevent.joinall([gevent.spawn(foo), gevent.spawn(bar)])
