#! -*- encoding: utf-8 -*-

import datetime

from rest_framework.serializers import ModelSerializer, IntegerField, SerializerMethodField, TimeField
from .models import Registration


class RegistrationSerializer(ModelSerializer):
    queue_number = IntegerField(read_only=True)
    waiting_time = SerializerMethodField(method_name="get_waiting_time")
    phone_display = SerializerMethodField(method_name="get_phone")

    class Meta:
        model = Registration
        fields = ("id", "phone", "table_type", "queue_number", "waiting_time",\
                "phone_display", "status")

    def get_waiting_time(self, obj):
        time_delta = datetime.datetime.now() - obj.create_time.replace(tzinfo=None)
        ret = ""

        if time_delta.days > 0:
            ret += "%d" % time_delta.days
            ret += u"天"

        if time_delta.seconds > 3600:
            hours = time_delta.seconds / 3600
            minutes = time_delta.seconds % 3600 / 60
            ret += u"%d小时%d分钟" % (hours, minutes)
        elif 60 < time_delta.seconds < 3600:
            minutes = time_delta.seconds / 60
            ret += u"%d分钟" % minutes
        else:
            ret += u"%d秒" % time_delta.seconds

        return ret

    def get_phone(self, obj):
        try:
            return obj.phone[:3] + '*' * 4 + obj.phone[-4:]
        except:
            return obj.phone


class RegistrationHistorySerializer(ModelSerializer):
    create_time = TimeField(format="%H:%M:%S")
    end_time = TimeField(format="%H:%M:%S")
    phone = SerializerMethodField(method_name="get_phone")
    status = SerializerMethodField(method_name="get_status_desc")
    table_name = SerializerMethodField(method_name="get_table_name")

    class Meta:
        model = Registration
        fields = ("id", "phone", "queue_number", "create_time", "end_time", "status", "table_name")

    def get_phone(self, obj):
        try:
            return obj.phone[:3] + '*' * 4 + obj.phone[-4:]
        except:
            return obj.phone

    def get_table_name(self, obj):
        return obj.table_type.name

    def get_status_desc(self, obj):
        desc = {
            "waiting": u"等待中",
            "turn": u"下一个",
            "expired": u"已就餐",
            "passed": u"已过号"
        }
        return desc[obj.status]

