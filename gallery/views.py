from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from users.models import Family
from rest_framework.exceptions import PermissionDenied

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_family = self.request.user.family
        return self.queryset.filter(family=user_family, status='Y')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, family=self.request.user.family)

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_family = self.request.user.family
        return self.queryset.filter(album__family=user_family, status='Y').order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        photo = self.get_object()
        if photo.user != self.request.user:
            raise PermissionDenied('편집권한x')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied('삭제권한x')
        instance.delete()

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        photo = self.get_object()
        if photo.album.family != request.user.family:
            return Response({'error': '좋아요 권한 x'}, status=status.HTTP_403_FORBIDDEN)
        like, created = PhotoVideoLike.objects.get_or_create(user=request.user, photo=photo)
        if not created:
            return Response({'status': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'Photo liked'})

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        photo = self.get_object()
        if photo.album.family != request.user.family:
            return Response({'error': '좋아요 취소 권한 x'}, status=status.HTTP_403_FORBIDDEN)
        PhotoVideoLike.objects.filter(user=request.user, photo=photo).delete()
        return Response({'status': 'Photo unliked'})

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        photo = self.get_object()
        favorite, created = Favorite.objects.get_or_create(user=request.user, photo=photo)
        if not created:
            return Response({'status': 'Already in favorites'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'Photo added to favorites'})

    @action(detail=True, methods=['post'])
    def unfavorite(self, request, pk=None):
        photo = self.get_object()
        Favorite.objects.filter(user=request.user, photo=photo).delete()
        return Response({'status': 'Photo removed from favorites'})


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_family = self.request.user.family
        return self.queryset.filter(album__family=user_family, status='Y').order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        video = self.get_object()
        if video.user != self.request.user:
            raise PermissionDenied('편집권한 x')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied('삭제권한 x')
        instance.delete()

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        video = self.get_object()
        if video.album.family != request.user.family:
            return Response({'error': '좋아요 권한 x'}, status=status.HTTP_403_FORBIDDEN)
        like, created = PhotoVideoLike.objects.get_or_create(user=request.user, video=video)
        if not created:
            return Response({'status': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'Video liked'})

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        video = self.get_object()
        if video.album.family != request.user.family:
            return Response({'error': '좋아요 취소 권한 x'}, status=status.HTTP_403_FORBIDDEN)
        PhotoVideoLike.objects.filter(user=request.user, video=video).delete()
        return Response({'status': 'Video unliked'})

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        video = self.get_object()
        favorite, created = Favorite.objects.get_or_create(user=request.user, video=video)
        if not created:
            return Response({'status': 'Already in favorites'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'Video added to favorites'})

    @action(detail=True, methods=['post'])
    def unfavorite(self, request, pk=None):
        video = self.get_object()
        Favorite.objects.filter(user=request.user, video=video).delete()
        return Response({'status': 'Video removed from favorites'})


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_family = self.request.user.family
        return self.queryset.filter(
            models.Q(photo__album__family=user_family, photo__status='Y') |
            models.Q(video__album__family=user_family, video__status='Y')
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FavoriteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)