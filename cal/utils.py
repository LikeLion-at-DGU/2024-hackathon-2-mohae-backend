from django.contrib.auth import get_user_model
from users.models import Family

User = get_user_model()

def is_user_family_member(user, family_id):
    try:
        family = Family.objects.get(pk=family_id)
        return user.profile.family == family
    except Family.DoesNotExist:
        return False
