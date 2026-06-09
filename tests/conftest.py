from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

def load_data(filename: str) -> pd.DataFrame:
    return pd.read_csv(BASE_DIR / "datasets" / filename)