import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def extract_leitos(file_path: Path) -> pd.DataFrame:
    return pd.read_csv(
        file_path,
        sep=";",
        encoding="latin1",
        low_memory=False
    )
