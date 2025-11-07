from datetime import date
from src.finance.application.recorders.base_recorder import Recorder
from src.finance.application.decorators.timing import timed
from src.finance.application.services.analytics_service import AnalyticsService

class AnalyticsFacade:
    def __init__(self, service: AnalyticsService, recorder: Recorder):
        self._diff = timed(recorder, "Analytics.Diff")(service.diff_for_period)
        self._by_cat = timed(recorder, "Analytics.ByCategory")(service.by_category)

    def diff_for_period(self, start: date, end: date) -> float:
        return self._diff(start, end)

    def by_category(self) -> dict[str, dict[str, float]]:
        return self._by_cat()