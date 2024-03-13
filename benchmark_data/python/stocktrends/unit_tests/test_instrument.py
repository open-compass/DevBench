import pandas as pd
import pytest
from stocktrends.indicators import Instrument

def test_validate_df():
    """
    This test checks whether the _validate_df method correctly validates the input DataFrame.
    """
    df = pd.DataFrame({'open': [1, 2, 3], 'high': [4, 5, 6], 'low': [7, 8, 9], 'close': [10, 11, 12]})
    instrument = Instrument(df)
    # Test when OHLC columns are present
    assert instrument._validate_df() is None
    # Test when OHLC columns are missing
    df_missing_columns = pd.DataFrame({'open': [1, 2, 3], 'high': [4, 5, 6]})
    with pytest.raises(ValueError):
        Instrument(df_missing_columns)