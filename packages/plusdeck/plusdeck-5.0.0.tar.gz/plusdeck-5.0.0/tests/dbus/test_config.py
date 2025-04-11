from typing import Any, cast

import pytest

from plusdeck.config import Config, GLOBAL_FILE
from plusdeck.dbus.config import StagedConfig

cfg_cls = cast(Any, Config)


@pytest.mark.parametrize(
    "active_config,target_config",
    [
        (
            cfg_cls(file=GLOBAL_FILE, port="/dev/ttyS0"),
            cfg_cls(file=GLOBAL_FILE, port="/dev/ttyS0"),
        ),
        (
            cfg_cls(file=GLOBAL_FILE, port="/dev/ttyS0"),
            cfg_cls(file=GLOBAL_FILE, port="/dev/ttyS4"),
        ),
    ],
)
def test_staged_config_as_dict(active_config, target_config, snapshot) -> None:
    cls = cast(Any, StagedConfig)
    staged = cls(active_config=active_config, target_config=target_config)
    assert staged.as_dict() == snapshot


@pytest.mark.parametrize(
    "active_config,target_config",
    [
        (
            cfg_cls(file=GLOBAL_FILE, port="/dev/ttyS0"),
            cfg_cls(file=GLOBAL_FILE, port="/dev/ttyS0"),
        ),
        (
            cfg_cls(file=GLOBAL_FILE, port="/dev/ttyS0"),
            cfg_cls(file=GLOBAL_FILE, port="/dev/ttyS4"),
        ),
    ],
)
def test_staged_config_repr(active_config, target_config, snapshot) -> None:
    cls = cast(Any, StagedConfig)
    staged = cls(active_config=active_config, target_config=target_config)
    assert repr(staged) == snapshot
