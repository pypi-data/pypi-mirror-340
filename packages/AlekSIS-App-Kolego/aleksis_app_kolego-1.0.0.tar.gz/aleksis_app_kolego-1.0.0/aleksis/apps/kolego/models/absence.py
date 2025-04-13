from datetime import date, datetime, time

from django.db import models
from django.db.models import Q, QuerySet
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from colorfield.fields import ColorField

from aleksis.core.managers import (
    CalendarEventManager,
)
from aleksis.core.mixins import ExtensibleModel
from aleksis.core.models import FreeBusy, Person

from ..managers import AbsenceQuerySet


class AbsenceReasonTag(ExtensibleModel):
    short_name = models.CharField(verbose_name=_("Short name"), max_length=255, unique=True)
    name = models.CharField(verbose_name=_("Name"), max_length=255)

    def __str__(self):
        if self.name:
            return f"{self.short_name} ({self.name})"
        else:
            return self.short_name

    class Meta:
        verbose_name = _("Absence reason tag")
        verbose_name_plural = _("Absence reason tags")


class AbsenceReason(ExtensibleModel):
    short_name = models.CharField(verbose_name=_("Short name"), max_length=255, unique=True)
    name = models.CharField(verbose_name=_("Name"), max_length=255)

    colour = ColorField(verbose_name=_("Colour"), blank=True)

    count_as_absent = models.BooleanField(
        default=True,
        verbose_name=_("Count as absent"),
        help_text=_(
            "If checked, this excuse type will be counted as absent. If not checked,"
            "it won't show up in absence reports."
        ),
    )

    default = models.BooleanField(verbose_name=_("Default Reason"), default=False)

    tags = models.ManyToManyField(
        AbsenceReasonTag, blank=True, verbose_name=_("Tags"), related_name="absence_reasons"
    )

    def __str__(self):
        if self.name:
            return f"{self.short_name} ({self.name})"
        else:
            return self.short_name

    def save(self, *args, **kwargs):
        # Ensure that there is only one default absence reason
        if self.default:
            reasons = AbsenceReason.objects.filter(default=True)
            if self.pk:
                reasons.exclude(pk=self.pk)
            reasons.update(default=False)
        super().save(*args, **kwargs)

    @classmethod
    def get_default(cls) -> "AbsenceReason":
        try:
            return cls.objects.get(default=True)
        except cls.ObjectDoesNotExist:
            return cls.objects.create(default=True, short_name="u", name=_("Unexcused"))

    @property
    def count_label(self):
        return f"reason_{self.id}_count"

    class Meta:
        verbose_name = _("Absence reason")
        verbose_name_plural = _("Absence reasons")
        constraints = [
            models.UniqueConstraint(
                fields=["default"],
                condition=models.Q(default=True),
                name="only_one_default_absence_reason",
            )
        ]
        ordering = ["-default"]


class Absence(FreeBusy):
    objects = CalendarEventManager.from_queryset(AbsenceQuerySet)()

    reason = models.ForeignKey(
        "AbsenceReason",
        on_delete=models.PROTECT,
        related_name="absences",
        verbose_name=_("Absence reason"),
    )

    person = models.ForeignKey(
        "core.Person",
        on_delete=models.CASCADE,
        related_name="kolego_absences",
        verbose_name=_("Person"),
    )

    comment = models.TextField(verbose_name=_("Comment"), blank=True)

    @classmethod
    def get_objects(
        cls,
        request: HttpRequest | None = None,
        params: dict[str, any] | None = None,
        additional_filter: Q | None = None,
        **kwargs,
    ) -> QuerySet:
        q = additional_filter or Q()
        if params:
            if params.get("person"):
                q = q & Q(person_id=params["person"])
            elif params.get("persons"):
                q = q & Q(person_id__in=params["persons"])
            elif params.get("group"):
                q = q & Q(person__member_of__id=params.get("group"))
        qs = super().get_objects(
            request, params, additional_filter=q, select_related=["person", "reason"], **kwargs
        )

        return qs

    @classmethod
    def value_title(cls, reference_object: "Absence", request: HttpRequest | None = None) -> str:
        """Return the title of the calendar event."""
        return f"{reference_object.person} ({reference_object.reason})"

    @classmethod
    def value_description(
        cls, reference_object: "Absence", request: HttpRequest | None = None
    ) -> str:
        """Return the title of the calendar event."""
        return ""

    @classmethod
    def clear_or_extend_absences_in_timespan(
        cls,
        person: Person,
        datetime_start: datetime,
        datetime_end: datetime,
        reason: AbsenceReason | None = None,
    ) -> list:
        extended_absence = None
        modified_absences = []

        events_within = cls.get_objects(
            None,
            {"person": person.pk},
            start=datetime_start,
            end=datetime_end,
        )

        for event_within in events_within:
            event_within_datetime_start = (
                event_within.datetime_start
                if event_within.datetime_start
                else datetime.combine(event_within.date_start, time.min)
            )
            event_within_datetime_end = (
                event_within.datetime_end
                if event_within.datetime_end
                else datetime.combine(event_within.date_end, time.max)
            )

            # If overlapping absence has the same reason, just extend it
            if reason is not None and event_within.reason == reason:
                event_within.datetime_start = min(datetime_start, event_within_datetime_start)
                event_within.datetime_end = max(datetime_end, event_within_datetime_end)
                event_within.save(skip_overlap_handling=True)
                extended_absence = event_within
                modified_absences.append(event_within)
            else:
                if (
                    datetime_start > event_within_datetime_start
                    and datetime_end < event_within_datetime_end
                ):
                    # Cut existing event in two parts
                    # First, cut end date of existing one
                    event_within.datetime_end = datetime_start
                    event_within.save(skip_overlap_handling=True)
                    modified_absences.append(event_within)
                    # Then, create new event based on existing one filling up the remaining time
                    end_filler_event = event_within
                    end_filler_event.pk = None
                    end_filler_event.id = None
                    end_filler_event.calendarevent_ptr_id = None
                    end_filler_event.freebusy_ptr_id = None
                    end_filler_event._state.adding = True
                    end_filler_event.datetime_start = datetime_end
                    end_filler_event.datetime_end = event_within_datetime_end

                    end_filler_event.save(skip_overlap_handling=True)
                    modified_absences.append(end_filler_event)
                elif (
                    datetime_start <= event_within_datetime_start
                    and datetime_end >= event_within_datetime_end
                ):
                    # Delete existing event
                    if event_within in modified_absences:
                        modified_absences.remove(event_within)
                    event_within.delete()
                elif (
                    datetime_start > event_within_datetime_start
                    and datetime_start < event_within_datetime_end
                    and datetime_end >= event_within_datetime_end
                ):
                    # Cut end of existing event
                    event_within.datetime_end = datetime_start
                    event_within.save(skip_overlap_handling=True)
                    modified_absences.append(event_within)
                elif (
                    datetime_start <= event_within_datetime_start
                    and datetime_end < event_within_datetime_end
                    and datetime_end > event_within_datetime_start
                ):
                    # Cut start of existing event
                    event_within.datetime_start = datetime_end
                    event_within.save(skip_overlap_handling=True)
                    modified_absences.append(event_within)

        return modified_absences, extended_absence

    def __str__(self):
        return f"{self.person} ({self.datetime_start} - {self.datetime_end})"

    def save(self, *args, skip_overlap_handling: bool = False, **kwargs):
        extended_absence = None
        modified_absences = []

        if not skip_overlap_handling:
            # Convert dates of new event to datetimes in case dates are used
            new_datetime_start = (
                self.datetime_start
                if self.datetime_start
                else datetime.combine(self.date_start, time.min)
            ).astimezone(self.timezone)
            new_datetime_end = (
                self.datetime_end
                if self.datetime_end
                else datetime.combine(self.date_end, time.max)
            ).astimezone(self.timezone)

            modified_absences, extended_absence = self.clear_or_extend_absences_in_timespan(
                self.person, new_datetime_start, new_datetime_end, self.reason
            )
            modified_absences.append(self)

        if extended_absence is not None:
            self._extended_absence = extended_absence
        else:
            super().save(*args, **kwargs)
        self._modified_absences = modified_absences

    @classmethod
    def get_for_person_by_datetimes(
        cls,
        person: Person,
        datetime_start: datetime | None = None,
        datetime_end: datetime | None = None,
        date_start: date | None = None,
        date_end: date | None = None,
        defaults: dict | None = None,
        **kwargs,
    ) -> "Absence":
        data = {"person": person, **kwargs}

        if date_start:
            data["date_start"] = date_start
            data["date_end"] = date_end
        else:
            data["datetime_start"] = datetime_start
            data["datetime_end"] = datetime_end

        absence, created = cls.objects.get_or_create(**data, defaults=defaults)

        if created:
            if hasattr(absence, "_extended_absence"):
                return absence._extended_absence
            return absence
        return absence

    class Meta:
        verbose_name = _("Absence")
        verbose_name_plural = _("Absences")
