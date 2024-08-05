from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Album, Photo, Comment, Favorite
from .serializers import AlbumSerializer, PhotoSerializer, CommentSerializer, FavoriteSerializer, PhotoBookSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from accounts.models import Profile
from datetime import timezone
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
        user_profile = Profile.objects.get(user=self.request.user)
        family = user_profile.family
        if family is None:
            raise ValidationError("Family is not set for the user's profile.")
        
        serializer.save(user=self.request.user, family=family)

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_family = self.request.user.profile.family
        return self.queryset.filter(family=user_family, status='Y').order_by('-created_at')

    def perform_create(self, serializer):
        try:
            user_profile = Profile.objects.get(user=self.request.user)
            family = user_profile.family
            if family is None:
                raise ValidationError("Family is not set for the user's profile.")
        except Profile.DoesNotExist:
            raise ValidationError("Profile for the user does not exist.")
        
        serializer.save(user=self.request.user, family=family)

    def perform_update(self, serializer):
        photo = self.get_object()
        if photo.user != self.request.user:
            raise PermissionDenied('편집권한이 없습니다.')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied('삭제권한이 없습니다.')
        instance.delete()

    @action(detail=True, methods=['post'])
    def add_to_album(self, request, pk=None):
        photo = self.get_object()
        if photo.user != request.user:
            raise PermissionDenied('편집권한이 없습니다.')
        
        album_id = request.data.get('album')
        try:
            album = Album.objects.get(id=album_id, family=request.user.profile.family)
            photo.album = album
            photo.save()
            return Response({'status': '사진이 앨범에 추가되었습니다.'}, status=status.HTTP_200_OK)
        except Album.DoesNotExist:
            return Response({'error': '앨범이 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 현재 로그인한 사용자의 가족의 즐겨찾기를 조회
        user_family = self.request.user.profile.family
        return Favorite.objects.filter(user__profile__family=user_family)

    def create(self, request, *args, **kwargs):
        photo_id = request.data.get('photo')
        photo = get_object_or_404(Photo, id=photo_id)
        user = request.user

        # 이미 즐겨찾기에 추가된 사진을 확인하고 204 NO CONTENT 반환
        favorite, created = Favorite.objects.get_or_create(photo=photo, user=user)
        if not created:
            return Response({'message': '이미 즐겨찾기에 추가된 사진입니다.'}, status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_family = self.request.user.profile.family
        return self.queryset.filter(photo__family=user_family, photo__status='Y')

    def perform_create(self, serializer):
        photo_id = self.request.data.get('photo')
        if not photo_id:
            raise ValidationError('Photo ID is required to create a comment.')
        try:
            photo = Photo.objects.get(id=photo_id, family=self.request.user.profile.family)
        except Photo.DoesNotExist:
            raise ValidationError('Photo does not exist or does not belong to your family.')
        
        serializer.save(user=self.request.user, photo=photo)

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.user != self.request.user:
            raise PermissionDenied('편집권한이 없습니다.')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied('삭제권한이 없습니다.')
        instance.delete()

class PhotoBookViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def create_photobook(self, request):
        serializer = PhotoBookSerializer(data=request.data)
        if serializer.is_valid():
            photo_ids = serializer.validated_data['photo_ids']
            photos = Photo.objects.filter(id__in=photo_ids, user__profile__family=request.user.profile.family)

            pdf = FPDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()

            for photo in photos:
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt=photo.description, ln=True)
                pdf.image(photo.image.path, w=100)

            pdf_output_path = os.path.join(settings.MEDIA_ROOT, 'photobooks')
            os.makedirs(pdf_output_path, exist_ok=True)
            # 파일 이름에 타임스탬프를 추가하여 파일명 충돌 방지
            pdf_file = os.path.join(pdf_output_path, f'photobook_{request.user.id}_{timezone.now().strftime("%Y%m%d%H%M%S")}.pdf')
            pdf.output(pdf_file)

            pdf_url = f'{settings.MEDIA_URL}photobooks/photobook_{request.user.id}_{timezone.now().strftime("%Y%m%d%H%M%S")}.pdf'
            return Response({'pdf_url': pdf_url}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
