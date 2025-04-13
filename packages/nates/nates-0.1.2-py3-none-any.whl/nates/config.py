from pathlib import Path

from .configuration import Config
from .utils import BASE_DIR

env = Config(
    path=Path.home() / ".cache" / "nates" / "config.json",
    keys=[
        dict(
            name="DATA_DIR",
            key_type="str",
            description="\nConfigure data\n",
            default=str((BASE_DIR.parent / "data").resolve()),
            group="data",
        ),
        dict(
            name="PYPI_TOKEN",
            key_type="str",
            description="\nConfigure Pypi\n",
            default=None,
            mask=True,
            group="pypi",
        ),
    ],
)
