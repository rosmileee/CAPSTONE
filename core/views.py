from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .serializers import RegisterSerializer, AppointmentSerializer
from .models import Appointment

# ✅ Register New User
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
    'message': 'User registered successfully',
    'token': token.key,
    'username': user.username,
    'email': user.email,
}, status=status.HTTP_201_CREATED)


# ✅ Login Existing User
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'message': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_obj = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    user = authenticate(username=user_obj.username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'Login successful',
            'token': token.key,
            'username': user.username,
            'email': user.email,
        }, status=status.HTTP_200_OK)

    return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

# ✅ Get Authenticated User's Profile
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    return Response({
        "email": user.email,
        "username": user.username,
        "profile_image": None  # You can add image handling here later
    }, status=status.HTTP_200_OK)

# ✅ Book Appointment (Safe Update)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_appointment(request):
    serializer = AppointmentSerializer(data=request.data)
    if serializer.is_valid():
        appointment = serializer.save(user=request.user)
        return Response({
            "message": "Appointment booked successfully",
            "appointment": AppointmentSerializer(appointment).data
        }, status=status.HTTP_201_CREATED)
    else:
        # Add debug log to check what's wrong
        print("❌ Appointment submission failed. Errors:", serializer.errors)
        return Response({
            "message": "Failed to book appointment",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
