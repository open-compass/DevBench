import pandas as pd
from stocktrends import indicators

def test_get_state():
    """
    Test case where the get_state method of the PnF class is tested. It checks if the method returns the correct state based on the given parameters.
    """
    df = pd.read_csv('unit_samples/HOOLI.csv')
    df.columns = [i.lower() for i in df.columns]
    pnf = indicators.PnF(df)
    assert pnf.get_state(True, 3) == pnf.UPTREND_CONTINUAL
    assert pnf.get_state(True, -4) == pnf.UPTREND_REVERSAL
    assert pnf.get_state(False, -2) == pnf.DOWNTREND_CONTINUAL
    assert pnf.get_state(False, 5) == pnf.DOWNTREND_REVERSAL

def test_roundit():
    """
    Test the roundit method of the PnF class. This function tests the roundit method of the PnF class by asserting the expected results for different inputs.
    """
    df = pd.read_csv('unit_samples/HOOLI.csv')
    df.columns = [i.lower() for i in df.columns]
    pnf = indicators.PnF(df)
    assert pnf.roundit(7) == 5
    assert pnf.roundit(12, base=10) == 10
    assert pnf.roundit(18, base=10) == 20
    assert pnf.roundit(23, base=5) == 25
    assert pnf.roundit(37, base=5) == 35

def test_get_bar_ohlc_data_close():
    """
    The test function that tests the get_bar_ohlc_data method of the PnF class. It checks if the method returns the correct data shape based on the given parameters.
    """
    df = pd.read_csv('unit_samples/HDFCLIFE.csv')
    df.columns = [i.lower() for i in df.columns]  
    pnf = indicators.PnF(df)
    pnf.box_size = 10
    data = pnf.get_bar_ohlc_data(source='close')
    assert data.shape == (41, 5)

def test_get_bar_ohlc_data_hl():
    """
    The test function that tests the get_bar_ohlc_data method of the PnF class. It checks if the method returns the correct data shape based on the given parameters.
    """
    df = pd.read_csv('unit_samples/HDFCLIFE.csv')
    df.columns = [i.lower() for i in df.columns]  
    pnf = indicators.PnF(df)
    pnf.box_size = 10
    data = pnf.get_bar_ohlc_data(source='hl')
    assert data.shape == (31, 5)

def test_get_ohlc_data_close():
    """
    The test function that tests the get_ohlc_data method of the PnF class. It checks if the method returns the correct data shape based on the given parameters.
    """
    df = pd.read_csv('unit_samples/HDFCLIFE.csv')
    df.columns = [i.lower() for i in df.columns]  
    pnf = indicators.PnF(df)
    pnf.box_size = 10
    data = pnf.get_ohlc_data(source='close')
    assert data.shape == (244, 6)
