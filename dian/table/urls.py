#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns(
    'table.views',

    url(r'^table-type/$', 'list_or_create_table_type'),
    url(r'^table-type/(?P<pk>[0-9]+)/$', 'get_or_update_table_type'),
    url(r'^table-type-details/$', 'list_table_type_details'),

    # for reset table number
    # url(r'^reset-table/$', 'rest_table_nub')

    # 管理餐桌相关
    url(r'^table/$', 'create_table'),
    url(r'^table/$', 'list_table'),
    url(r'^table/(?P<pk>[0-9]+)/$', 'get_table'),
    url(r'^table/(?P<pk>[0-9]+)/$', 'update_table'),
    url(r'^table/(?P<pk>[0-9]+)/$', 'delete_table'),
    url(r'^table-detail/$', 'list_table_detail'),

)
