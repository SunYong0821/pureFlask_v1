# -*- coding: utf-8 -*-
from app.models import User, SCIhub
import requests
from lxml import etree
from datetime import datetime

__author__ = 'zhengpanone'
from app.extensions import db


def modify_score():
    """定时修改用户积分，每天12点重置积分"""
    with db.app.app_context():
        User.query.filter_by(confirm=1).update({'scores': 10})
        db.session.commit()


def query_scihub_ck():
    html = requests.get("https://wadauk.github.io/scihub_ck/index.html",
                        headers={
                            'user-agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0"})
    if html.status_code != 200:
        return 0
    select = etree.HTML(html.text)
    url = select.xpath("//a/p[@class='m-text']/text()")
    time = select.xpath("//p[@class='m-text']/text()")
    seq = select.xpath("//h2[@class='ui orange header m-inline-block m-text-thin']/text()")

    with db.app.app_context():
        for i in range(1, len(int(seq) + 1)):
            SCIhub.query.filter_by(id=i).update({'name': url[i - 1], 'time': time[i - 1], 'addtime': datetime.now()})
        db.session.commit()
