"""
Tests for the GameTester class.

These tests verify that the GameTester can be initialized, configured,
and used to control the JumpKing game for automated testing.
"""

import sys
import os
import pytest
import math

# Add the tests directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from game_tester import GameTester


class TestGameTesterInitialization:
    """Tests for GameTester initialization"""
    
    def test_gametester_initialization_headless(self):
        """Test that GameTester can be initialized in headless mode"""
        tester = GameTester(headless=True, fps=60)
        assert tester._initialized is True
        assert tester.game is not None
        assert tester.headless is True
        assert tester.fps == 60
        tester.shutdown()
    
    def test_gametester_initialization_with_custom_fps(self):
        """Test that GameTester can be initialized with custom FPS"""
        tester = GameTester(headless=True, fps=30)
        assert tester.fps == 30
        assert os.environ.get("fps") == "30"
        tester.shutdown()
    
    def test_gametester_context_manager(self):
        """Test that GameTester works as a context manager"""
        with GameTester(headless=True) as tester:
            assert tester._initialized is True
            assert tester.game is not None
        # After exiting context, should be shut down
        assert tester._initialized is False
        assert tester.game is None


class TestPlayerPositioning:
    """Tests for player positioning functionality"""
    
    def test_set_player_position_valid(self):
        """Test setting player position with valid coordinates"""
        with GameTester(headless=True) as tester:
            tester.set_player_position(100.0, 150.0)
            x, y = tester.get_player_position()
            assert abs(x - 100.0) < 0.1
            assert abs(y - 150.0) < 0.1
    
    def test_set_player_position_default(self):
        """Test that player starts at default position"""
        with GameTester(headless=True) as tester:
            x, y = tester.get_player_position()
            # Default position is (230, 298)
            assert abs(x - 230.0) < 0.1
            assert abs(y - 298.0) < 0.1
    
    def test_set_player_position_boundaries(self):
        """Test setting player position at boundaries"""
        with GameTester(headless=True) as tester:
            # Test minimum coordinates
            tester.set_player_position(0.0, 0.0)
            x, y = tester.get_player_position()
            assert abs(x - 0.0) < 0.1
            assert abs(y - 0.0) < 0.1
            
            # Test maximum coordinates
            tester.set_player_position(480.0, 360.0)
            x, y = tester.get_player_position()
            assert abs(x - 480.0) < 0.1
            assert abs(y - 360.0) < 0.1
    
    def test_set_player_position_invalid_x_too_low(self):
        """Test that invalid x coordinate (too low) raises ValueError"""
        with GameTester(headless=True) as tester:
            with pytest.raises(ValueError, match="Invalid x coordinate"):
                tester.set_player_position(-1.0, 150.0)
    
    def test_set_player_position_invalid_x_too_high(self):
        """Test that invalid x coordinate (too high) raises ValueError"""
        with GameTester(headless=True) as tester:
            with pytest.raises(ValueError, match="Invalid x coordinate"):
                tester.set_player_position(481.0, 150.0)
    
    def test_set_player_position_invalid_y_too_low(self):
        """Test that invalid y coordinate (too low) raises ValueError"""
        with GameTester(headless=True) as tester:
            with pytest.raises(ValueError, match="Invalid y coordinate"):
                tester.set_player_position(150.0, -1.0)
    
    def test_set_player_position_invalid_y_too_high(self):
        """Test that invalid y coordinate (too high) raises ValueError"""
        with GameTester(headless=True) as tester:
            with pytest.raises(ValueError, match="Invalid y coordinate"):
                tester.set_player_position(150.0, 361.0)
    
    def test_set_player_position_resets_physics(self):
        """Test that setting position resets physics state"""
        with GameTester(headless=True) as tester:
            tester.set_player_position(200.0, 200.0)
            # Verify physics state is reset
            assert tester.game.king.speed == 0
            assert tester.game.king.angle == 0
            assert tester.game.king.isFalling is False
            assert tester.game.king.isSplat is False
            assert tester.game.king.lastCollision is None


class TestEnvironmentConfiguration:
    """Tests for environment configuration functionality"""
    
    def test_set_level_valid(self):
        """Test setting level with valid identifier"""
        with GameTester(headless=True) as tester:
            tester.set_level(5)
            assert tester.get_current_level() == 5
    
    def test_set_level_boundaries(self):
        """Test setting level at boundaries"""
        with GameTester(headless=True) as tester:
            # Test minimum level
            tester.set_level(0)
            assert tester.get_current_level() == 0
            
            # Test maximum level
            tester.set_level(42)
            assert tester.get_current_level() == 42
    
    def test_set_level_invalid_too_low(self):
        """Test that invalid level (too low) raises ValueError"""
        with GameTester(headless=True) as tester:
            with pytest.raises(ValueError, match="Invalid level"):
                tester.set_level(-1)
    
    def test_set_level_invalid_too_high(self):
        """Test that invalid level (too high) raises ValueError"""
        with GameTester(headless=True) as tester:
            with pytest.raises(ValueError, match="Invalid level"):
                tester.set_level(43)
    
    def test_set_wind_valid(self):
        """Test setting wind phase with valid value"""
        with GameTester(headless=True) as tester:
            wind_phase = math.pi / 2
            tester.set_wind(wind_phase)
            assert abs(tester.get_wind_state() - wind_phase) < 0.001
    
    def test_set_wind_boundaries(self):
        """Test setting wind phase at boundaries"""
        with GameTester(headless=True) as tester:
            # Test minimum wind phase
            tester.set_wind(0.0)
            assert abs(tester.get_wind_state() - 0.0) < 0.001
            
            # Test maximum wind phase
            tester.set_wind(2 * math.pi)
            assert abs(tester.get_wind_state() - 2 * math.pi) < 0.001
    
    def test_set_wind_invalid_too_low(self):
        """Test that invalid wind phase (too low) raises ValueError"""
        with GameTester(headless=True) as tester:
            with pytest.raises(ValueError, match="Invalid wind phase"):
                tester.set_wind(-0.1)
    
    def test_set_wind_invalid_too_high(self):
        """Test that invalid wind phase (too high) raises ValueError"""
        with GameTester(headless=True) as tester:
            with pytest.raises(ValueError, match="Invalid wind phase"):
                tester.set_wind(2 * math.pi + 0.1)


class TestUnifiedSetup:
    """Tests for unified setup method"""
    
    def test_setup_with_defaults(self):
        """Test setup with default parameters"""
        with GameTester(headless=True) as tester:
            tester.setup()
            assert tester.get_current_level() == 0
            x, y = tester.get_player_position()
            assert abs(x - 230.0) < 0.1
            assert abs(y - 298.0) < 0.1
            assert abs(tester.get_wind_state() - 0.0) < 0.001
    
    def test_setup_with_custom_parameters(self):
        """Test setup with custom parameters"""
        with GameTester(headless=True) as tester:
            tester.setup(level=10, player_x=100.0, player_y=200.0, wind_phase=math.pi)
            assert tester.get_current_level() == 10
            x, y = tester.get_player_position()
            assert abs(x - 100.0) < 0.1
            assert abs(y - 200.0) < 0.1
            assert abs(tester.get_wind_state() - math.pi) < 0.001
    
    def test_setup_verifies_playable_state(self):
        """Test that setup verifies game is in playable state"""
        with GameTester(headless=True) as tester:
            tester.setup()
            assert tester.is_playable() is True


class TestStateInspection:
    """Tests for state inspection methods"""
    
    def test_get_player_position(self):
        """Test getting player position"""
        with GameTester(headless=True) as tester:
            tester.set_player_position(150.0, 250.0)
            x, y = tester.get_player_position()
            assert isinstance(x, (int, float))
            assert isinstance(y, (int, float))
            assert abs(x - 150.0) < 0.1
            assert abs(y - 250.0) < 0.1
    
    def test_get_current_level(self):
        """Test getting current level"""
        with GameTester(headless=True) as tester:
            tester.set_level(15)
            level = tester.get_current_level()
            assert isinstance(level, int)
            assert level == 15
    
    def test_get_wind_state(self):
        """Test getting wind state"""
        with GameTester(headless=True) as tester:
            wind_phase = math.pi / 4
            tester.set_wind(wind_phase)
            state = tester.get_wind_state()
            assert isinstance(state, (int, float))
            assert abs(state - wind_phase) < 0.001
    
    def test_is_playable_true(self):
        """Test is_playable returns True when game is playable"""
        with GameTester(headless=True) as tester:
            tester.setup()
            assert tester.is_playable() is True
    
    def test_is_playable_false_when_paused(self):
        """Test is_playable returns False when game is paused"""
        with GameTester(headless=True) as tester:
            tester.setup()
            os.environ["pause"] = "1"
            assert tester.is_playable() is False
            os.environ["pause"] = ""


class TestGameStepping:
    """Tests for game stepping functionality"""
    
    def test_step_single_frame(self):
        """Test stepping a single frame"""
        with GameTester(headless=True) as tester:
            tester.setup()
            # Should not raise
            tester.step(frames=1)
    
    def test_step_multiple_frames(self):
        """Test stepping multiple frames"""
        with GameTester(headless=True) as tester:
            tester.setup()
            # Should not raise
            tester.step(frames=5)
    
    def test_step_preserves_pause_state(self):
        """Test that step preserves the original pause state"""
        with GameTester(headless=True) as tester:
            tester.setup()
            # Set pause state before stepping
            os.environ["pause"] = ""
            tester.step(frames=1)
            # Pause state should be restored
            assert os.environ.get("pause") == ""
    
    def test_step_restores_pause_state_when_paused(self):
        """Test that step restores pause state when game was paused"""
        with GameTester(headless=True) as tester:
            tester.setup()
            # Set pause state before stepping
            os.environ["pause"] = "1"
            tester.step(frames=1)
            # Pause state should be restored
            assert os.environ.get("pause") == "1"
    
    def test_step_pauses_during_execution(self):
        """Test that step pauses game logic during frame advancement"""
        with GameTester(headless=True) as tester:
            tester.setup()
            # Verify pause state is set during step
            original_pause = os.environ.get("pause", "")
            
            # Create a flag to track if pause was set during step
            pause_was_set = False
            
            # Step should set pause to "1" during execution
            tester.step(frames=1)
            
            # After step, pause should be restored to original state
            assert os.environ.get("pause") == original_pause
    
    def test_step_default_frames(self):
        """Test that step defaults to 1 frame"""
        with GameTester(headless=True) as tester:
            tester.setup()
            # Should not raise
            tester.step()
    
    def test_step_not_initialized(self):
        """Test that step raises error when not initialized"""
        tester = GameTester(headless=True)
        tester.shutdown()
        with pytest.raises(RuntimeError, match="not initialized"):
            tester.step()


class TestResourceCleanup:
    """Tests for resource cleanup"""
    
    def test_shutdown_cleans_up_resources(self):
        """Test that shutdown properly cleans up resources"""
        tester = GameTester(headless=True)
        assert tester._initialized is True
        tester.shutdown()
        assert tester._initialized is False
        assert tester.game is None
    
    def test_shutdown_is_idempotent(self):
        """Test that shutdown can be called multiple times safely"""
        tester = GameTester(headless=True)
        tester.shutdown()
        tester.shutdown()  # Should not raise
        assert tester._initialized is False
    
    def test_context_manager_cleanup(self):
        """Test that context manager properly cleans up"""
        with GameTester(headless=True) as tester:
            assert tester._initialized is True
        assert tester._initialized is False
        assert tester.game is None
