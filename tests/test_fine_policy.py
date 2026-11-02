from datetime import datetime, timedelta, timezone

from app.modules.loans.policies import DailyFinePolicy

DUE = datetime(2026, 1, 8, tzinfo=timezone.utc)


def test_no_fine_when_returned_on_time():
    assert DailyFinePolicy(1000).calculate(DUE, DUE - timedelta(days=1)) == 0


def test_fine_for_three_late_days():
    assert DailyFinePolicy(1000).calculate(DUE, DUE + timedelta(days=3)) == 3000