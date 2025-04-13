from aleksis.core.managers import CalendarEventQuerySet, DateRangeQuerySetMixin
from aleksis.core.models import Person


class AbsenceQuerySet(DateRangeQuerySetMixin, CalendarEventQuerySet):
    """QuerySet with custom query methods for absences."""

    def absent_persons(self):
        return Person.objects.filter(absences__in=self).distinct().order_by("short_name")
