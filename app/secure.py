# db
from app.jobs import modify_score, query_scihub_ck

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@10.10.100.2:7821/magweb?charset=utf8'
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/microanaly?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = "64ebe6f0ee0411e8a8b56c92bf4f31c4"

MAIL_SERVER = 'smtphm.qiye.163.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USER_TSL = False
MAIL_USERNAME = 'tmagweb@microanaly.com'
MAIL_PASSWORD = 'WeiFen2019'
MAIL_SUBJECT_PREFIX = '[微分]'
MAIL_SENDER = '微分交付中心<tmagweb@microanaly.com>'

SCHEDULER_API_ENABLED = True
JOBS = [
    {
        'id': 'job1_modify_score',
        'func': modify_score,
        'trigger': 'cron',
        'hour': 12,
        'minute': 0,
    },
    {
        'id': 'job2_query_scihub',
        'func': query_scihub_ck,
        'trigger': 'cron',
        'hour': 0,
        'minute': 0,
    }
]
