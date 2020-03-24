from django.contrib.auth.models import User
from django.test import TestCase

from .models import Profile

# models test


class ProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="user1", password="123456")
        Profile.objects.create(city="noida", contact_no="1234567890")

    def test_create_profile(self):
        user = User.objects.get(username="user1")
        profile_details = Profile.objects.get(user=user)
        self.assertEqual(profile_details.city, "noida")
