from django.utils.translation import gettext_lazy as _

from dynamic_preferences.preferences import Section
from dynamic_preferences.types import (
    ModelMultipleChoicePreference,
)

from aleksis.core.models import GroupType
from aleksis.core.registries import site_preferences_registry

kolego = Section("kolego", verbose_name=_("Absences"))


@site_preferences_registry.register
class GroupTypesManagePersonAbsences(ModelMultipleChoicePreference):
    section = kolego
    name = "group_types_manage_person_absences"
    required = False
    default = []
    model = GroupType
    verbose_name = _(
        "User is allowed to manage (planned) absences for members "
        "of groups the user is an owner of with these group types"
    )
