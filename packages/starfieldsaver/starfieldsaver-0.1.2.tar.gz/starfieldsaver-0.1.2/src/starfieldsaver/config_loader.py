from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

import toml
from polykit.paths import PolyPath
from watchdog.events import (
    DirModifiedEvent,
    DirMovedEvent,
    FileModifiedEvent,
    FileMovedEvent,
    FileSystemEventHandler,
)

if TYPE_CHECKING:
    from starfieldsaver.quicksave_utility import QuicksaveUtility

CONFIG_FILE_NAME: str = "config.toml"
CONFIG_FILE: Path = PolyPath("starfieldsaver").from_config(CONFIG_FILE_NAME)


@dataclass
class QuicksaveConfig:
    """Configuration for behavior of the quicksave utility.

    Attributes:
        save_directory: Directory where save files are stored.
        process_name: Name of the game process to monitor (without extension).
        status_check_interval: Time between status checks (in seconds).
        quicksave_every: Time between quicksaves (in seconds).
        enable_quicksave_on_interval: Whether to quicksave on the set interval.
        enable_copy_to_regular_save: Whether to copy quicksaves to regular saves.
        enable_save_cleanup: Whether to enable save cleanup.
        prune_saves_older_than: Number of days before pruning saves to one per day (0 to keep all).
        dry_run: Whether to perform a dry run of save cleanup.
        enable_sounds: Whether to play sounds on events.
        info_volume: Volume for info sounds (0.0 to 1.0).
        error_volume: Volume for error sounds (0.0 to 1.0).
        debug_log: Whether to enable debug logging.
    """

    save_directory: str
    process_name: str = "Starfield"
    status_check_interval: float = 10
    quicksave_every: float = 240
    enable_quicksave_on_interval: bool = True
    enable_copy_to_regular_save: bool = True
    enable_save_cleanup: bool = False
    prune_saves_older_than: int = 0
    dry_run: bool = True
    enable_sounds: bool = True
    info_volume: float = 0.1
    error_volume: float = 0.5
    debug_log: bool = False
    extra_config: dict[str, Any] = field(default_factory=dict)

    # Define the structure of the TOML file
    config_structure: ClassVar[dict[str, list[str]]] = {
        "paths": ["save_directory", "process_name"],
        "saves": [
            "status_check_interval",
            "quicksave_every",
            "enable_quicksave_on_interval",
            "enable_copy_to_regular_save",
        ],
        "cleanup": ["enable_save_cleanup", "prune_saves_older_than", "dry_run"],
        "sounds": ["enable_sounds", "info_volume", "error_volume"],
        "logging": ["debug_log"],
    }

    def __post_init__(self):
        self.extra_config = {
            k: v for k, v in self.__dict__.items() if k not in self.__annotations__
        }
        for k in self.extra_config:
            delattr(self, k)


class ConfigLoader:
    """Class for loading and saving the quicksave configuration."""

    MAX_RETRIES = 3
    RETRY_DELAY = 0.1

    @classmethod
    def load(cls) -> QuicksaveConfig:
        """Load the configuration from the TOML file or create a new one.

        Raises:
            toml.TomlDecodeError: If the configuration file is malformed.
        """
        for attempt in range(cls.MAX_RETRIES):
            try:
                if not CONFIG_FILE.exists():
                    return cls._create_default_config()
                with CONFIG_FILE.open(encoding="utf-8") as f:
                    config_data = toml.load(f)
                return cls._process_config(config_data)
            except toml.TomlDecodeError:
                if attempt < cls.MAX_RETRIES - 1:
                    time.sleep(cls.RETRY_DELAY)
                else:
                    raise
        return cls._create_default_config()

    @classmethod
    def reload(cls, current_config: QuicksaveConfig, logger: logging.Logger) -> QuicksaveConfig:
        """Reload the configuration from the TOML file."""
        try:
            new_config = cls.load()
            if current_config.debug_log != new_config.debug_log:
                cls._update_logger_level(logger, new_config.debug_log)
            logger.info("Reloaded config due to modification on disk.")
            return new_config
        except Exception as e:
            logger.warning(
                "Failed to reload config after multiple attempts: %s. Continuing with previous config.",
                str(e),
            )
            return current_config

    @staticmethod
    def _update_logger_level(logger: logging.Logger, debug_log: bool) -> None:
        new_level = logging.DEBUG if debug_log else logging.INFO
        logger.setLevel(new_level)
        for handler in logger.handlers:
            handler.setLevel(new_level)
        logger.info("Logger level updated to %s.", "debug" if debug_log else "info")

    @classmethod
    def _process_config(cls, config_data: dict[str, Any]) -> QuicksaveConfig:
        # Flatten the sectioned config
        flat_config = {}
        for section, values in config_data.items():
            if section in QuicksaveConfig.config_structure:
                flat_config |= values
            else:
                flat_config[section] = values

        known_attrs = {
            k: flat_config.pop(k) for k in QuicksaveConfig.__annotations__ if k in flat_config
        }
        config = QuicksaveConfig(**known_attrs)
        config.extra_config = flat_config

        # Check for missing attributes and add them with default values
        default_config = QuicksaveConfig(save_directory=config.save_directory)
        updated = False
        for attr, value in default_config.__dict__.items():
            if attr not in known_attrs and attr != "extra_config":
                setattr(config, attr, value)
                updated = True

        if updated:
            cls._save_config(config)

        return config

    @classmethod
    def _save_config(cls, config: QuicksaveConfig) -> None:
        config_dict = {
            section: {k: getattr(config, k) for k in keys}
            for section, keys in QuicksaveConfig.config_structure.items()
        }
        # Add any extra config items to a new section
        if config.extra_config:
            config_dict["extra"] = config.extra_config

        with CONFIG_FILE.open("w", encoding="utf-8") as f:
            toml.dump(config_dict, f)

    @classmethod
    def _create_default_config(cls) -> QuicksaveConfig:
        quicksave_folder = Path("~/Documents/My Games/Starfield/Saves").expanduser()
        config = QuicksaveConfig(str(quicksave_folder))
        cls._save_config(config)
        return config


class SaveType(Enum):
    """Enumeration of save types for Starfield."""

    QUICKSAVE = "quicksave"
    AUTOSAVE = "autosave"
    MANUAL = "manual save"

    def __str__(self):
        return self.value


class ConfigFileHandler(FileSystemEventHandler):
    """Watchdog event handler for changes to the quicksave configuration file."""

    def __init__(self, quicksave_utility: QuicksaveUtility):
        self.saver = quicksave_utility

    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent) -> None:
        """Reload the configuration when the file is modified."""
        if not event.is_directory and str(event.src_path).endswith(CONFIG_FILE_NAME):
            self.saver.reload_config()


class SaveFileHandler(FileSystemEventHandler):
    """Watchdog event handler for changes to the save directory."""

    def __init__(self, quicksave_utility: QuicksaveUtility):
        self.saver = quicksave_utility

    def on_moved(self, event: FileMovedEvent | DirMovedEvent) -> None:
        """Handle a file move in the save directory."""
        self.saver.logger.debug(
            "Move event detected: %s -> %s",
            Path(str(event.src_path)).name,
            Path(str(event.dest_path)).name,
        )

        if not event.is_directory and str(event.dest_path).endswith(".sfs"):
            if self.saver.config.enable_copy_to_regular_save:
                self.saver.new_game_save_detected(str(event.dest_path))
        else:
            self.saver.logger.debug("Moved file is not a game save, ignoring.")
