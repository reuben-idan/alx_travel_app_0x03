from django.shortcuts import render

# Create your views here.
# alx_travel_app/listings/views.py

from rest_framework import viewsets
from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer, PaymentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import requests
from .tasks import send_booking_confirmation_email

class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        booking = serializer.save()
        user_email = booking.user.email
        subject = 'Booking Confirmation'
        message = f"Dear {booking.user.username}, your booking for {booking.listing.title} from {booking.check_in} to {booking.check_out} has been confirmed."
        send_booking_confirmation_email.delay(user_email, subject, message)

class PaymentInitiateView(APIView):
    def post(self, request):
        booking_id = request.data.get('booking_id')
        amount = request.data.get('amount')
        user_email = request.data.get('email')
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)
        # Prepare Chapa API request
        chapa_url = 'https://api.chapa.co/v1/transaction/initialize'
        headers = {
            'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        data = {
            'amount': str(amount),
            'currency': 'ETB',
            'email': user_email,
            'first_name': request.data.get('first_name', ''),
            'last_name': request.data.get('last_name', ''),
            'tx_ref': f'booking_{booking_id}_{booking.user.id}',
            'callback_url': request.build_absolute_uri('/api/payments/verify/'),
        }
        chapa_response = requests.post(chapa_url, json=data, headers=headers)
        if chapa_response.status_code == 200 and chapa_response.json().get('status') == 'success':
            resp_data = chapa_response.json()['data']
            payment = Payment.objects.create(
                booking=booking,
                amount=amount,
                status='Pending',
                transaction_id=resp_data['tx_ref'],
            )
            return Response({
                'payment_url': resp_data['checkout_url'],
                'payment': PaymentSerializer(payment).data
            }, status=status.HTTP_201_CREATED)
        return Response({'error': 'Failed to initiate payment.'}, status=status.HTTP_400_BAD_REQUEST)

class PaymentVerifyView(APIView):
    def get(self, request):
        tx_ref = request.query_params.get('tx_ref')
        if not tx_ref:
            return Response({'error': 'tx_ref is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            payment = Payment.objects.get(transaction_id=tx_ref)
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found.'}, status=status.HTTP_404_NOT_FOUND)
        chapa_url = f'https://api.chapa.co/v1/transaction/verify/{tx_ref}'
        headers = {
            'Authorization': f'Bearer {settings.CHAPA_SECRET_KEY}',
        }
        chapa_response = requests.get(chapa_url, headers=headers)
        if chapa_response.status_code == 200 and chapa_response.json().get('status') == 'success':
            resp_data = chapa_response.json()['data']
            if resp_data['status'] == 'success':
                payment.status = 'Completed'
                payment.save()
                return Response({'status': 'Payment completed', 'payment': PaymentSerializer(payment).data})
            else:
                payment.status = 'Failed'
                payment.save()
                return Response({'status': 'Payment failed', 'payment': PaymentSerializer(payment).data})
        return Response({'error': 'Failed to verify payment.'}, status=status.HTTP_400_BAD_REQUEST)
