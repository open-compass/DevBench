import pandas as pd
from stocktrends import indicators

def test_Renko_box_periodic_close():
    """
    The test function that tests the get_ohlc_data method of the Renko class. It checks if the method returns the correct data shape based on the given parameters.
    """
    df = pd.read_csv('unit_samples/HDFCLIFE.csv')
    df.columns = [i.lower() for i in df.columns]
    renko = indicators.Renko(df)
    renko.brick_size = 20
    renko.chart_type = indicators.Renko.PERIOD_CLOSE
    data = renko.get_ohlc_data()
    assert data.shape == (84, 6)
