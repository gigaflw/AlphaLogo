# -*- coding: utf-8 -*-
#
# According to a paragraph introducing a logo, judge the possible industry the logo belongs to.

import jieba
import time


INDU_PROFI = 0
INDU_ORGANIZATION = 1
INDU_ENTERTAINMENT = 2
INDU_FESTIVAL = 3
INDU_TEAM = 4
INDU_OTHER = 5

keywords = {
    INDU_PROFI: [u'公司', u'工作室', u'店', u'品牌', u'食品',
                 u'甜品', u'集团', u'银行', u'业务', u'服务',
                 u'俱乐部', u'博物馆', u'度假区', u'旅游', u'度假',
                 u'酒店', u'剧院', u'餐饮', u'互联网', u'经济',
                 u'医院', u'商城', u'服装', u'房产', u'企业',
                 u'客户', u'工业', u'市场', u'电视台', u'旅行社',
                 u'行业', u'地铁', u'运营', u'业务', u'浏览器',
                 u'商店', u'会所', u'腾讯'u'单位', u'软件', u'产品',
                 u'传媒', u'厂', u'店'],
    INDU_ORGANIZATION : [u'基金会', u'基金', u'希望工程', u'联合会'],
    INDU_ENTERTAINMENT : [u'游戏', u'动漫', u'电子竞技', u'运动', u'动画'],
    INDU_FESTIVAL : [u'晚会', u'运动会', u'音乐会', u'国庆', u'论坛',
                     u'冬奥会', u'奥运会', u'联赛', u'奥委会', u'青奥会', u'赛事',
                     u'图书馆', u'博物馆', u'博物院', u'世博会'],
    INDU_TEAM : [u'队', u'学校', u'大学', u'学校']
}


def classify(info):
    info = jieba.cut(info, cut_all=True)

    for word in info:
        for indu, kw_list in keywords.items():
            if any(kw in word for kw in kw_list):
                return indu

    return INDU_OTHER
