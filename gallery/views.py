from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Album, Photo, Comment, Favorite
from .serializers import AlbumSerializer, PhotoSerializer, CommentSerializer, FavoriteSerializer, PhotoBookSerializer
from django.http import HttpResponse
from fpdf import FPDF
from django.conf import settings
import os

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_family = self.request.user.profile.family
        return self.queryset.filter(family=user_family, status='Y')

    def perform_create(self, serializer):
         serializer.save(user=self.request.user.profile, family=self.request.user.profile.family)

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_family = self.request.user.profile.family
        return self.queryset.filter(album__family=user_family, status='Y').order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.profile)

    def perform_update(self, serializer):
        photo = self.get_object()
        if photo.user != self.request.user.profile:
            raise PermissionDenied('편집 권한이 없습니다.')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user.profile:
            raise PermissionDenied('삭제 권한이 없습니다.')
        instance.delete()

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_family = self.request.user.profile.family
        return self.queryset.filter(photo__album__family=user_family, photo__status='Y')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.profile)

class FavoriteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user.profile)

class PhotoBookViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def create_photobook(self, request):
        serializer = PhotoBookSerializer(data=request.data)
        if serializer.is_valid():
            photo_ids = serializer.validated_data['photo_ids']
            photos = Photo.objects.filter(id__in=photo_ids, user__family=request.user.profile.family)

            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            for photo in photos:
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt=photo.description, ln=True)
                pdf.image(photo.image.path, w=100)

            pdf_output_path = os.path.join(settings.MEDIA_ROOT, 'photobooks')
            os.makedirs(pdf_output_path, exist_ok=True)
            pdf_file = os.path.join(pdf_output_path, f'photobook_{request.user.id}.pdf')
            pdf.output(pdf_file)

            pdf_url = os.path.join(settings.MEDIA_URL, 'photobooks', f'photobook_{request.user.id}.pdf')
            return Response({'pdf_url': pdf_url}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
