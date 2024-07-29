# tests.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from users.models import Family
from gallery.models import Album, Photo, Comment, Favorite
from django.core.files.uploadedfile import SimpleUploadedFile
import os

User = get_user_model()

class GalleryModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')
        self.family = Family.objects.create(family_name='Test Family', created_by=self.user)
        self.album = Album.objects.create(user=self.user, name='Test Album', family=self.family)
        self.photo = Photo.objects.create(user=self.user, album=self.album, image='photos/조성현 사진.jpg')

    def test_album_creation(self):
        self.assertEqual(self.album.name, 'Test Album')
        self.assertEqual(self.album.user, self.user)

    def test_photo_creation(self):
        self.assertEqual(self.photo.image.name, 'photos/조성현 사진.jpg')
        self.assertEqual(self.photo.user, self.user)

    def test_comment_creation(self):
        comment = Comment.objects.create(user=self.user, photo=self.photo, text='Nice photo!')
        self.assertEqual(comment.text, 'Nice photo!')
        self.assertEqual(comment.user, self.user)

    def test_favorite_creation(self):
        favorite = Favorite.objects.create(user=self.user, photo=self.photo)
        self.assertEqual(favorite.photo, self.photo)
        self.assertEqual(favorite.user, self.user)

class GalleryViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')
        self.family = Family.objects.create(family_name='Test Family', created_by=self.user)
        self.album = Album.objects.create(user=self.user, name='Test Album', family=self.family)
        self.photo = Photo.objects.create(user=self.user, album=self.album, image='photos/조성현 사진.jpg')
        self.client.force_authenticate(user=self.user)

    def test_create_album(self):
        data = {'name': 'New Album', 'shared': False, 'family': self.family.family_id}
        response = self.client.post('/gallery/albums/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Album.objects.count(), 2)

    def test_create_photo(self):
        # 절대 경로로 설정
        image_path = os.path.join(os.path.dirname(__file__), '..', 'media', 'photos', '조성현 사진.jpg')
        with open(image_path, 'rb') as image_file:
            data = {'album': self.album.id, 'image': SimpleUploadedFile(image_file.name, image_file.read(), content_type='image/jpeg')}
            response = self.client.post('/gallery/photos/', data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
            self.assertEqual(Photo.objects.count(), 2)

    def test_comment_photo(self):
        data = {'photo': self.photo.id, 'text': 'Great photo!'}
        response = self.client.post('/gallery/comments/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().text, 'Great photo!')
