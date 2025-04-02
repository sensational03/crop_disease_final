
from rest_framework import serializers


class loginInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')