from django.shortcuts import get_object_or_404
from pydantic import ValidationError
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CulturalActivity, Reservation, ConfirmedReservation, Like
from .serializers import CulturalActivitySerializer, ReservationSerializer, ConfirmedReservationSerializer, LikeSerializer
from accounts.models import Profile
from rest_framework.exceptions import NotFound

class CulturalActivityViewSet(viewsets.ModelViewSet):
    queryset = CulturalActivity.objects.filter(status='Y')
    serializer_class = CulturalActivitySerializer

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        activity_id = request.data.get('activity')
        subcategory_id = request.data.get('subcategory', None)
        people = request.data.get('people', 1)  # 기본값 1
        price = request.data.get('price', None)

        activity = get_object_or_404(CulturalActivity, id=activity_id)
        user = request.user

        confirmed_reservations_count = ConfirmedReservation.objects.filter(reservation__activity=activity).count()
        if confirmed_reservations_count >= activity.available_slots:
            return Response({'message': '예약 가능한 자원이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        reservation_data = {
            'activity': activity.id,
            'people': people,
            'price': price,
            'status': 'C',
            'start_date': activity.start_date,
            'end_date': activity.end_date,
            'thumbnail': activity.thumbnail
        }
        if subcategory_id:
            reservation_data['subcategory'] = subcategory_id

        serializer = self.get_serializer(data=reservation_data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            reservation = serializer.save(user=user)

            ConfirmedReservation.objects.create(
                reservation=reservation,
                start_date=activity.start_date,
                end_date=activity.end_date,
                thumbnail=activity.thumbnail
            )

            response_data = serializer.data
            response_data['activity'] = CulturalActivitySerializer(activity).data

            headers = self.get_success_headers(serializer.data)
            return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
        except ValidationError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            user_profile = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            raise NotFound('Profile matching query does not exist.')
        
        family = user_profile.family
        return Like.objects.filter(user__profile__family=family)

    def create(self, request, *args, **kwargs):
        activity_id = request.data.get('activity')
        activity = get_object_or_404(CulturalActivity, id=activity_id)
        user = request.user

        like, created = Like.objects.get_or_create(activity=activity, user=user)
        if not created:
            like.delete()
            return Response({'message': 'Like removed.'}, status=status.HTTP_200_OK)
        
        return Response({'message': 'Liked.'}, status=status.HTTP_201_CREATED)