from rest_framework import serializers
from .models import TextData

class TextDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextData
        fields = ['id', 'content', 'lang', 'project', 'name', 'occupation', 'address', 'phone',
            'district_corporation', 'taluka_zone', 'village_area', 'subject', 'department',
            'email', 'mode', 'created_at']
