import pandas as pd

def validate_dataframe(data):
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Input data must be a pandas DataFrame.")
    return data

def _get_labels(x=None, y=None, xlabel=None, ylabel=None):
    """Smart default axis label resolver."""
    xlabel = xlabel or x or ""
    ylabel = ylabel or y or ""
    return xlabel, ylabel
