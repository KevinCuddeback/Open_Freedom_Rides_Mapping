from pathlib import Path
import unittest

from open_freedom_rides import (
    events_for_rider,
    events_in_date_range,
    journey_segments_for_rider,
    load_dataset,
    riders_at_location,
)


class LibraryQueriesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dataset = load_dataset(Path("data/raw/pilot"))

    def test_events_for_rider(self) -> None:
        events = events_for_rider(self.dataset, "rider-john-lewis")
        self.assertGreaterEqual(len(events), 1)

    def test_riders_at_location(self) -> None:
        riders = riders_at_location(self.dataset, "loc-charlotte-nc")
        rider_ids = {r["id"] for r in riders}
        self.assertIn("rider-john-lewis", rider_ids)

    def test_events_in_date_range(self) -> None:
        events = events_in_date_range(self.dataset, "1961-05-04", "1961-05-04")
        self.assertEqual(len(events), 3)

    def test_journey_segments_for_rider(self) -> None:
        segments = journey_segments_for_rider(self.dataset, "rider-john-lewis")
        self.assertEqual(len(segments), 2)


if __name__ == "__main__":
    unittest.main()
