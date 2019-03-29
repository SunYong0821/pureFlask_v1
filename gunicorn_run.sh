/usr/local/python3/bin/python3.6 /usr/local/bin/gunicorn -w17 -D -k gevent -b 0.0.0.0:5000 --access-logfile /opt/log/gunicornlog/5000.log --error-logfile /opt/log/gunicornlog/5000.error manage:app
#/usr/local/python3/bin/python3.6 /usr/local/bin/gunicorn -w17 -D -k gevent -b 0.0.0.0:80 --access-logfile /opt/log/gunicornlog/80.log --error-logfile /opt/log/gunicornlog/80.error manage:app
