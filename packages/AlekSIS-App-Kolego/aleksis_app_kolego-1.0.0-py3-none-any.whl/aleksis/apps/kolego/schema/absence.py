from collections.abc import Iterable
from typing import Union

from graphene_django.types import DjangoObjectType

from aleksis.core.schema.base import (
    BaseBatchCreateMutation,
    BaseBatchDeleteMutation,
    BaseBatchPatchMutation,
    DjangoFilterMixin,
    PermissionsTypeMixin,
)

from ..models import Absence, AbsenceReason, AbsenceReasonTag


class AbsenceReasonTagType(PermissionsTypeMixin, DjangoFilterMixin, DjangoObjectType):
    class Meta:
        model = AbsenceReasonTag
        fields = ("id", "short_name", "name")
        filter_fields = {
            "short_name": ["icontains", "exact"],
            "name": ["icontains", "exact"],
        }


class AbsenceReasonType(PermissionsTypeMixin, DjangoFilterMixin, DjangoObjectType):
    class Meta:
        model = AbsenceReason
        fields = ("id", "short_name", "name", "colour", "count_as_absent", "default", "tags")
        filter_fields = {
            "short_name": ["icontains", "exact"],
            "name": ["icontains", "exact"],
        }

    def resolve_tags(root, info, **kwargs):
        return root.tags.filter(absence_reasons=root)


class AbsenceType(PermissionsTypeMixin, DjangoFilterMixin, DjangoObjectType):
    class Meta:
        model = Absence
        fields = (
            "id",
            "person",
            "reason",
            "comment",
            "datetime_start",
            "datetime_end",
            "date_start",
            "date_end",
        )
        filter_fields = {
            "person__full_name": ["icontains", "exact"],
            "comment": ["icontains", "exact"],
        }


class AbsenceBatchCreateMutation(BaseBatchCreateMutation):
    class Meta:
        model = Absence
        fields = (
            "person",
            "reason",
            "comment",
            "datetime_start",
            "datetime_end",
            "date_start",
            "date_end",
        )
        optional_fields = ("comment", "reason")
        permissions = ("kolego.create_absence_rule",)

    @classmethod
    def before_save(cls, root, info, input, created_objs):  # noqa
        modified_absences = []

        for absence in created_objs:
            modified_absences += getattr(absence, "_modified_absences", [])

        return modified_absences


class AbsenceBatchDeleteMutation(BaseBatchDeleteMutation):
    class Meta:
        model = Absence
        permissions = ("kolego.delete_absence_rule",)


class AbsenceBatchPatchMutation(BaseBatchPatchMutation):
    class Meta:
        model = Absence
        fields = (
            "id",
            "person",
            "reason",
            "comment",
            "datetime_start",
            "datetime_end",
            "date_start",
            "date_end",
        )
        permissions = ("kolego.edit_absence_rule",)

    @classmethod
    def after_mutate(cls, root, info, input, updated_objs, return_data):  # noqa
        modified_absences = []

        for absence in updated_objs:
            modified_absences += getattr(absence, "_modified_absences", [])

        return_data[cls._meta.return_field_name] = modified_absences
        return return_data


class AbsenceReasonBatchCreateMutation(BaseBatchCreateMutation):
    class Meta:
        model = AbsenceReason
        fields = ("short_name", "name", "colour", "count_as_absent", "default", "tags")
        optional_fields = ("name",)
        permissions = ("kolego.create_absencereason_rule",)

    @classmethod
    def get_all_objs(cls, Model, ids: Iterable[Union[str, int]]):
        return list(Model.objects.filter(pk__in=[cls.resolve_id(id_) for id_ in ids]))


class AbsenceReasonBatchDeleteMutation(BaseBatchDeleteMutation):
    class Meta:
        model = AbsenceReason
        permissions = ("kolego.delete_absencereason_rule",)


class AbsenceReasonBatchPatchMutation(BaseBatchPatchMutation):
    class Meta:
        model = AbsenceReason
        fields = ("id", "short_name", "name", "colour", "count_as_absent", "default", "tags")
        permissions = ("kolego.edit_absencereason_rule",)

    @classmethod
    def get_all_objs(cls, Model, ids: Iterable[Union[str, int]]):
        return list(Model.objects.filter(pk__in=[cls.resolve_id(id_) for id_ in ids]))


class AbsenceReasonTagBatchCreateMutation(BaseBatchCreateMutation):
    class Meta:
        model = AbsenceReasonTag
        fields = ("short_name", "name")
        optional_fields = ("name",)
        permissions = ("kolego.create_absencereasontag_rule",)


class AbsenceReasonTagBatchDeleteMutation(BaseBatchDeleteMutation):
    class Meta:
        model = AbsenceReasonTag
        permissions = ("kolego.delete_absencereasontag_rule",)


class AbsenceReasonTagBatchPatchMutation(BaseBatchPatchMutation):
    class Meta:
        model = AbsenceReasonTag
        fields = ("id", "short_name", "name")
        permissions = ("kolego.edit_absencereasontag_rule",)
