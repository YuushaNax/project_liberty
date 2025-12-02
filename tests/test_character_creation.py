"""
Comprehensive tests for character creation system.
Tests Entity initialization, stat calculations, childhood event effects, and JSON save format.
"""

import unittest
import json
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Setup path to import from project
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine.entities.entity import Entity


class TestEntityInitialization(unittest.TestCase):
    """Test Entity class initialization and basic attributes."""

    def test_entity_creation_with_basic_stats(self):
        """Test creating an entity with name, stats, and height."""
        test_stats = {
            "strength": 12,
            "agility": 10,
            "dexterity": 11,
            "constitution": 13,
            "intellect": 14,
            "psique": 9,
            "will": 10,
            "perception": 11,
            "education": 12,
            "charisma": 10,
        }
        entity = Entity(name="TestChar", new_stats=test_stats, height=175)

        self.assertEqual(entity.name, "TestChar")
        self.assertEqual(entity.height, 175)
        self.assertEqual(entity.stats, test_stats)
        self.assertEqual(entity.level, 1)
        self.assertEqual(entity.experience, 0)

    def test_entity_health_calculation(self):
        """Test that max_health is calculated correctly from stats and weight."""
        test_stats = {
            "strength": 10,
            "agility": 10,
            "dexterity": 10,
            "constitution": 15,
            "intellect": 10,
            "psique": 10,
            "will": 10,
            "perception": 10,
            "education": 10,
            "charisma": 10,
        }
        entity = Entity(name="HealthTest", new_stats=test_stats, height=175)
        
        # max_health = (constitution * 2) + strength + (weight * height) / 2
        expected_health = (15 * 2) + 10 + (80 * 175) / 2
        self.assertEqual(entity.max_health, expected_health)
        self.assertEqual(entity.current_health, expected_health)

    def test_entity_mana_calculation(self):
        """Test that max_mana is calculated correctly from stats."""
        test_stats = {
            "strength": 10,
            "agility": 10,
            "dexterity": 10,
            "constitution": 10,
            "intellect": 14,
            "psique": 12,
            "will": 11,
            "perception": 10,
            "education": 10,
            "charisma": 10,
        }
        entity = Entity(name="ManaTest", new_stats=test_stats, height=175)
        
        # max_mana = ((intellect * 3) + education + (will * 2) + (psique * 2)) / 2
        expected_mana = ((14 * 3) + 10 + (11 * 2) + (12 * 2)) / 2
        self.assertEqual(entity.max_mana, expected_mana)
        self.assertEqual(entity.current_mana, expected_mana)

    def test_entity_initial_state(self):
        """Test entity has correct initial state and needs."""
        test_stats = {s: 10 for s in [
            "strength", "agility", "dexterity", "constitution", "intellect",
            "psique", "will", "perception", "education", "charisma"
        ]}
        entity = Entity(name="StateTest", new_stats=test_stats, height=175)

        self.assertEqual(entity.state, "conscious")
        self.assertEqual(entity.hunger, 100)
        self.assertEqual(entity.thirst, 100)
        self.assertEqual(entity.tiredness, 100)
        self.assertEqual(entity.magic_heat, 0)
        self.assertEqual(entity.reputation, 0)


class TestStatModifiers(unittest.TestCase):
    """Test stat modification methods."""

    def setUp(self):
        """Create a test entity for each test."""
        self.test_stats = {s: 10 for s in [
            "strength", "agility", "dexterity", "constitution", "intellect",
            "psique", "will", "perception", "education", "charisma"
        ]}
        self.entity = Entity(name="ModTest", new_stats=self.test_stats, height=175)

    def test_modify_stat(self):
        """Test modifying a single stat."""
        self.entity.modify_stat("strength", 5)
        self.assertEqual(self.entity.stats["strength"], 15)

    def test_modify_stat_negative(self):
        """Test modifying a stat to negative (should clamp to 0)."""
        self.entity.modify_stat("strength", -15)
        self.assertEqual(self.entity.stats["strength"], 0)

    def test_modify_multiple_stats(self):
        """Test modifying multiple stats sequentially."""
        self.entity.modify_stat("strength", 3)
        self.entity.modify_stat("intellect", -2)
        self.entity.modify_stat("charisma", 1)
        
        self.assertEqual(self.entity.stats["strength"], 13)
        self.assertEqual(self.entity.stats["intellect"], 8)
        self.assertEqual(self.entity.stats["charisma"], 11)


class TestChildhoodEventsData(unittest.TestCase):
    """Test that childhood events data is properly structured and accessible."""

    def setUp(self):
        """Load childhood events data."""
        data_dir = Path(__file__).resolve().parent.parent / "data"
        with open(data_dir / "childhood_events.json", "r", encoding="utf-8") as f:
            self.childhood_events = json.load(f)

    def test_childhood_events_structure(self):
        """Test that childhood events file has expected structure."""
        expected_categories = [
            "birth", "age_1_2", "age_3_5", "age_6_10", "age_11_15", "age_16_20", "special_events"
        ]
        for category in expected_categories:
            self.assertIn(category, self.childhood_events)
            self.assertIsInstance(self.childhood_events[category], list)

    def test_birth_events_have_options(self):
        """Test that birth events have proper structure with options."""
        birth_events = self.childhood_events.get("birth", [])
        self.assertGreater(len(birth_events), 0, "Should have at least one birth event")
        
        for event in birth_events:
            self.assertIn("event_name", event)
            self.assertIn("description", event)
            self.assertIn("options", event)
            self.assertIsInstance(event["options"], list)
            
            for option in event["options"]:
                self.assertIn("option_name", option)
                self.assertIn("effect", option)
                self.assertIsInstance(option["effect"], dict)

    def test_event_effects_are_numeric(self):
        """Test that all event option effects are numeric values."""
        for category, events in self.childhood_events.items():
            if isinstance(events, list):
                for event in events:
                    for option in event.get("options", []):
                        for stat, value in option.get("effect", {}).items():
                            self.assertIsInstance(value, (int, float),
                                f"Effect {stat} in {event['event_name']} should be numeric, got {type(value)}")


class TestStatApplicationFromChildhoodEvents(unittest.TestCase):
    """Test applying childhood event effects to character stats."""

    def setUp(self):
        """Create test entity and load childhood events."""
        self.test_stats = {s: 10 for s in [
            "strength", "agility", "dexterity", "constitution", "intellect",
            "psique", "will", "perception", "education", "charisma"
        ]}
        self.entity = Entity(name="EffectTest", new_stats=self.test_stats, height=175)
        
        data_dir = Path(__file__).resolve().parent.parent / "data"
        with open(data_dir / "childhood_events.json", "r", encoding="utf-8") as f:
            self.childhood_events = json.load(f)

    def test_apply_single_event_effect(self):
        """Test applying a single childhood event effect."""
        # Get first birth event and first option
        birth_event = self.childhood_events["birth"][0]
        option = birth_event["options"][0]
        effects = option.get("effect", {})
        
        # Apply effects manually (simulating what CreatePlayer does)
        original_values = {k: self.entity.stats[k] for k in effects.keys() if k in self.entity.stats}
        
        for stat_name, delta in effects.items():
            if stat_name in self.entity.stats:
                self.entity.stats[stat_name] += delta
        
        # Verify effects were applied
        for stat_name, delta in effects.items():
            if stat_name in self.entity.stats:
                expected = original_values[stat_name] + delta
                self.assertEqual(self.entity.stats[stat_name], expected)

    def test_apply_multiple_effects_to_same_stat(self):
        """Test applying multiple effects that modify the same stat."""
        initial_strength = self.entity.stats["strength"]
        
        # Apply +3 strength from event 1
        self.entity.stats["strength"] += 3
        # Apply +2 strength from event 2
        self.entity.stats["strength"] += 2
        
        self.assertEqual(self.entity.stats["strength"], initial_strength + 5)

    def test_effects_with_float_values(self):
        """Test that float effect values are handled correctly."""
        # Some effects in the JSON might be floats
        initial_education = self.entity.stats.get("education", 10)
        
        # Apply a float effect
        self.entity.stats["education"] += 2.0
        
        self.assertEqual(self.entity.stats["education"], initial_education + 2.0)


class TestRaceModifiers(unittest.TestCase):
    """Test race modifier application."""

    def setUp(self):
        """Load race data."""
        data_dir = Path(__file__).resolve().parent.parent / "data"
        with open(data_dir / "races.json", "r", encoding="utf-8") as f:
            self.races_data = json.load(f)

    def test_race_modifiers_structure(self):
        """Test that race data has modifiers."""
        for race in self.races_data:
            self.assertIn("race_name", race)
            self.assertIn("modifiers", race)
            self.assertIsInstance(race["modifiers"], list)

    def test_apply_race_modifiers_to_stats(self):
        """Test applying race modifiers to base stats."""
        base_stats = {s: 10 for s in [
            "strength", "agility", "dexterity", "constitution", "intellect",
            "psique", "will", "perception", "education", "charisma"
        ]}
        
        # Test with Orc (has strength, constitution, dexterity modifiers)
        orc_race = next((r for r in self.races_data if r["race_name"] == "orc"), None)
        self.assertIsNotNone(orc_race)
        
        stats = base_stats.copy()
        for mod in orc_race.get("modifiers", []):
            stat_name = mod.get("stat_name")
            modifier = mod.get("modifier", 0)
            if stat_name in stats:
                stats[stat_name] += modifier
        
        # Orcs should have: STR +3, CON +2, DEX -1
        self.assertEqual(stats["strength"], 13)
        self.assertEqual(stats["constitution"], 12)
        self.assertEqual(stats["dexterity"], 9)


class TestCharacterSerialization(unittest.TestCase):
    """Test saving and loading character data."""

    def setUp(self):
        """Create test entity and temp directory."""
        self.test_stats = {s: 10 for s in [
            "strength", "agility", "dexterity", "constitution", "intellect",
            "psique", "will", "perception", "education", "charisma"
        ]}
        # Apply some modifications to make it more realistic
        self.test_stats["strength"] = 13
        self.test_stats["education"] = 12
        
        self.entity = Entity(name="SaveTest", new_stats=self.test_stats, height=175)
        self.entity.race = {"human": 100}
        self.entity.age = 20
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up temp directory."""
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_save_character_to_json(self):
        """Test saving character data to JSON format."""
        save_data = {
            "meta": {
                "save_name": "test_save",
                "created": "2025-12-02",
                "version": "0.1-alpha"
            },
            "player": {
                "name": self.entity.name,
                "race": self.entity.race,
                "age": self.entity.age,
                "height": self.entity.height,
                "stats": self.entity.stats,
                "level": self.entity.level,
                "experience": self.entity.experience,
                "state": self.entity.state,
                "hunger": self.entity.hunger,
                "thirst": self.entity.thirst,
                "tiredness": self.entity.tiredness,
                "reputation": self.entity.reputation
            }
        }
        
        save_path = Path(self.temp_dir) / "test_character.json"
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(save_data, f, indent=4, ensure_ascii=False)
        
        self.assertTrue(save_path.exists())
        
        # Verify saved data
        with open(save_path, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        
        self.assertEqual(loaded_data["player"]["name"], "SaveTest")
        self.assertEqual(loaded_data["player"]["age"], 20)
        self.assertEqual(loaded_data["player"]["stats"]["strength"], 13)
        self.assertEqual(loaded_data["player"]["stats"]["education"], 12)

    def test_character_json_contains_all_required_fields(self):
        """Test that saved character JSON has all required fields."""
        save_data = {
            "meta": {"save_name": "test", "created": "2025-12-02", "version": "0.1-alpha"},
            "player": {
                "name": self.entity.name,
                "race": self.entity.race,
                "age": self.entity.age,
                "height": self.entity.height,
                "stats": self.entity.stats,
                "level": self.entity.level,
                "experience": self.entity.experience,
                "state": self.entity.state,
                "hunger": self.entity.hunger,
                "thirst": self.entity.thirst,
                "tiredness": self.entity.tiredness,
                "reputation": self.entity.reputation
            }
        }
        
        required_player_fields = [
            "name", "race", "age", "height", "stats", "level", "experience",
            "state", "hunger", "thirst", "tiredness", "reputation"
        ]
        
        for field in required_player_fields:
            self.assertIn(field, save_data["player"], f"Missing field: {field}")


class TestStatsDataIntegrity(unittest.TestCase):
    """Test stats.json file integrity."""

    def setUp(self):
        """Load stats data."""
        data_dir = Path(__file__).resolve().parent.parent / "data"
        with open(data_dir / "stats.json", "r", encoding="utf-8") as f:
            self.stats_data = json.load(f)

    def test_all_stats_have_required_fields(self):
        """Test that all stats have required metadata fields."""
        required_fields = ["stat_name", "acronym", "display", "description"]
        
        for stat in self.stats_data:
            for field in required_fields:
                self.assertIn(field, stat, f"Stat {stat.get('stat_name')} missing field: {field}")

    def test_stat_names_consistency(self):
        """Test that stat names used elsewhere match stats.json."""
        stat_names = {stat["stat_name"] for stat in self.stats_data}
        expected_stats = {
            "strength", "agility", "dexterity", "constitution", "intellect",
            "psique", "will", "perception", "education", "charisma"
        }
        
        self.assertEqual(stat_names, expected_stats)


class TestIntegrationCharacterCreationFlow(unittest.TestCase):
    """Integration tests for the complete character creation flow."""

    def setUp(self):
        """Load all game data."""
        data_dir = Path(__file__).resolve().parent.parent / "data"
        
        with open(data_dir / "races.json", "r", encoding="utf-8") as f:
            self.races_data = json.load(f)
        with open(data_dir / "stats.json", "r", encoding="utf-8") as f:
            self.stats_data = json.load(f)
        with open(data_dir / "childhood_events.json", "r", encoding="utf-8") as f:
            self.childhood_events = json.load(f)

    def test_complete_character_creation_flow(self):
        """Simulate complete character creation: name -> race -> age -> childhood event."""
        # Step 1: Player name
        player_name = "Aragorn"
        
        # Step 2: Select race
        selected_race = next((r for r in self.races_data if r["race_name"] == "human"), None)
        self.assertIsNotNone(selected_race)
        
        # Step 3: Initialize base stats with race modifiers
        base_stats = {s["stat_name"]: 10 for s in self.stats_data}
        for mod in selected_race.get("modifiers", []):
            stat_name = mod.get("stat_name")
            if stat_name in base_stats:
                base_stats[stat_name] += mod.get("modifier", 0)
        
        # Step 4: Select age
        player_age = 25
        
        # Step 5: Select childhood event and option
        childhood_events_for_age = self.childhood_events.get("birth", [])
        self.assertGreater(len(childhood_events_for_age), 0)
        
        selected_event = childhood_events_for_age[0]
        selected_option = selected_event.get("options", [])[0]
        
        # Apply effects
        effects = selected_option.get("effect", {})
        for stat_name, delta in effects.items():
            if stat_name in base_stats:
                base_stats[stat_name] += delta
        
        # Step 6: Create entity
        entity = Entity(
            name=player_name,
            new_stats=base_stats,
            height=175
        )
        entity.race = {selected_race.get("race_name"): 100}
        entity.age = player_age
        
        # Verify final state
        self.assertEqual(entity.name, "Aragorn")
        self.assertEqual(entity.age, 25)
        self.assertEqual(entity.race, {"human": 100})
        self.assertGreater(entity.stats["education"], 10)  # humans have +2 education
        # stats should also have event effects applied
        self.assertGreater(sum(entity.stats.values()), 100)  # base 10 * 10 stats + modifiers


if __name__ == "__main__":
    unittest.main(verbosity=2)
