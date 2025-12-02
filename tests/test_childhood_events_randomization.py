"""
Test randomization of childhood events based on rareness values.
"""

import unittest
import json
import random
from pathlib import Path

# Setup path to import from project
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


class TestChildhoodEventsRandomization(unittest.TestCase):
    """Test that childhood events are selected using rareness probability."""

    def setUp(self):
        """Load childhood events data."""
        data_dir = Path(__file__).resolve().parent.parent / "data"
        with open(data_dir / "childhood_events.json", "r", encoding="utf-8") as f:
            self.childhood_events = json.load(f)

    def test_rareness_filtering_logic(self):
        """Test that events are filtered based on rareness probability."""
        events = []
        # Collect all birth events
        if "birth" in self.childhood_events:
            events.extend(self.childhood_events.get("birth", []))
        
        # Simulate 1000 iterations to check probability distribution
        random.seed(42)
        selected_counts = {}
        iterations = 1000
        
        for _ in range(iterations):
            selected = []
            for event in events:
                rareness = event.get("rareness", 0.5)
                if random.random() < rareness:
                    selected.append(event.get("event_name"))
                    selected_counts[event.get("event_name")] = selected_counts.get(event.get("event_name"), 0) + 1
        
        # Verify that events were selected
        self.assertGreater(len(selected_counts), 0, "Should have selected at least one event")
        
        # Verify selection counts roughly match rareness values (with some tolerance)
        for event in events:
            event_name = event.get("event_name")
            rareness = event.get("rareness", 0.5)
            expected_count = rareness * iterations
            actual_count = selected_counts.get(event_name, 0)
            
            # Allow ±10% tolerance
            tolerance = expected_count * 0.1
            self.assertAlmostEqual(
                actual_count, expected_count, delta=tolerance * 2,
                msg=f"{event_name}: expected ~{expected_count}, got {actual_count}"
            )

    def test_maturity_age_from_race(self):
        """Test that maturity value is correctly extracted from race data."""
        data_dir = Path(__file__).resolve().parent.parent / "data"
        with open(data_dir / "races.json", "r", encoding="utf-8") as f:
            races_data = json.load(f)
        
        for race in races_data:
            maturity = race.get("maturity")
            self.assertIsNotNone(maturity, f"{race['race_name']} should have maturity value")
            self.assertGreater(maturity, 0, f"{race['race_name']} maturity should be > 0")
            # Maturity should be reasonable (between 10 and 50)
            self.assertGreater(maturity, 10)
            self.assertLess(maturity, 50)

    def test_event_availability_by_age(self):
        """Test that different events appear based on age thresholds."""
        test_cases = [
            (0, ["birth"]),  # Age 0: only birth
            (1, ["birth"]),  # Age 1: only birth
            (2, ["birth", "age_1_2"]),  # Age 2: birth + age_1_2
            (5, ["birth", "age_1_2", "age_3_5"]),  # Age 5: birth + age_1_2 + age_3_5
            (10, ["birth", "age_1_2", "age_3_5", "age_6_10"]),  # Age 10
            (15, ["birth", "age_1_2", "age_3_5", "age_6_10", "age_11_15"]),  # Age 15
            (20, ["birth", "age_1_2", "age_3_5", "age_6_10", "age_11_15", "age_16_20"]),  # Age 20
        ]
        
        for age, expected_categories in test_cases:
            # Collect available event categories for this age
            available_categories = []
            if "birth" in self.childhood_events:
                available_categories.append("birth")
            
            if age >= 2 and "age_1_2" in self.childhood_events:
                available_categories.append("age_1_2")
            if age >= 5 and "age_3_5" in self.childhood_events:
                available_categories.append("age_3_5")
            if age >= 10 and "age_6_10" in self.childhood_events:
                available_categories.append("age_6_10")
            if age >= 15 and "age_11_15" in self.childhood_events:
                available_categories.append("age_11_15")
            if age >= 20 and "age_16_20" in self.childhood_events:
                available_categories.append("age_16_20")
            
            # Always include special events
            if "special_events" in self.childhood_events:
                available_categories.append("special_events")
            
            self.assertEqual(available_categories, expected_categories + ["special_events"],
                           f"Age {age} should have categories {expected_categories + ['special_events']}")

    def test_event_has_proper_rareness(self):
        """Test that all events have rareness values between 0 and 1."""
        for category, events in self.childhood_events.items():
            if isinstance(events, list):
                for event in events:
                    rareness = event.get("rareness")
                    self.assertIsNotNone(rareness, f"Event {event['event_name']} missing rareness")
                    self.assertGreaterEqual(rareness, 0, f"Rareness should be >= 0")
                    self.assertLessEqual(rareness, 1, f"Rareness should be <= 1")


if __name__ == "__main__":
    unittest.main(verbosity=2)
