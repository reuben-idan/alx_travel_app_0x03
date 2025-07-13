from django.test import TestCase
from django.contrib.auth.models import User
from .models import Listing, Booking
from django.urls import reverse
from rest_framework.test import APIClient
from unittest.mock import patch

# Create your tests here.

class BookingEmailTaskTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpass')
        self.listing = Listing.objects.create(title='Test Listing', description='Test Desc', price_per_night=100, location='Test City')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    @patch('listings.tasks.send_booking_confirmation_email.delay')
    def test_booking_triggers_email_task(self, mock_send_email):
        url = reverse('booking-list')
        data = {
            'user': self.user.id,
            'listing': self.listing.id,
            'check_in': '2024-07-01',
            'check_out': '2024-07-05'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(mock_send_email.called)
        args, kwargs = mock_send_email.call_args
        self.assertIn(self.user.email, args)
        self.assertIn('Booking Confirmation', args)
        self.assertIn('Test Listing', args[2])
