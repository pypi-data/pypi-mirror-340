from django.apps import apps
from django.db.models import QuerySet
from django.utils import timezone

import graphene
import graphene_django_optimizer
from guardian.shortcuts import get_objects_for_user

from aleksis.apps.kolego.models.absence import Absence, AbsenceReason, AbsenceReasonTag
from aleksis.core.models import Person
from aleksis.core.schema.base import FilterOrderList
from aleksis.core.util.core_helpers import filter_active_school_term_by_date

from .absence import (
    AbsenceBatchCreateMutation,
    AbsenceBatchDeleteMutation,
    AbsenceBatchPatchMutation,
    AbsenceReasonBatchCreateMutation,
    AbsenceReasonBatchDeleteMutation,
    AbsenceReasonBatchPatchMutation,
    AbsenceReasonTagBatchCreateMutation,
    AbsenceReasonTagBatchDeleteMutation,
    AbsenceReasonTagBatchPatchMutation,
    AbsenceReasonTagType,
    AbsenceReasonType,
    AbsenceType,
)


class Query(graphene.ObjectType):
    app_name = graphene.String()
    absences = FilterOrderList(AbsenceType)
    planned_absences_for_person = FilterOrderList(AbsenceType, person=graphene.ID(required=True))
    absence_reasons = FilterOrderList(AbsenceReasonType)
    absence_reason_tags = FilterOrderList(AbsenceReasonTagType)
    all_absence_reason_tags = FilterOrderList(AbsenceReasonTagType)

    @staticmethod
    def resolve_app_name(root, info, **kwargs) -> str:
        return apps.get_app_config("kolego").verbose_name

    @staticmethod
    def resolve_absences(root, info, **kwargs) -> QuerySet:
        return graphene_django_optimizer.query(
            get_objects_for_user(
                info.context.user,
                "kolego.view_absence",
                filter_active_school_term_by_date(info.context, Absence.objects.all()),
            ),
            info,
        )

    @staticmethod
    def resolve_planned_absences_for_person(root, info, person: str, **kwargs):
        person = Person.objects.get(pk=person)
        if not info.context.user.has_perm("kolego.view_person_absences_rule", person):
            return []
        return graphene_django_optimizer.query(
            filter_active_school_term_by_date(
                info.context,
                Absence.objects.filter(
                    person=person, datetime_end__date__gte=timezone.now().date()
                ).order_by("datetime_start"),
            ),
            info,
        )

    @staticmethod
    def resolve_absence_reasons(root, info, **kwargs) -> QuerySet:
        if not info.context.user.has_perm("kolego.fetch_absencereasons_rule"):
            return []
        return graphene_django_optimizer.query(AbsenceReason.objects.all(), info)

    @staticmethod
    def resolve_absence_reason_tags(root, info, **kwargs) -> QuerySet:
        return graphene_django_optimizer.query(
            get_objects_for_user(
                info.context.user,
                "kolego.view_absencereasontag",
                AbsenceReasonTag.objects.all(),
            ),
            info,
        )

    @staticmethod
    def resolve_all_absence_reason_tags(root, info, **kwargs) -> QuerySet:
        return graphene_django_optimizer.query(
            get_objects_for_user(
                info.context.user,
                "kolego.view_absencereasontag",
                AbsenceReasonTag.objects.all(),
            ),
            info,
        )


class Mutation(graphene.ObjectType):
    create_absences = AbsenceBatchCreateMutation.Field()
    delete_absences = AbsenceBatchDeleteMutation.Field()
    update_absences = AbsenceBatchPatchMutation.Field()

    create_absence_reasons = AbsenceReasonBatchCreateMutation.Field()
    delete_absence_reasons = AbsenceReasonBatchDeleteMutation.Field()
    update_absence_reasons = AbsenceReasonBatchPatchMutation.Field()

    create_absence_reason_tags = AbsenceReasonTagBatchCreateMutation.Field()
    delete_absence_reason_tags = AbsenceReasonTagBatchDeleteMutation.Field()
    update_absence_reason_tags = AbsenceReasonTagBatchPatchMutation.Field()
