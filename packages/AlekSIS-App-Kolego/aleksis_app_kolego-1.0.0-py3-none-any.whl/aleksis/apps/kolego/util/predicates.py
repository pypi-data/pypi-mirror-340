from django.contrib.auth.models import User

from rules import predicate

from aleksis.core.models import Person
from aleksis.core.util.core_helpers import get_site_preferences

from ..models import Absence


@predicate
def can_manage_absences_for_person(user: User, obj: Person) -> bool:
    """Predicate for viewing absences of a person."""
    group_types = get_site_preferences()["kolego__group_types_manage_person_absences"]
    if not group_types:
        return False
    qs = obj.member_of.filter(owners=user.person)
    return qs.filter(group_type__in=group_types).exists()


@predicate
def can_manage_absence(user: User, obj: Absence) -> bool:
    group_types = get_site_preferences()["kolego__group_types_manage_person_absences"]
    if not group_types:
        return False
    qs = obj.person.member_of.filter(owners=user.person)
    return qs.filter(group_type__in=group_types).exists()
