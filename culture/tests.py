# culture/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Category, SubCategory, CulturalActivity, Reservation, ConfirmedReservation, Like
from users.models import Family  # Family 모델 임포트

class ModelTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(email='testuser@example.com', password='testpass')
        self.family = Family.objects.create(family_name='Test Family', created_by=self.user)  # 유효한 Family 객체 생성
        self.category = Category.objects.create(name='Music')
        self.subcategory = SubCategory.objects.create(category=self.category, name='Concert')
        self.activity = CulturalActivity.objects.create(
            title='Rock Concert',
            description='A rock music concert.',
            date='2024-08-01T20:00:00Z',
            created_by=self.user,
            family=self.family,  # 유효한 Family 객체 사용
            price=50.00,
            available_slots=10,
            category=self.category,
            subcategory=self.subcategory
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Music')

    def test_subcategory_creation(self):
        self.assertEqual(self.subcategory.name, 'Concert')

    def test_activity_creation(self):
        self.assertEqual(self.activity.title, 'Rock Concert')
        self.assertEqual(self.activity.description, 'A rock music concert.')

    def test_reservation_creation(self):
        reservation = Reservation.objects.create(activity=self.activity, user=self.user, status='P')
        self.assertEqual(reservation.activity.title, 'Rock Concert')
        self.assertEqual(reservation.user.email, 'testuser@example.com')

    def test_confirmed_reservation_creation(self):
        reservation = Reservation.objects.create(activity=self.activity, user=self.user, status='P')
        confirmed_reservation = ConfirmedReservation.objects.create(reservation=reservation)
        self.assertEqual(confirmed_reservation.reservation.activity.title, 'Rock Concert')

    def test_like_creation(self):
        like = Like.objects.create(activity=self.activity, user=self.user)
        self.assertEqual(like.activity.title, 'Rock Concert')
        self.assertEqual(like.user.email, 'testuser@example.com')


from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Category, SubCategory, CulturalActivity, Reservation, Like
from users.models import Family  # Family 모델 임포트

class ViewSetTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='testuser@example.com', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.family = Family.objects.create(family_name='Test Family', created_by=self.user)  # 유효한 Family 객체 생성
        self.category = Category.objects.create(name='Music')
        self.subcategory = SubCategory.objects.create(category=self.category, name='Concert')
        self.activity = CulturalActivity.objects.create(
            title='Rock Concert',
            description='A rock music concert.',
            date='2024-08-01T20:00:00Z',
            created_by=self.user,
            family=self.family,  # 유효한 Family 객체 사용
            price=50.00,
            available_slots=10,
            category=self.category,
            subcategory=self.subcategory
        )

    def test_reserve_activity(self):
        url = reverse('activities-reserve', kwargs={'pk': self.activity.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(Reservation.objects.first().status, 'C')

    def test_like_activity(self):
        url = reverse('activities-like', kwargs={'pk': self.activity.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)

    def test_unlike_activity(self):
        Like.objects.create(activity=self.activity, user=self.user)
        url = reverse('activities-unlike', kwargs={'pk': self.activity.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Like.objects.count(), 0)

    def test_get_my_reservations(self):
        reservation = Reservation.objects.create(activity=self.activity, user=self.user, status='C')
        ConfirmedReservation.objects.create(reservation=reservation)
        url = reverse('my_reservations-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_my_likes(self):
        Like.objects.create(activity=self.activity, user=self.user)
        url = reverse('my_likes-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
