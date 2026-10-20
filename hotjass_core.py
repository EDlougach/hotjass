"""Compatibility alias: `hotjass_core` is `hotjass.core`.

The model layer used to be a top-level module next to the `hotjass` package
(HI-Jass, before the physics moved into its own repository). Existing code
keeps working with `from hotjass_core import HotJassModel`; new code should
use `from hotjass.core import HotJassModel`.
"""
import sys

from hotjass import core as _core

sys.modules[__name__] = _core
