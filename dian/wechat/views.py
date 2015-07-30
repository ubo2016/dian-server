#!/usr/bin/env python
#! -*- encoding:utf-8 -*-

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes

from wechat_sdk.basic import WechatBasic
from wechat_sdk.messages import TextMessage, VoiceMessage, ImageMessage,\
VideoMessage, LinkMessage, LocationMessage, EventMessage 

from dian.settings import WECHAT_TOKEN

import logging
logger = logging.getLogger('dian')


@api_view(['GET', 'POST'])
@authentication_classes(())
@permission_classes(())
def receive_message(request):
    """
    收取微信消息
    """
    signature = request.GET.get('signature')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')

    wechat = WechatBasic(token=WECHAT_TOKEN)

    logger.debug(request.GET)

    if request.method == 'GET':
        """
        用于在微信配置响应服务器时的验证
        {u'nonce': [u'280474307'], u'timestamp': [u'143801
        5570'], u'echostr': [u'3904558954066704850'], u'signature':
        [u'cfbd4c33549370f85424415310449f44e962c5d7']}
        """
        echostr = request.GET.get('echostr')
        logger.debug(echostr)

        if wechat.check_signature(signature=signature, timestamp=timestamp,\
                nonce=nonce):
            return Response(int(echostr))
        else:
            return Response('')

    elif request.method == 'POST':
        body = request.body
        logger.debug(body)
        if body:
            wechat.parse_data(body)
            message = wechat.get_message()
            logger.debug(message)

            response = ''

            if isinstance(message, TextMessage):
                response = wechat.response_text(content=u'文字信息')
            elif isinstance(message, VoiceMessage):
                response = wechat.response_text(content=u'语音信息')
            elif isinstance(message, ImageMessage):
                response = wechat.response_text(content=u'图片信息')
            elif isinstance(message, VideoMessage):
                response = wechat.response_text(content=u'视频信息')
            elif isinstance(message, LinkMessage):
                response = wechat.response_text(content=u'链接信息')
            elif isinstance(message, LocationMessage):
                response = wechat.response_text(content=u'地理位置信息')
            elif isinstance(message, EventMessage):  # 事件信息
                if message.type == 'subscribe':  # 关注事件(包括普通关注事件和扫描二维码造成的关注事件)
                    if message.key and message.ticket:  # 如果 key 和 ticket 均不为空，则是扫描二维码造成的关注事件
                        response = wechat.response_text(content=u'用户尚未关注时的二维码扫描关注事件')
                    else:
                        response = wechat.response_text(content=u'普通关注事件')
                elif message.type == 'unsubscribe':
                    response = wechat.response_text(content=u'取消关注事件')
                elif message.type == 'scan':
                    response = wechat.response_text(content=u'用户已关注时的二维码扫描事件')
                elif message.type == 'location':
                    response = wechat.response_text(content=u'上报地理位置事件')
                elif message.type == 'click':
                    response = wechat.response_text(content=u'自定义菜单点击事件')
                elif message.type == 'view':
                    response = wechat.response_text(content=u'自定义菜单跳转链接事件')
                elif message.type == 'templatesendjobfinish':
                    response = wechat.response_text(content=u'模板消息事件')

        logger.debug(response)

        return Response(response)


