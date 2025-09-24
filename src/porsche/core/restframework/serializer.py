from typing import override

from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta


class PorscheSerializer(serializers.Serializer):
    pass


class PorscheModelSerializer(serializers.ModelSerializer):
    # 优化原生的序列化器更新操作，只更新需要更新的字段
    # 不支持多对多字段的更新，默认项目里不使用多对多字段.ForeignKey可以获得更多的对中间表的控制
    @override
    def update(self, instance, validated_data):
        raise_errors_on_nested_writes("update", self, validated_data)
        info = model_meta.get_field_info(instance)

        m2m_fields = []
        update_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)
                update_fields.append(attr)
        instance.save(update_fields=update_fields)

        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)
        return instance
