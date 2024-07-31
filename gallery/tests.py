import os
from django.conf import settings
from django.urls import reverse, get_resolver
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from gallery.models import Album, Photo, Comment, Favorite
from users.models import Family
from pprint import pprint

User = get_user_model()

class GalleryTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.family = Family.objects.create(family_name='Test Family', created_by=self.user)
        self.client.login(username='testuser', password='testpass')
        self.album = Album.objects.create(user=self.user, name='Test Album', family=self.family, status='Y')
        self.image_path = os.path.join(settings.MEDIA_ROOT, 'photos', '조성현 사진.png')

        # Ensure the test image file exists
        assert os.path.exists(self.image_path), f'Test image file not found: {self.image_path}'

    def test_create_album(self):
        url = reverse('albums-list')
        data = {'name': 'New Album', 'family': self.family.family_id, 'status': 'Y'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Album.objects.count(), 2)
    
    def test_create_photo(self):
        url = reverse('photos-list')
        with open(self.image_path, 'rb') as image:
            data = {'album': self.album.id, 'image': image, 'description': 'Test Photo', 'status': 'Y'}
            response = self.client.post(url, data, format='multipart')
        print(response.json())  # 응답 데이터를 출력하여 디버깅
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Photo.objects.count(), 1)
    
    def test_create_comment(self):
        photo = Photo.objects.create(user=self.user, album=self.album, image=self.image_path, description='Test Photo', status='Y')
        url = reverse('comments-list')
        data = {'photo': photo.id, 'text': 'Test Comment'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)

    def test_add_favorite(self):
        photo = Photo.objects.create(user=self.user, album=self.album, image=self.image_path, description='Test Photo', status='Y')
        # URL 패턴 출력
        print("Registered URL patterns:")
        pprint(list(get_resolver().reverse_dict.keys()))

        # 생성된 photo 객체 확인
        print(f"Created photo: {photo.id}, {photo.user}, {photo.album}, {photo.image}, {photo.description}, {photo.status}")

        url = reverse('photos-favorite', args=[photo.id])
        print(f"Request URL: {url}")  # 요청 URL 출력
        response = self.client.post(url)
        if response.status_code != status.HTTP_200_OK:
            print(f"Response status code: {response.status_code}")
            print(f"Response data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Favorite.objects.count(), 1)
    
    def test_create_photobook(self):
        photo = Photo.objects.create(user=self.user, album=self.album, image=self.image_path, description='Test Photo', status='Y')
        url = reverse('photobooks-create-photobook')
        data = {'photo_ids': [photo.id]}
        response = self.client.post(url, data, format='json')
        print(response.json())  # 응답 데이터를 출력하여 디버깅
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('pdf_url', response.json())
