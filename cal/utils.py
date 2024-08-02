from django.shortcuts import get_object_or_404
from users.models import Family

def is_user_family_member(user, family_id):
    family = get_object_or_404(Family, pk=family_id)
    return user in family.created_by.families.all()
