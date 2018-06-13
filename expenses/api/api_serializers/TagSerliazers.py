from rest_framework import serializers
from expenses.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag_name',)
        # fields = '__all__'
