from application import celery
from application import init_app, Flask

app: Flask = init_app("application.settings.dev")


@celery.task(name="send_sms")
def send_sms(mobile: str):
    """占用celery导包，不然代码格式化把导包删除了，shell启动不了celery"""
    print("发送短信~")


if __name__ == '__main__':
    app.run()
    send_sms.delay("18888888888")
