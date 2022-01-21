#!/bin/bash
export FLASK_APP="/home/wang/mofang_api/manage.py"
# 生产模式/运营模式
# export FLASK_ENV=product
# 开发模式
export FLASK_ENV=development

if [ $1 ]; then
  if [ $1 == "run" ]; then
    flask run --host=0.0.0.0 --port=5000
  elif [ $1 == "startapp" ]; then
    cd application/apps
    flask $1 --name=$2
  elif [ $1 == "celery" ]; then
    celery -A manage.celery worker -l info

  elif [ $1 == "beat" ]; then
    celery -A manage.celery beat -l info
  else
    flask $1
  fi
fi
