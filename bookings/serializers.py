from rest_framework import serializers
from .models import ClassList,Client


class ClassListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassList
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class BookingSerializer(serializers.Serializer):
    class_id = serializers.IntegerField()
    client_name = serializers.CharField(max_length=25)
    client_email = serializers.EmailField()

    def validate_class_id(self, value):
        if not ClassList.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid class_id: Class not found.")
        return value