from django.shortcuts import get_object_or_404
from django.db import transaction, IntegrityError, DatabaseError  # 트랜잭션 및 데이터베이스 관련 에러 처리를 위해 추가
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError, ParseError, NotAuthenticated
from rest_framework.decorators import action
from accounts.models import Profile
from .models import CulturalActivity, Reservation, ConfirmedReservation, Like
from .serializers import CulturalActivitySerializer, ReservationSerializer, ConfirmedReservationSerializer, LikeSerializer
import logging  # 로깅 기능을 위해 추가


logger = logging.getLogger(__name__)

class CulturalActivityViewSet(viewsets.ModelViewSet):
    queryset = CulturalActivity.objects.filter(status='Y')
    serializer_class = CulturalActivitySerializer

# 개선된 코드
class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        activity_id = request.data.get('activity')
        subcategory_id = request.data.get('subcategory', None)
        people = request.data.get('people', 1)
        price = request.data.get('price', None)
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        # Get the activity object, or return a 404 error if not found
        activity = get_object_or_404(CulturalActivity, id=activity_id)
        user = request.user

        # Check if the activity has available slots
        confirmed_reservations_count = ConfirmedReservation.objects.filter(reservation__activity=activity).count()
        if confirmed_reservations_count >= activity.available_slots:
            return Response({'message': 'No available slots for this activity.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate date logic
        if start_date and end_date and start_date >= end_date:
            return Response({'message': 'End date must be after start date.'}, status=status.HTTP_400_BAD_REQUEST)

        # Prepare data for the new reservation
        reservation_data = {
            'activity': activity.id,
            'user': user.id,
            'people': people,
            'price': price,
            'status': 'C',
            'start_date': start_date,
            'end_date': end_date,
        }

        # Handle subcategory if provided
        if subcategory_id:
            reservation_data['subcategory'] = subcategory_id

        # Include the thumbnail if provided
        if 'thumbnail' in request.FILES:
            reservation_data['thumbnail'] = request.FILES['thumbnail']
        elif activity.thumbnail:
            reservation_data['thumbnail'] = activity.thumbnail

        try:
            # Start a transaction
            with transaction.atomic():
                serializer = self.get_serializer(data=reservation_data, context={'request': request})
                serializer.is_valid(raise_exception=True)
                reservation = serializer.save()
                
                # Create a confirmed reservation
                ConfirmedReservation.objects.create(
                    reservation=reservation,
                    start_date=start_date,
                    end_date=end_date,
                    thumbnail=reservation.thumbnail
                )

                response_data = serializer.data
                response_data['activity'] = CulturalActivitySerializer(activity).data
                headers = self.get_success_headers(serializer.data)
                return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

        except ValidationError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as ie:
            logger.error(f'Database integrity error: {ie}')
            return Response({'message': 'Database integrity error.'}, status=status.HTTP_409_CONFLICT)
        except DatabaseError as de:
            logger.error(f'Database error: {de}')
            return Response({'message': 'Database error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except NotAuthenticated as na:
            logger.error(f'Authentication error: {na}')
            return Response({'message': 'Not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            logger.error(f'Unexpected error occurred: {e}')
            return Response({'message': 'Internal server error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 기존코드
# class ReservationViewSet(viewsets.ModelViewSet):
#     queryset = Reservation.objects.all()
#     serializer_class = ReservationSerializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         activity_id = request.data.get('activity')
#         subcategory_id = request.data.get('subcategory', None)
#         people = request.data.get('people', 1)  # 기본값 1
#         price = request.data.get('price', None)
#         start_date = request.data.get('start_date')
#         end_date = request.data.get('end_date')

#         activity = get_object_or_404(CulturalActivity, id=activity_id)
#         user = request.user

#         confirmed_reservations_count = ConfirmedReservation.objects.filter(reservation__activity=activity).count()
#         if confirmed_reservations_count >= activity.available_slots:
#             return Response({'message': '예약 가능한 자원이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

#         reservation_data = {
#             'activity': activity.id,
#             'people': people,
#             'price': price,
#             'status': 'C',
#             'start_date': start_date,
#             'end_date': end_date,
#             'thumbnail': activity.thumbnail
#         }
#         if subcategory_id:
#             reservation_data['subcategory'] = subcategory_id

#         serializer = self.get_serializer(data=reservation_data, context={'request': request})
#         try:
#             serializer.is_valid(raise_exception=True)
#             reservation = serializer.save()

#             ConfirmedReservation.objects.create(
#                 reservation=reservation,
#                 start_date=start_date,
#                 end_date=end_date,
#                 thumbnail=activity.thumbnail if activity.thumbnail else None
#             )

#             response_data = serializer.data
#             response_data['activity'] = CulturalActivitySerializer(activity).data

#             headers = self.get_success_headers(serializer.data)
#             return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
#         except ValidationError as e:
#             return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_profile = Profile.objects.get(user=self.request.user)
        family = user_profile.family
        return Like.objects.filter(user__profile__family=family)

    def create(self, request, *args, **kwargs):
        activity_id = request.data.get('activity')
        activity = get_object_or_404(CulturalActivity, id=activity_id)
        user = request.user

        like, created = Like.objects.get_or_create(activity=activity, user=user)
        if not created:
            return Response({'message': 'Already liked.'}, status=status.HTTP_200_OK)
        
        return Response({'message': 'Liked.'}, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def remove_like(self, request):
        activity_id = request.data.get('activity')
        user = request.user

        try:
            like = Like.objects.get(activity_id=activity_id, user=user)
            like.delete()
            return Response({'message': 'Like removed.'}, status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({'message': 'Like does not exist.'}, status=status.HTTP_404_NOT_FOUND)