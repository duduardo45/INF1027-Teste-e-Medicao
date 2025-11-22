import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from game_tester import GameTester

# Manual testing with keyboard input
with GameTester(headless=False, fps=60) as tester:
    # Setup initial game state (optional)
    tester.setup(
        level=30,
        player_x=240.0,
        player_y=258.0,
        wind_phase=1.5*3.14159
    )
    # wind_phase incurs visual bugs, but is functional

    tester.step(200)

    tester.set_wind(0.0)
    tester.set_level(30)

    # Run the game with keyboard input enabled
    # Use arrow keys to move, space to jump
    tester.run_with_input()
