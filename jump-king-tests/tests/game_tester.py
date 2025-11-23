"""
GameTester - A utility class for programmatically controlling the JumpKing game.

This module provides a unified interface for initializing the game, positioning
the player character, configuring the game environment, and inspecting game state
for automated testing scenarios.
"""

import os
import sys
import math
import pygame


class GameTester:
    """
    A test utility class that provides complete control over the JumpKing game state.
    
    This class wraps the JumpKing game instance and provides methods for:
    - Initializing the game in a testable state
    - Positioning the player character at specific coordinates
    - Configuring the game environment (level, wind, etc.)
    - Inspecting game state
    - Stepping through game frames
    - Cleaning up resources
    
    Can be used as a context manager for automatic resource cleanup.
    """
    
    def __init__(self, headless: bool = False, fps: int = 60):
        """
        Initialize the GameTester and launch the JumpKing game.
        
        Args:
            headless: If True, run pygame in headless mode for CI/CD environments.
                     Uses SDL_VIDEODRIVER=dummy to avoid display requirements.
            fps: Target frame rate for game execution (default: 60)
            
        Raises:
            RuntimeError: If game initialization fails
        """
        self._initialized = False
        self.headless = headless
        self.fps = fps
        self.game = None
        
        try:
            # Set headless mode BEFORE any pygame operations
            if headless:
                os.environ["SDL_VIDEODRIVER"] = "dummy"
            else:
                # Ensure we're NOT in headless mode if headless=False
                os.environ.pop("SDL_VIDEODRIVER", None)
            
            # Configure environment variables before game initialization
            self._configure_environment(fps, headless)
            
            # Import and initialize the game
            self._initialize_game()
            
            self._initialized = True
        except Exception as e:
            self.shutdown()
            raise RuntimeError(f"Failed to initialize GameTester: {e}") from e
    
    def _configure_environment(self, fps: int, headless: bool) -> None:
        """
        Configure environment variables to set up the game for testing.
        
        This method sets up environment variables that the JumpKing game reads
        to configure its behavior, including bypassing menus and starting screens.
        
        Note: SDL_VIDEODRIVER is set in __init__ before pygame initialization.
        
        Args:
            fps: Frame rate to set
            headless: Whether to use headless mode (for reference only)
        """
        # Set frame rate
        os.environ["fps"] = str(fps)
        
        # Bypass menus and start screens
        os.environ["gaming"] = "1"      # Skip to game state
        os.environ["start"] = "1"       # Skip start screen
        os.environ["active"] = "1"      # Player is active
        os.environ["pause"] = ""        # Game is not paused
    
    def _initialize_game(self) -> None:
        """
        Import and initialize the JumpKing game instance.
        
        This method adds the JumpKingAtHome submodule to the Python path,
        imports the JKGame class, and creates a game instance.
        
        Raises:
            ImportError: If the JumpKingAtHome module cannot be imported
            RuntimeError: If pygame initialization fails
        """
        # Add JumpKingAtHome submodule to Python path
        submodule_path = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'JumpKingAtHome'
        )
        
        if not os.path.exists(submodule_path):
            raise RuntimeError(f"JumpKingAtHome submodule not found at {submodule_path}")
        
        sys.path.insert(0, submodule_path)
        
        # Save current working directory
        original_cwd = os.getcwd()
        
        try:
            # Change to JumpKingAtHome directory so relative paths work
            os.chdir(submodule_path)
            
            # Import the game class
            from JumpKing import JKGame
            
            # Initialize pygame (if not already initialized)
            if not pygame.get_init():
                pygame.init()
            
            # Create game instance with infinite max steps for testing
            self.game = JKGame(max_step=float('inf'))
            
            # Re-apply environment configuration after game initialization
            # (game initialization may have modified environment variables)
            self._configure_environment(self.fps, self.headless)
            
        except ImportError as e:
            raise ImportError(f"Failed to import JumpKing module: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Failed to initialize JKGame: {e}") from e
        finally:
            # Restore original working directory
            os.chdir(original_cwd)
    
    # ========== Parameter Validation Helpers ==========
    
    def _validate_x_coordinate(self, x: float) -> None:
        """
        Validate that an x coordinate is within valid range.
        
        Args:
            x: X coordinate to validate
            
        Raises:
            ValueError: If x is outside the valid range (0-480)
        """
        if not (0 <= x <= 480):
            raise ValueError(f"Invalid x coordinate: {x}. Must be 0-480")
    
    def _validate_y_coordinate(self, y: float) -> None:
        """
        Validate that a y coordinate is within valid range.
        
        Args:
            y: Y coordinate to validate
            
        Raises:
            ValueError: If y is outside the valid range (0-360)
        """
        if not (0 <= y <= 360):
            raise ValueError(f"Invalid y coordinate: {y}. Must be 0-360")
    
    def _validate_coordinates(self, x: float, y: float) -> None:
        """
        Validate that both x and y coordinates are within valid ranges.
        
        Args:
            x: X coordinate to validate (valid range: 0-480)
            y: Y coordinate to validate (valid range: 0-360)
            
        Raises:
            ValueError: If either coordinate is outside valid range
        """
        self._validate_x_coordinate(x)
        self._validate_y_coordinate(y)
    
    def _validate_level(self, level: int) -> None:
        """
        Validate that a level identifier is within valid range.
        
        Args:
            level: Level identifier to validate
            
        Raises:
            ValueError: If level is outside the valid range (0-42)
        """
        if not (0 <= level <= 42):
            raise ValueError(f"Invalid level: {level}. Must be 0-42")
    
    def _validate_wind_phase(self, wind_phase: float) -> None:
        """
        Validate that a wind phase value is within valid range.
        
        Args:
            wind_phase: Wind phase value to validate
            
        Raises:
            ValueError: If wind_phase is outside the valid range (0 to 2π)
        """
        if not (0 <= wind_phase <= 2 * math.pi):
            raise ValueError(
                f"Invalid wind phase: {wind_phase}. Must be 0 to 2π (0 to {2 * math.pi})"
            )
    
    def set_player_position(self, x: float, y: float) -> None:
        """
        Set the player character at specific coordinates.
        
        This method directly manipulates the King object's position attributes
        and resets physics state to ensure the player is in a stable state at
        the specified position.
        
        Args:
            x: Player x coordinate (valid range: 0-480)
            y: Player y coordinate (valid range: 0-360)
            
        Raises:
            ValueError: If coordinates are outside valid range
            RuntimeError: If game is not initialized
        """
        if not self._initialized or self.game is None:
            raise RuntimeError("GameTester is not initialized")
        
        # Validate coordinates using helper methods
        self._validate_coordinates(x, y)
        
        # Set player position
        # Account for rect offsets used by the game
        self.game.king.x = x
        self.game.king.y = y
        self.game.king.rect_x = x + 1
        self.game.king.rect_y = y + 7
        
        # Reset physics state for stability
        self.game.king.speed = 0
        self.game.king.angle = 0
        self.game.king.isFalling = False
        self.game.king.isSplat = False
        self.game.king.lastCollision = None
    
    def set_level(self, level: int) -> None:
        """
        Set the current game level.
        
        Args:
            level: Level identifier (valid range: 0-42)
            
        Raises:
            ValueError: If level is outside valid range
            RuntimeError: If game is not initialized
        """
        if not self._initialized or self.game is None:
            raise RuntimeError("GameTester is not initialized")
        
        # Validate level using helper method
        self._validate_level(level)
        
        # Set current level
        self.game.levels.current_level = level
    
    def set_wind(self, wind_phase: float) -> None:
        """
        Set the wind oscillation phase.
        
        The wind system in the game uses a sine wave to calculate horizontal wind force.
        The wind_var is the phase of the sine wave, and wind.x accumulates the integrated
        wind displacement over time. When setting wind_var to an arbitrary value, we need
        to recalculate wind.x to match, otherwise the visual weather effect desynchronizes.
        
        Args:
            wind_phase: Wind phase value (valid range: 0.0 to 2π)
            
        Raises:
            ValueError: If wind_phase is outside valid range
            RuntimeError: If game is not initialized
        """
        if not self._initialized or self.game is None:
            raise RuntimeError("GameTester is not initialized")
        
        # Validate wind phase using helper method
        self._validate_wind_phase(wind_phase)
        
        # Set wind phase
        self.game.levels.wind.wind_var = wind_phase
        
        # Recalculate wind.x to match the new phase
        # The wind displacement is the integral of sin(wind_var) * 6.25
        # Integral of sin(x) is -cos(x), so we use -cos(wind_var) * 6.25
        # This keeps the visual weather effect synchronized with the wind phase
        self.game.levels.wind.x = -math.cos(wind_phase) * (2.5 ** 2)
    
    def setup(
        self,
        level: int = 0,
        player_x: float = 230.0,
        player_y: float = 298.0,
        wind_phase: float = 0.0
    ) -> None:
        """
        Configure the complete game environment in a single call.
        
        This method sets up the game by calling set_level, set_player_position,
        and set_wind in the correct order, ensuring all game systems are
        initialized and ready for testing.
        
        Args:
            level: Level identifier (default: 0, valid range: 0-42)
            player_x: Player x coordinate (default: 230.0, valid range: 0-480)
            player_y: Player y coordinate (default: 298.0, valid range: 0-360)
            wind_phase: Wind phase value (default: 0.0, valid range: 0.0 to 2π)
            
        Raises:
            ValueError: If any parameter is outside valid range
            RuntimeError: If game is not initialized
        """
        if not self._initialized or self.game is None:
            raise RuntimeError("GameTester is not initialized")
        
        # Apply configuration in correct order
        self.set_level(level)
        self.set_player_position(player_x, player_y)
        self.set_wind(wind_phase)
        
        # Verify game is in playable state
        self._ensure_playable_state()
    
    def _ensure_playable_state(self) -> None:
        """
        Internal method to verify the game is in a playable state.
        
        Checks that environment variables are set correctly and the player
        is in a stable state.
        
        Raises:
            RuntimeError: If game is not in a playable state
        """
        if not self._initialized or self.game is None:
            raise RuntimeError("GameTester is not initialized")
        
        # Verify environment variables
        if os.environ.get("gaming") != "1":
            raise RuntimeError("Game is not in gaming state")
        if os.environ.get("active") != "1":
            raise RuntimeError("Player is not active")
        if os.environ.get("pause") != "":
            raise RuntimeError("Game is paused")
    
    def get_player_position(self) -> tuple:
        """
        Get the current player character position.
        
        Returns:
            A tuple of (x, y) coordinates representing the player's position
            
        Raises:
            RuntimeError: If game is not initialized
        """
        if not self._initialized or self.game is None:
            raise RuntimeError("GameTester is not initialized")
        
        return (self.game.king.x, self.game.king.y)
    
    def get_current_level(self) -> int:
        """
        Get the current game level identifier.
        
        Returns:
            The current level (0-42)
            
        Raises:
            RuntimeError: If game is not initialized
        """
        if not self._initialized or self.game is None:
            raise RuntimeError("GameTester is not initialized")
        
        return self.game.levels.current_level
    
    def get_wind_state(self) -> float:
        """
        Get the current wind oscillation phase.
        
        Returns:
            The current wind phase value (0.0 to 2π)
            
        Raises:
            RuntimeError: If game is not initialized
        """
        if not self._initialized or self.game is None:
            raise RuntimeError("GameTester is not initialized")
        
        return self.game.levels.wind.wind_var
    
    def is_playable(self) -> bool:
        """
        Check if the game is in a playable state.
        
        Returns:
            True if the game is playable (not in menus, not paused, player active),
            False otherwise
            
        Raises:
            RuntimeError: If game is not initialized
        """
        if not self._initialized or self.game is None:
            raise RuntimeError("GameTester is not initialized")
        
        return (
            os.environ.get("gaming") == "1" and
            os.environ.get("pause") == "" and
            os.environ.get("active") == "1" and
            not self.game.king.isFalling
        )
    
    def step(self, frames: int = 1, action: int = None) -> None:
        """
        Advance the game simulation by a specified number of frames.
        
        This method advances the game by the specified number of frames,
        running the full game loop including physics, collisions, and rendering.
        Keyboard input is ignored during stepping to allow deterministic testing.
        
        Args:
            frames: Number of frames to advance (default: 1)
            action: Optional action command to pass to game logic (default: None).
                   Valid actions: 0='right', 1='left', 2='right+space', 3='left+space'
            
        Raises:
            RuntimeError: If game is not initialized
        """
        if not self._initialized or self.game is None:
            raise RuntimeError("GameTester is not initialized")
        
        # Advance frames with full game logic but no keyboard input
        for _ in range(frames):
            self.game.clock.tick(self.game.fps)
            # Skip _check_events() to prevent keyboard input from affecting the simulation
            if not os.environ["pause"]:
                self.game._update_gamestuff(action=action)
            
            self.game._update_gamescreen()
            self.game._update_guistuff()
            # Skip audio processing in headless mode
            if not self.headless:
                self.game._update_audio()
            pygame.display.update()
    
    def run_with_input(self) -> None:
        """
        Run the game with keyboard input enabled for manual testing.
        
        This method starts the game's main loop with full keyboard input support,
        preserving any setup configuration (level, player position, wind) that
        was applied before calling this method.
        
        The working directory is automatically managed to ensure relative paths
        for game resources work correctly.
        
        Controls:
        - Arrow keys: Move left/right
        - Space: Jump
        - ESC: Pause/Menu
        
        Raises:
            RuntimeError: If game is not initialized
        """
        if not self._initialized or self.game is None:
            raise RuntimeError("GameTester is not initialized")
        
        # Save current working directory
        original_cwd = os.getcwd()
        
        try:
            # Change to JumpKingAtHome directory so relative paths work
            submodule_path = os.path.join(
                os.path.dirname(__file__), 
                '..', 
                'JumpKingAtHome'
            )
            os.chdir(submodule_path)
            
            # Run the game main loop with keyboard input
            # Note: We replicate running() but skip the reset() call to preserve setup
            while True:
                self.game.clock.tick(self.game.fps)
                self.game._check_events()
                if not os.environ["pause"]:
                    self.game._update_gamestuff()
                
                self.game._update_gamescreen()
                self.game._update_guistuff()
                self.game._update_audio()
                pygame.display.update()
        finally:
            # Restore original working directory
            os.chdir(original_cwd)
    
    def shutdown(self) -> None:
        """
        Clean shutdown of the game instance and pygame resources.
        
        This method stops all audio channels, quits pygame, and releases
        all associated resources. Safe to call multiple times.
        """
        if not self._initialized:
            return
        
        try:
            if self.game is not None:
                # Save any necessary state
                if hasattr(self.game, 'environment'):
                    self.game.environment.save()
                
                # Stop all audio channels
                if pygame.mixer.get_init():
                    for i in range(pygame.mixer.get_num_channels()):
                        try:
                            pygame.mixer.Channel(i).stop()
                        except Exception:
                            pass
            
            # Quit pygame
            if pygame.get_init():
                pygame.quit()
        except Exception:
            pass
        finally:
            self._initialized = False
            self.game = None
    
    def __enter__(self):
        """
        Context manager entry point.
        
        Returns:
            self: The GameTester instance
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit point with automatic cleanup.
        
        Args:
            exc_type: Exception type if an exception occurred
            exc_val: Exception value if an exception occurred
            exc_tb: Exception traceback if an exception occurred
        """
        self.shutdown()
