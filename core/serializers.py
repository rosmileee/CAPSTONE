from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Appointment  # Import the Appointment model

# Registration Serializer
class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('name', 'email', 'password')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists')
        return value

    def create(self, validated_data):
        name = validated_data.pop('name')
        email = validated_data['email']
        password = validated_data['password']
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )
        return user

# Appointment Serializer
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'id',
            'user',
            'service_type',
            'appointment_date',
            'appointment_time',
            'doctor_name',
            'first_name',
            'last_name',
            'age',
            'gender',
            'reason',
            'booking_for',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'status', 'created_at', 'user']  # 👈 mark 'user' as read-only

    def create(self, validated_data):
        user = self.context['request'].user  # 👈 get logged-in user
        return Appointment.objects.create(user=user, **validated_data)
