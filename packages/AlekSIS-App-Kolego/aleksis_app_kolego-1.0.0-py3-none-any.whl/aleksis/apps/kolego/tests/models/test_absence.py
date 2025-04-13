from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import pytest

from aleksis.apps.kolego.models import Absence, AbsenceReason
from aleksis.core.models import Person

pytestmark = pytest.mark.django_db


@pytest.fixture
def absences_test_data():
    datetime_start_existing_1 = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc).astimezone(
        ZoneInfo("Europe/Berlin")
    )
    datetime_end_existing_1 = datetime(2024, 1, 2, 10, 0, tzinfo=timezone.utc).astimezone(
        ZoneInfo("Europe/Berlin")
    )
    datetime_start_existing_2 = datetime(2024, 1, 2, 12, 0, tzinfo=timezone.utc).astimezone(
        ZoneInfo("Europe/Berlin")
    )
    datetime_end_existing_2 = datetime(2024, 1, 3, 19, 43, tzinfo=timezone.utc).astimezone(
        ZoneInfo("Europe/Berlin")
    )

    reason_1 = AbsenceReason.objects.create(short_name="i", name="ill")
    reason_2 = AbsenceReason.objects.create(short_name="e", name="excused")
    reason_1.refresh_from_db()
    reason_2.refresh_from_db()

    person_1 = Person.objects.create(first_name="Maria", last_name="Montessori")
    person_2 = Person.objects.create(first_name="Karl Moritz", last_name="Fleischer")
    person_1.refresh_from_db()
    person_2.refresh_from_db()

    # Create existing absencess
    existing_absence_1 = Absence.objects.create(
        datetime_start=datetime_start_existing_1,
        datetime_end=datetime_end_existing_1,
        person=person_1,
        reason=reason_1,
    )
    existing_absence_2 = Absence.objects.create(
        datetime_start=datetime_start_existing_2,
        datetime_end=datetime_end_existing_2,
        person=person_1,
        reason=reason_1,
    )
    existing_absence_1.refresh_from_db()
    existing_absence_2.refresh_from_db()

    return {
        "datetime_start_existing_1": datetime_start_existing_1,
        "datetime_end_existing_1": datetime_end_existing_1,
        "datetime_start_existing_2": datetime_start_existing_2,
        "datetime_end_existing_2": datetime_end_existing_2,
        "reason_1": reason_1,
        "reason_2": reason_2,
        "person_1": person_1,
        "person_2": person_2,
        "existing_absence_1": existing_absence_1,
        "existing_absence_2": existing_absence_2,
    }


# Create new absences in six scenarios in relation to existing
# absence 1 with same person and different absence reason


# 1: new absence is fully inside exiting absence
def test_overlapping_single_absence_different_reason_inside(absences_test_data):
    datetime_start_new = datetime(2024, 1, 1, 14, 0, tzinfo=timezone.utc).astimezone(
        ZoneInfo("Europe/Berlin")
    )
    datetime_end_new = datetime(2024, 1, 2, 8, 0, tzinfo=timezone.utc).astimezone(
        ZoneInfo("Europe/Berlin")
    )
    new_absence = Absence.objects.create(
        datetime_start=datetime_start_new,
        datetime_end=datetime_end_new,
        person=absences_test_data["person_1"],
        reason=absences_test_data["reason_2"],
    )
    new_absence.refresh_from_db()

    absences_test_data["existing_absence_1"].refresh_from_db()

    assert absences_test_data["existing_absence_1"].datetime_start == datetime(
        2024, 1, 1, 12, 0, tzinfo=timezone.utc
    )
    assert absences_test_data["existing_absence_1"].datetime_end == datetime(
        2024, 1, 1, 14, 0, tzinfo=timezone.utc
    )

    assert new_absence.datetime_start == datetime(2024, 1, 1, 14, 0, tzinfo=timezone.utc)
    assert new_absence.datetime_end == datetime(2024, 1, 2, 8, 0, tzinfo=timezone.utc)

    assert len(Absence.objects.all()) == 4
    assert Absence.objects.filter(
        datetime_start=datetime(2024, 1, 2, 8, 0, tzinfo=timezone.utc)
    ).exists()

    existing_absence_1_part_2 = Absence.objects.get(
        datetime_start=datetime(2024, 1, 2, 8, 0, tzinfo=timezone.utc)
    )

    assert existing_absence_1_part_2.datetime_start == datetime(
        2024, 1, 2, 8, 0, tzinfo=timezone.utc
    )
    assert existing_absence_1_part_2.datetime_end == datetime(
        2024, 1, 2, 10, 0, tzinfo=timezone.utc
    )


# 2: new absence covers the same time span as the existing one
def test_overlapping_single_absence_different_reason_same(absences_test_data):
    datetime_start_new = absences_test_data["datetime_start_existing_1"]
    datetime_end_new = absences_test_data["datetime_end_existing_1"]
    new_absence = Absence.objects.create(
        datetime_start=datetime_start_new,
        datetime_end=datetime_end_new,
        person=absences_test_data["person_1"],
        reason=absences_test_data["reason_2"],
    )
    new_absence.refresh_from_db()

    assert len(Absence.objects.all()) == 2
    assert (
        not Absence.objects.filter(
            datetime_start=datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc),
            datetime_end=datetime(2024, 1, 2, 10, 0, tzinfo=timezone.utc),
        )
        .exclude(pk=new_absence.pk)
        .exists()
    )

    assert new_absence.datetime_start == datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    assert new_absence.datetime_end == datetime(2024, 1, 2, 10, 0, tzinfo=timezone.utc)


# 3: new absence starts earlier and ends later than the existing absence
def test_overlapping_single_absence_different_reason_exceed(absences_test_data):
    datetime_start_new = datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc).astimezone(
        ZoneInfo("Europe/Berlin")
    )
    datetime_end_new = datetime(2024, 1, 2, 12, 0, tzinfo=timezone.utc).astimezone(
        ZoneInfo("Europe/Berlin")
    )
    new_absence = Absence.objects.create(
        datetime_start=datetime_start_new,
        datetime_end=datetime_end_new,
        person=absences_test_data["person_1"],
        reason=absences_test_data["reason_2"],
    )
    new_absence.refresh_from_db()

    assert len(Absence.objects.all()) == 2
    assert not Absence.objects.filter(
        datetime_start=datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc),
        datetime_end=datetime(2024, 1, 2, 10, 0, tzinfo=timezone.utc),
    ).exists()

    assert new_absence.datetime_start == datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc)
    assert new_absence.datetime_end == datetime(2024, 1, 2, 12, 0, tzinfo=timezone.utc)


# 4: new absence starts before existing absence and ends within the existing absence
def test_overlapping_single_absence_different_reason_cut_start(absences_test_data):
    datetime_start_new = datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc).astimezone(
        ZoneInfo("Europe/Berlin")
    )
    datetime_end_new = datetime(2024, 1, 1, 14, 0, tzinfo=timezone.utc).astimezone(
        ZoneInfo("Europe/Berlin")
    )
    new_absence = Absence.objects.create(
        datetime_start=datetime_start_new,
        datetime_end=datetime_end_new,
        person=absences_test_data["person_1"],
        reason=absences_test_data["reason_2"],
    )
    new_absence.refresh_from_db()

    absences_test_data["existing_absence_1"].refresh_from_db()

    assert absences_test_data["existing_absence_1"].datetime_start == datetime(
        2024, 1, 1, 14, 0, tzinfo=timezone.utc
    )
    assert absences_test_data["existing_absence_1"].datetime_end == datetime(
        2024, 1, 2, 10, 0, tzinfo=timezone.utc
    )

    assert new_absence.datetime_start == datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc)
    assert new_absence.datetime_end == datetime(2024, 1, 1, 14, 0, tzinfo=timezone.utc)


# 5: new absence starts within existing absence and ends after the existing absence
def test_overlapping_single_absence_different_reason_cut_end(absences_test_data):
    datetime_start_new = datetime(2024, 1, 2, 8, 0, tzinfo=timezone.utc).astimezone(
        ZoneInfo("Europe/Berlin")
    )
    datetime_end_new = datetime(2024, 1, 2, 12, 0, tzinfo=timezone.utc).astimezone(
        ZoneInfo("Europe/Berlin")
    )
    new_absence = Absence.objects.create(
        datetime_start=datetime_start_new,
        datetime_end=datetime_end_new,
        person=absences_test_data["person_1"],
        reason=absences_test_data["reason_2"],
    )
    new_absence.refresh_from_db()

    absences_test_data["existing_absence_1"].refresh_from_db()

    assert absences_test_data["existing_absence_1"].datetime_start == datetime(
        2024, 1, 1, 12, 0, tzinfo=timezone.utc
    )
    assert absences_test_data["existing_absence_1"].datetime_end == datetime(
        2024, 1, 2, 8, 0, tzinfo=timezone.utc
    )

    assert new_absence.datetime_start == datetime(2024, 1, 2, 8, 0, tzinfo=timezone.utc)
    assert new_absence.datetime_end == datetime(2024, 1, 2, 12, 0, tzinfo=timezone.utc)


# 6: new absence is completely outside of existing absence
def test_overlapping_single_absence_different_reason_outside(absences_test_data):
    datetime_start_new = datetime(2024, 1, 1, 8, 0, tzinfo=timezone.utc).astimezone(
        ZoneInfo("Europe/Berlin")
    )
    datetime_end_new = datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc).astimezone(
        ZoneInfo("Europe/Berlin")
    )
    new_absence = Absence.objects.create(
        datetime_start=datetime_start_new,
        datetime_end=datetime_end_new,
        person=absences_test_data["person_1"],
        reason=absences_test_data["reason_2"],
    )
    new_absence.refresh_from_db()

    absences_test_data["existing_absence_1"].refresh_from_db()

    assert absences_test_data["existing_absence_1"].datetime_start == datetime(
        2024, 1, 1, 12, 0, tzinfo=timezone.utc
    )
    assert absences_test_data["existing_absence_1"].datetime_end == datetime(
        2024, 1, 2, 10, 0, tzinfo=timezone.utc
    )

    assert new_absence.datetime_start == datetime(2024, 1, 1, 8, 0, tzinfo=timezone.utc)
    assert new_absence.datetime_end == datetime(2024, 1, 1, 10, 0, tzinfo=timezone.utc)
