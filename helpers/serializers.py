from rest_framework.serializers import ModelSerializer


class BaseSerializer(ModelSerializer):
    basic_fields = ['idx']
    
    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
