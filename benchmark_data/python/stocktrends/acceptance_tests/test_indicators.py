import pandas as pd
import numpy as np
from stocktrends.indicators import Renko, LineBreak


def test_renko():
    """
    Test the Renko indicator by comparing the close prices of the Renko chart
    generated from the input data with the expected close prices.

    The Renko chart is generated using the brick size of 4.

    Raises:
        AssertionError: If the absolute difference between the close prices of
        the generated Renko chart and the expected close prices is greater than
        1e-12.
    """
    df = pd.read_csv('acceptance_samples/HOOLI.csv')
    rdf = pd.read_csv('acceptance_samples/hooli_renko_4.csv')
    renko = Renko(df)
    renko.brick_size = 4
    cdf = renko.get_ohlc_data()
    assert np.all(np.abs(cdf['close'] - rdf['close']) <= 1e-12)

def test_linebreak():
    """
    Test the LineBreak indicator by comparing the close prices of the LineBreak chart
    generated from the input data with the expected close prices.

    The LineBreak chart is generated using the line number of 3.

    Raises:
        AssertionError: If the absolute difference between the close prices of
        the generated LineBreak chart and the expected close prices is greater than
        1e-12.
    """
    df = pd.read_csv('acceptance_samples/HOOLI.csv')
    lbdf = pd.read_csv('acceptance_samples/hooli_linebreak_3.csv')
    lb = LineBreak(df)
    lb.line_number = 3
    cdf = lb.get_ohlc_data()
    assert np.all(np.abs(cdf['close'] - lbdf['close']) <= 1e-12)
