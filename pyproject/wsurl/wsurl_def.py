# -*- coding: utf-8 -*-
# @Time    : 2016/12/13 10:30
# @Author  : jmhuo

from collections import namedtuple

HttpRequest = namedtuple('HttpRequest', ['id', 'type','url','data'])
HttpResponse = namedtuple('HttpResponse', ['id','isok', 'status_code', 'content'])
