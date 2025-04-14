import configparser
import os
import threading
import logging
from contextlib import contextmanager
from typing import Optional, Any, Dict

from dyncfg.section import Section

logger = logging.getLogger(__name__)


class DynamicConfig:
    """A class to manage dynamic configuration settings using an INI file."""

    def __init__(self, filename: Optional[str], default_section: str = "Default", auto_write: bool = True, **kwargs):

        self.filename = filename
        self.default_section = default_section
        self.auto_write = auto_write if filename is not None else False
        self.config = configparser.ConfigParser()
        self._lock = threading.RLock()
        self._overrides = threading.local()
        self._overrides.stack = []

        if self.filename is not None and not kwargs.get('_from_setstate_', False):
            self._read_config()
        elif self.filename is None:
            if not self.config.has_section(self.default_section):
                try:
                    self.config.add_section(self.default_section)
                except Exception as e:
                    logger.error(f"Failed to add default section '{self.default_section}' during init: {e}")

    def _read_config(self):
        """Reads configuration from the file, protected by the lock."""
        if self.filename is None:
            logger.debug("Skipping read_config as filename is None.")
            return
        with self._lock:
            try:
                if os.path.exists(self.filename):
                    if not hasattr(self, 'config'):
                        self.config = configparser.ConfigParser()
                    self.config.read(self.filename, encoding="utf-8")
                    logger.debug(f"Read config from {self.filename}")
                else:
                    logger.warning(f"Config file '{self.filename}' not found. Using empty/default config.")
                    if not hasattr(self, 'config'):
                        self.config = configparser.ConfigParser()
                    if not self.config.has_section(self.default_section):
                        self.config.add_section(self.default_section)

                    try:
                        with open(self.filename, "w", encoding="utf-8") as f:
                            pass
                    except IOError as e:
                        logger.error(f"Could not create empty config file {self.filename}: {e}")

            except Exception as e:
                logger.error(f"Error reading config file '{self.filename}': {e}")
                if not hasattr(self, 'config'):
                    self.config = configparser.ConfigParser()
                if not self.config.has_section(self.default_section):
                    try:
                        self.config.add_section(self.default_section)
                    except Exception:
                        pass  # Avoid error loop

    def _write_config(self):
        """Writes current configuration state to file, protected by the lock."""
        if self.filename is None:
            logger.debug("Skipping write_config as filename is None.")
            return
        with self._lock:
            try:
                if not hasattr(self, 'config'):
                    logger.error("Config object missing, cannot write.")
                    return
                parent_dir = os.path.dirname(self.filename)
                if parent_dir and not os.path.exists(parent_dir):
                    os.makedirs(parent_dir, exist_ok=True)
                    logger.debug(f"Created directory {parent_dir} for config file.")

                with open(self.filename, "w", encoding="utf-8") as configfile:
                    self.config.write(configfile)
            except Exception as e:
                logger.error(f"Error writing config file '{self.filename}': {e}")

    def save(self):
        """Manually save current configuration state to the file."""
        if self.filename is None:
            logger.warning("Cannot save configuration as no filename is associated.")
            return
        self._write_config()

    def reload(self):
        """Reload the configuration from the file."""
        if self.filename is None:
            logger.warning("Cannot reload configuration as no filename is associated.")
            return
        logger.info(f"Reloading configuration from {self.filename}")
        self._read_config()

    def ensure_section(self, section: str):
        """Ensures a section exists, creating it if necessary."""
        needs_write = False
        with self._lock:
            if not self.config.has_section(section):
                self.config.add_section(section)
                logger.debug(f"Added section '{section}'")
                needs_write = True

            if needs_write and self.auto_write:
                self._write_config()

    def remove_key(self, section: str, key: str):
        """Remove a key from a given section."""
        removed = False
        with self._lock:
            if self.config.has_option(section, key):
                removed = self.config.remove_option(section, key)
                logger.debug(f"Removed key '{key}' from section '{section}': {removed}")

            if removed and self.auto_write:
                self._write_config()

    def remove_section(self, section: str):
        """Remove an entire section."""
        removed = False
        with self._lock:
            if self.config.has_section(section):
                removed = self.config.remove_section(section)
                logger.debug(f"Removed section '{section}': {removed}")

            if removed and self.auto_write:
                self._write_config()

    def update_section(self, section: str, data: dict):
        """Batch update keys in a section from a dictionary."""
        updated = False
        with self._lock:
            if not self.config.has_section(section):
                self.config.add_section(section)
                updated = True  # Section creation counts as an update

            for key, value in data.items():
                str_value = str(value)
                if not self.config.has_option(section, key) or self.config.get(section, key) != str_value:
                    self.config.set(section, key, str_value)
                    updated = True

            if updated:
                logger.debug(f"Updated section '{section}' with {len(data)} keys.")
                if self.auto_write:
                    self._write_config()

    # Helper method to get a value, checking overrides then base config
    # Used by Section class and __getattr__
    def _get_value(self, section: str, key: str, fallback: Any = None) -> Any:
        """Internal helper to get a value, checking overrides then base config."""
        value = fallback  # Start with fallback
        value_found = False

        # 1. Check overrides (thread-local, no lock needed for _overrides itself)
        override_value = self._get_override(section, key)
        if override_value is not None:
            value = override_value
            value_found = True

        # 2. Check base config if no override found (use lock)
        if not value_found:
            with self._lock:
                if self.config.has_option(section, key):
                    # Values from ConfigParser are always strings
                    value = self.config.get(section, key)
                    value_found = True

        # Raise error if not found and no fallback was provided
        if not value_found and fallback is None:
            # Check if section itself exists to give better error
            section_exists_in_base = False
            with self._lock:
                section_exists_in_base = self.config.has_section(section)
            section_exists_in_overrides = any(
                s == section for lyr in getattr(self._overrides, "stack", []) for s, k in lyr.keys())

            if not section_exists_in_base and not section_exists_in_overrides:
                raise KeyError(f"Section '{section}' not found.")
            # If section exists but key doesn't
            raise KeyError(f"Key '{key}' not found in section '{section}'.")

        return value

    # Helper method to set a value
    # Used by Section class and __setattr__
    def _set_value(self, section: str, key: str, value: Any):
        """Internal helper to set a value in the base config. Does not affect overrides."""
        needs_write = False
        with self._lock:
            # Ensure section exists first without triggering write yet
            section_existed = self.config.has_section(section)
            if not section_existed:
                self.config.add_section(section)
                needs_write = True  # Section creation requires write

            str_value = str(value)
            # Check if value actually changed before setting
            if not self.config.has_option(section, key) or self.config.get(section, key) != str_value:
                self.config.set(section, key, str_value)
                logger.debug(f"Set config [{section}][{key}] = {str_value}")
                needs_write = True  # Value change requires write

        # Perform write outside the main lock if needed
        if needs_write and self.auto_write:
            self._write_config()

    def get_section(self, section: str) -> Section:
        """Return a Section object for the given section name."""
        self.ensure_section(section)
        return Section(self, section)

    def _get_override(self, section: str, key: str) -> Optional[Any]:
        """Checks override stack for a value."""
        stack = getattr(self._overrides, "stack", [])
        for layer in reversed(stack):
            if (section, key) in layer:
                return layer[(section, key)]
        return None

    @contextmanager
    def temporary_override(self, overrides: dict = None, **kwargs):
        """
        Temporarily override configuration values using a flexible syntax.

        Overrides can be provided as a nested dictionary or as keyword arguments.
        This only affects the current thread in the current process.
        """
        # Check if override mechanism is available
        if not hasattr(self, '_overrides') or self._overrides is None:
            logger.warning("Temporary override mechanism not available in this context.")
            yield self  # Still yield self for consistent 'with...as' usage
            return

        flat_overrides = {}
        # Process nested dictionary syntax
        if overrides is not None:
            for section, subdict in overrides.items():
                if isinstance(subdict, dict):
                    for key, value in subdict.items():
                        flat_overrides[(section, key)] = value
                else:
                    flat_overrides[(self.default_section, section)] = subdict

        # Process keyword arguments syntax (e.g., section__key='value')
        for composite_key, value in kwargs.items():
            if '__' in composite_key:
                section, key = composite_key.split('__', 1)
            elif '.' in composite_key:  # Allow dot as well
                section, key = composite_key.split('.', 1)
            else:  # No delimiter means default section
                section, key = self.default_section, composite_key
            flat_overrides[(section, key)] = value

        # Ensure stack exists on thread-local object
        if not hasattr(self._overrides, "stack"):
            self._overrides.stack = []

        # Push the current override layer onto the stack
        self._overrides.stack.append(flat_overrides)
        logger.debug(f"Entered override context, stack depth: {len(self._overrides.stack)}")
        try:
            # Yield self to allow usage like 'with cfg.temporary_override(...) as cfg_override:'
            yield self
        finally:
            # Pop the override layer off the stack on exit
            if hasattr(self._overrides, "stack") and self._overrides.stack:  # Check stack exists and is not empty
                try:
                    self._overrides.stack.pop()
                    logger.debug(f"Exited override context, stack depth: {len(self._overrides.stack)}")
                except IndexError:
                    logger.warning("Override stack was empty when trying to pop.")
            else:
                logger.warning("Override stack was empty or missing on exit from context.")

    def clear_overrides(self):
        """Clear all active temporary overrides (forcibly resets the override stack)."""
        if hasattr(self._overrides, "stack"):
            self._overrides.stack.clear()

    def __getitem__(self, section: str) -> Section:
        """Allow dictionary-style access for sections."""
        self.ensure_section(section)
        return self.get_section(section)

    def __getattr__(self, key: str) -> Any:
        """Allow attribute-style access for keys in the default section."""

        if key.startswith("_"):
             raise AttributeError(f"'{type(self).__name__}' object has no attribute '{key}'")
        try:
            # Use internal helper which checks overrides then base config
            return self._get_value(self.default_section, key)
        except KeyError as e: # Convert KeyError from _get_value to AttributeError
            # Provide a more specific error message
            raise AttributeError(f"Configuration key '{key}' not found in default section '{self.default_section}'. Original error: {e}")


    def __setattr__(self, name: str, value: Any):
        """Allow attribute-style setting for keys in the default section."""

        if name.startswith("_") or name in ("filename", "default_section", "config", "auto_write"):
             super().__setattr__(name, value)
             return

        # Check if it's trying to overwrite an existing method or attribute that isn't config
        try:
            # Use object.__getattribute__ to bypass our custom __getattr__
            current_attr = object.__getattribute__(self, name)
            if callable(current_attr) or not isinstance(current_attr, (str, int, float, bool, list, dict, type(None))):
                 # If it's callable (method) or some other complex type, use default behavior
                 super().__setattr__(name, value)
                 return

            super().__setattr__(name, value)
            return

        except AttributeError:
             # Attribute doesn't exist, treat it as a config key for the default section
             try:
                 self._set_value(self.default_section, name, value)
             except Exception as e:
                 # Fallback to default behavior if _set_value fails unexpectedly
                 logger.error(f"Failed to set config value via __setattr__ for '{name}': {e}")
                 super().__setattr__(name, value)

    def to_dict(self, include_overrides: bool = True) -> Dict[str, Dict[str, Any]]:
        """
        Exports the effective configuration state to a nested dictionary.
        Designed to create pickleable snapshots for multiprocessing.

        Args:
            include_overrides (bool): If True (default), incorporates active
                                      temporary overrides into the exported dict.
                                      If False, exports only the base configuration
                                      from the file.

        Returns:
            Dict[str, Dict[str, Any]]:
              A nested dictionary representing the configuration.
              Keys are sections, values are dictionaries of key-value pairs.
              Values will have the type they have in the override stack or
              will be strings if taken from the base config file.
        """
        # Lock ensures atomic read of config and consistent check against overrides
        with self._lock:
            effective_config: Dict[str, Dict[str, Any]] = {}
            base_sections = set(self.config.sections())
            override_sections = set()
            override_keys_by_section: Dict[str, set] = {}

            # Collect all sections and keys involved in active overrides (if requested)
            current_override_stack = getattr(self._overrides, "stack", []) if include_overrides else []
            if include_overrides and current_override_stack:
                # Store all unique tuples seen in the stack for easier lookup later
                all_override_tuples = set()
                for layer in current_override_stack:
                    all_override_tuples.update(layer.keys())

                for section, key in all_override_tuples:
                    override_sections.add(section)
                    override_keys_by_section.setdefault(section, set()).add(key)

            all_sections = base_sections.union(override_sections)

            for section in all_sections:
                current_section_dict: Dict[str, Any] = {}
                # Get keys from base config safely
                base_keys = set(self.config.options(section)) if section in base_sections else set()
                # Get keys relevant to this section from overrides
                override_keys = override_keys_by_section.get(section, set())
                # Combine all unique keys for this section
                all_keys = base_keys.union(override_keys)

                for key in all_keys:
                    value: Any = None
                    value_found = False

                    # 1. Check overrides first (if requested)
                    if include_overrides:
                        override_value = self._get_override(section, key)  # Checks the whole stack
                        if override_value is not None:
                            value = override_value  # Keep original type from override
                            value_found = True

                    # 2. If no *active* override found, check base config
                    if not value_found:
                        if self.config.has_option(section, key):
                            # Values from ConfigParser are always strings
                            value = self.config.get(section, key)
                            value_found = True

                    # Add to dict only if a value was found from either source
                    if value_found:
                        current_section_dict[key] = value

                # Add section dict to result only if it contains values
                if current_section_dict:
                    effective_config[section] = current_section_dict

            logger.debug(
                f"Exported config to dict. Sections: {len(effective_config)}. Include overrides: {include_overrides}")
            return effective_config

    def from_dict(self, config_data: Dict[str, Dict[str, Any]]):
        """
        Populates the internal ConfigParser from a nested dictionary.

        Clears existing configuration in self.config before loading.
        Does NOT automatically save changes (call save() manually if needed).
        Uses instance lock for thread safety during modification.

        Args:
            config_data (Dict[str, Dict[str, Any]]):
              A nested dictionary where keys are sections
              and values are dictionaries of key-value pairs.
        """
        with self._lock:
            self.config = configparser.ConfigParser()
            loaded_sections = 0
            loaded_keys = 0

            for section, items_dict in config_data.items():
                # Ensure the value is actually a dictionary
                if not isinstance(items_dict, dict):
                    logger.warning(f"Value for section '{section}' in from_dict input is not a dictionary, skipping.")
                    continue

                # Ensure section exists before adding items
                if not self.config.has_section(section):
                    try:
                        self.config.add_section(section)
                        loaded_sections += 1
                    except (ValueError, TypeError) as e:  # Catch invalid section names etc.
                        logger.error(f"Could not add section '{section}': {e}")
                        continue  # Skip this section

                for key, value in items_dict.items():
                    try:
                        # ConfigParser requires values to be strings
                        self.config.set(section, key, str(value))
                        loaded_keys += 1
                    except Exception as e:  # Catch errors during set (e.g., invalid key)
                        logger.error(f"Could not set key '{key}' in section '{section}': {e}")

            logger.debug(f"Loaded config from dict: {loaded_sections} sections, {loaded_keys} keys.")
            # Note: This method does not trigger auto_write.

    @classmethod
    def create_from_dict(cls, config_data: Dict[str, Dict[str, Any]], default_section: str = "Default"):
        """
        Creates a new DynamicConfig instance populated from a dictionary.

        The created instance is detached from any file (filename=None) and
        has auto_write set to False. It initializes its own real RLock for
        potential intra-instance thread safety and non-functional overrides.
        Suitable for use in worker processes.

        Args:
            config_data (dict): The nested dictionary to load configuration from.
            default_section (str): The default section name for the new instance.

        Returns:
            DynamicConfig: A new instance populated with the provided data.
        """
        # Step 1: Create instance detached from file, disable auto_write
        # __init__ will create the real RLock and initialize empty config/overrides
        instance = cls(filename=None, default_section=default_section, auto_write=False)

        # Step 2: Populate self.config using the instance method `from_dict`
        # This method uses the instance's lock (created in __init__) correctly.
        try:
            instance.from_dict(config_data)
        except Exception as e:
            # Log error during population but return the instance anyway
            logger.error(f"Error populating config during create_from_dict: {e}")


        # Overrides are initialized by __init__, no further action needed here.
        # They will be thread-local within the worker if used.

        logger.debug("Created DynamicConfig instance from dict.")
        return instance
