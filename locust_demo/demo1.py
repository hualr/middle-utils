import json
import os

from locust import HttpUser, TaskSet, task, between


class Demo(TaskSet):
    @task
    def test_get(self):
        self.client.get("http://www.baidu.com")

    @task
    def test_post(self):
        responses = self.client.post(url='url', headers='headers', data='body')
        # 对返回内容 进行断言
        if responses.status_code == 200:
            rst = json.loads(responses.text, strict=False)
            if rst['code'] == '00000':
                responses.success()  # Locust ResponseContextManager类提供的  Report the response as successful
            else:
                responses.failure('code：%s ErrorMsg：%s' % (rst['code'], rst['errorMsg']))
        else:
            responses.failure('status_code：%s' % responses.status_code)


class WebsiteUser(HttpUser):
    task_set = Demo
    host = 'http://www.baidu.com'  # 目标服务地址
    # min_wait = 1000  # 单位为ms  最小等待时间  最新版本 已弃用 （当前版本:0.14.5）
    # max_wait = 1000  # 单位为ms  最大等待时间  最新版本 已弃用 （当前版本:0.14.5）

    # between(min_wait, max_wait)
    wait_time = between(2, 5)  # 单位为s   等待时间  任务执行间隔时间


# 以下 便于当前脚本 本地调试
# 启动 当前脚本
if __name__ == "__main__":
    cmd = 'locust -f server.py'
    os.system(cmd)


