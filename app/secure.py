# db
#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@10.10.100.2:7821/magweb?charset=utf8'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/magweb?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = "64ebe6f0ee0411e8a8b56c92bf4f31c4"

MAIL_SERVER = 'smtp-n.global-mail.cn'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USER_TSL = False
MAIL_USERNAME = 'tmagweb@microanaly.com'
MAIL_PASSWORD = 'Tmagweb1212@'
MAIL_SUBJECT_PREFIX = '[微分]'
MAIL_SENDER = '微分交付中心<tmagweb@microanaly.com>'
