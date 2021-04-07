from rest_framework import serializers
from .models import OperatingLog, TaskPort
from user.models import UserInfo


class SystemLogSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    operator_id = serializers.SerializerMethodField()
    update_time = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.id

    def get_content(self, obj):
        return obj.content

    def get_operator_id(self, obj):
        return UserInfo.objects.filter(id=obj.operator_id).first().name

    def get_update_time(self, obj):
        return obj.update_time.strftime('%Y-%m-%d %H:%M:%S')


class HostListSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    ip = serializers.SerializerMethodField()
    os_info = serializers.SerializerMethodField()
    port_count = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.id

    def get_name(self, obj):
        return obj.name

    def get_ip(self, obj):
        return obj.ip

    def get_os_info(self, obj):
        return obj.os_info

    def get_port_count(self, obj):
        return len(TaskPort.objects.filter(host__id=obj.id))

    def get_user(self, obj):
        return obj.user.name
