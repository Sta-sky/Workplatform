# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from .models import MindNode


class MindTreeSerializer(serializers.ModelSerializer):
    child = serializers.ListField(source='get_sub_note', child=RecursiveField())
    parent = serializers.SerializerMethodField()

    class Meta:
        model = MindNode
        # exclude = ["group","text","cou_group_child","actual_vm","pdf","video"]
        fields = ["id","parent", "name", "left", "children","index"]

    def get_parent(self, obj):
        if obj.child:

            return obj.child.id
        else:
            return None
