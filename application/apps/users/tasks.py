from typing import Dict, Any

import orjson
from celery import Task
from redis.client import Pipeline
from ronglian_sms_sdk import SmsSDK

from application import celery, redis_check as redis


class SMSTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        print('任务执行成功!')
        return super().on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('任务执行失败!%s' % self.request.retries)
        # 重新尝试执行失败任务，时间间隔:3秒，最大尝试次数：5次
        self.retry(exc=exc, countdown=3, max_retries=5)
        return super().on_failure(exc, task_id, args, kwargs, einfo)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        print('任务执行的回调操作，不管执行的结果是成功还是失败，都会执行这里')
        return super().after_return(status, retval, task_id, args, kwargs, einfo)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        print('当任务尝试重新执行时，会执行到这里，但是目前执行有问题')
        return super().on_retry(exc, task_id, args, kwargs, einfo)


@celery.task(name="send_sms", base=SMSTask)
def send_sms(mobile: str, sms_code: str) -> Dict[str, Any]:
    """发送短信"""
    sdk: SmsSDK = SmsSDK(
        celery.app.config.get("SMS_ACCOUNT_ID"),
        celery.app.config.get("SMS_ACCOUNT_TOKEN"),
        celery.app.config.get("SMS_APP_ID")
    )
    try:
        ret: str = sdk.sendMessage(
            celery.app.config.get("SMS_TEMPLATE_ID"),  # 模板ID
            mobile,  # 用户手机号
            (sms_code, celery.app.config.get("SMS_EXPIRE_TIME") // 60)  # 模板变量信息
        )

        # 容联云短信返回的结果是json格式的字符串，需要转换成dict
        result: Dict[str, Any] = orjson.loads(ret)

        # 6个0表示短信发送成功，将验证码缓存到redis中
        if result["statusCode"] == "000000":
            pipe: Pipeline = redis.pipeline()
            pipe.multi()  # 开启事务
            # 保存短信记录到redis中
            pipe.setex("sms_%s" % mobile, celery.app.config.get("SMS_EXPIRE_TIME"), sms_code)
            # 进行冷却倒计时
            pipe.setex("int_%s" % mobile, celery.app.config.get("SMS_INTERVAL_TIME"), "_")
            pipe.execute()  # 提交事务
            return result
        else:
            raise Exception
    except Exception as exc:
        celery.app.logger.error("短信发送失败!\r\n%s" % exc)
        return result
