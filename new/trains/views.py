from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.authtoken.views import ObtainAuthToken
from .models import CustomUser, Train, Booking
from .serializers import UserSerializer, TrainSerializer, BookingSerializer

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'status': 'Account successfully created',
            'status_code': 200,
            'user_id': serializer.data['id']
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'status': 'Login successful',
                'status_code': 200,
                'user_id': user.id,
                'access_token': token.key
            })
        return Response({
            'status': 'Incorrect username/password provided. Please retry',
            'status_code': 401
        })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_train(request):
    serializer = TrainSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Train added successfully',
            'train_id': serializer.data['id']
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_seat_availability(request):
    source = request.GET.get('source')
    destination = request.GET.get('destination')

    trains = Train.objects.filter(source=source, destination=destination, seat_capacity__gt=0)
    
    if not trains:
        return Response({
            'message': 'No trains available for this route'
        }, status=status.HTTP_404_NOT_FOUND)

    train_data = []
    for train in trains:
        available_seats = train.seat_capacity - Booking.objects.filter(train=train).count()
        train_data.append({
            'train_id': train.id,
            'train_name': train.train_name,
            'available_seats': available_seats
        })

    return Response(train_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_seat(request, train_id):
    user_id = request.user.id
    no_of_seats = request.data.get('no_of_seats')
    
    try:
        train = Train.objects.get(pk=train_id)
    except Train.DoesNotExist:
        return Response({
            'message': 'Train not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    available_seats = train.seat_capacity - Booking.objects.filter(train=train).count()
    
    if available_seats < no_of_seats:
        return Response({
            'message': 'Not enough seats available on this train'
        }, status=status.HTTP_400_BAD_REQUEST)


    return Response({
        'message': 'Seat booked successfully',
        'booking_id': booking.id,
        'seat_numbers': booked_seats
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_booking_details(request, booking_id):
    user_id = request.user.id
    
    try:
        booking = Booking.objects.get(pk=booking_id, user=user_id)
    except Booking.DoesNotExist:
        return Response({
            'message': 'Booking not found'
        }, status=status.HTTP_404_NOT_FOUND)

    booking_data = {
        'booking_id': booking.id,
        'train_id': booking.train.id,
        'train_name': booking.train.train_name,
        'user_id': booking.user.id,
        'no_of_seats': booking.no_of_seats,
        'seat_numbers': booking.seat_numbers,
        'arrival_time_at_source': booking.train.arrival_time_at_source,
        'arrival_time_at_destination': booking.train.arrival_time_at_destination
    }

    return Response(booking_data, status=status.HTTP_200_OK)
