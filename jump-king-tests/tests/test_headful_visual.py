"""
Visual headful mode test - Run this to verify the game window opens and responds to commands.

This test file is designed to be run manually to visually verify that:
1. The game window opens when headless=False
2. Player positioning works and is visible
3. Level changes are reflected
4. Wind effects are visible

IMPORTANT: Run this test file SEPARATELY from other tests to avoid pygame driver conflicts.
Run with: python -m pytest tests/test_headful_visual.py -v -s

Do NOT run: pytest tests/  (this will mix headless and headful tests)
"""

import sys
import os
import pytest
import subprocess

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from game_tester import GameTester


# @pytest.fixture(autouse=True)
# def clean_pygame_environment():
#     """
#     Fixture to ensure pygame environment is clean before each test.
#     Removes SDL_VIDEODRIVER to allow headful mode.
#     """
#     # Remove SDL_VIDEODRIVER before test
#     os.environ.pop("SDL_VIDEODRIVER", None)
#     yield
#     # Cleanup after test
#     os.environ.pop("SDL_VIDEODRIVER", None)


class TestHeadfulVisual:
    """Visual verification tests for headful mode"""
    
    def test_01_window_opens_and_stays_visible(self):
        """
        VISUAL TEST: Verify a game window opens.
        
        Expected: A game window should appear and stay open for 3 seconds.
        You should see the JumpKing game interface.
        """
        print("\n" + "="*60)
        print("TEST 1: Window Opening")
        print("="*60)
        print("A game window should appear now...")
        print("Watch for 3 seconds to confirm the window is visible.")
        print("="*60 + "\n")
        
        with GameTester(headless=False, fps=60) as tester:
            tester.setup()
            
            # Render for 3 seconds
            for i in range(180):
                tester.step(frames=1)
                if i % 60 == 0:
                    print(f"  {i//60} second(s) elapsed...")
        
        print("✓ Window test complete\n")
    
    def test_02_player_position_visible(self):
        """
        VISUAL TEST: Verify player position changes are visible.
        
        Expected: You should see the player character move from:
        - Top-left corner (1 second)
        - Center of screen (1 second)
        - Bottom-right corner (1 second)
        """
        print("\n" + "="*60)
        print("TEST 2: Player Position Changes")
        print("="*60)
        print("Watch the player character move across the screen:")
        print("  1. Top-left corner")
        print("  2. Center of screen")
        print("  3. Bottom-right corner")
        print("="*60 + "\n")
        
        with GameTester(headless=False, fps=60) as tester:
            tester.setup()
            
            # Position 1: Top-left
            print("Moving to TOP-LEFT...")
            tester.set_player_position(50.0, 50.0)
            for i in range(60):
                tester.step(frames=1)
            x, y = tester.get_player_position()
            print(f"  Position: ({x:.1f}, {y:.1f})")
            
            # Position 2: Center
            print("Moving to CENTER...")
            tester.set_player_position(240.0, 180.0)
            for i in range(60):
                tester.step(frames=1)
            x, y = tester.get_player_position()
            print(f"  Position: ({x:.1f}, {y:.1f})")
            
            # Position 3: Bottom-right
            print("Moving to BOTTOM-RIGHT...")
            tester.set_player_position(430.0, 310.0)
            for i in range(60):
                tester.step(frames=1)
            x, y = tester.get_player_position()
            print(f"  Position: ({x:.1f}, {y:.1f})")
        
        print("✓ Position test complete\n")
    
    def test_03_level_changes_visible(self):
        """
        VISUAL TEST: Verify level changes are visible.
        
        Expected: You should see the game level change:
        - Level 0 (1 second)
        - Level 10 (1 second)
        - Level 20 (1 second)
        - Level 30 (1 second)
        """
        print("\n" + "="*60)
        print("TEST 3: Level Changes")
        print("="*60)
        print("Watch the game level change:")
        print("  Level 0 → Level 10 → Level 20 → Level 30")
        print("="*60 + "\n")
        
        with GameTester(headless=False, fps=60) as tester:
            levels = [0, 10, 20, 30]
            
            for level in levels:
                print(f"Setting level to {level}...")
                tester.set_level(level)
                tester.set_player_position(240.0, 180.0)
                
                for i in range(60):
                    tester.step(frames=1)
                
                current = tester.get_current_level()
                print(f"  Current level: {current}")
        
        print("✓ Level test complete\n")
    
    def test_04_wind_phase_changes(self):
        """
        VISUAL TEST: Verify wind phase changes are visible.
        
        Expected: You should see wind effects change as the phase changes:
        - Wind phase 0 (1 second)
        - Wind phase π/2 (1 second)
        - Wind phase π (1 second)
        - Wind phase 3π/2 (1 second)
        """
        import math
        
        print("\n" + "="*60)
        print("TEST 4: Wind Phase Changes")
        print("="*60)
        print("Watch for wind effect changes:")
        print("  Phase 0 → π/2 → π → 3π/2")
        print("="*60 + "\n")
        
        with GameTester(headless=False, fps=60) as tester:
            tester.setup()
            
            phases = [0, math.pi/2, math.pi, 3*math.pi/2]
            phase_names = ["0", "π/2", "π", "3π/2"]
            
            for phase, name in zip(phases, phase_names):
                print(f"Setting wind phase to {name}...")
                tester.set_wind(phase)
                
                for i in range(60):
                    tester.step(frames=1)
                
                current = tester.get_wind_state()
                print(f"  Current wind phase: {current:.4f}")
        
        print("✓ Wind test complete\n")
    
    def test_05_combined_setup(self):
        """
        VISUAL TEST: Verify combined setup works.
        
        Expected: Game should initialize with:
        - Level 15
        - Player at position (200, 150)
        - Wind phase at π/4
        """
        import math
        
        print("\n" + "="*60)
        print("TEST 5: Combined Setup")
        print("="*60)
        print("Setting up game with:")
        print("  Level: 15")
        print("  Player Position: (200, 150)")
        print("  Wind Phase: π/4")
        print("="*60 + "\n")
        
        with GameTester(headless=False, fps=60) as tester:
            tester.setup(
                level=15,
                player_x=200.0,
                player_y=150.0,
                wind_phase=math.pi/4
            )
            
            # Render for 3 seconds
            for i in range(180):
                tester.step(frames=1)
            
            # Verify all settings
            level = tester.get_current_level()
            x, y = tester.get_player_position()
            wind = tester.get_wind_state()
            
            print(f"Verified settings:")
            print(f"  Level: {level}")
            print(f"  Player Position: ({x:.1f}, {y:.1f})")
            print(f"  Wind Phase: {wind:.4f}")
        
        print("✓ Combined setup test complete\n")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("JUMPKING HEADFUL VISUAL TEST SUITE")
    print("="*60)
    print("\nThis test suite will open the game window and verify")
    print("that all GameTester controls work visually.")
    print("\nRun with: python -m pytest tests/test_headful_visual.py -v -s")
    print("="*60 + "\n")
