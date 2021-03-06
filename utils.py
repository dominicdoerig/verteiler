import os
from google.cloud import bigquery
from google.cloud import bigquery_storage
import datetime
import pandas as pd
from sklearn.preprocessing import LabelEncoder


def get_project_root():
    """
    Returns the root directory of the project
    :return: Root directory (str)
    """
    return os.path.dirname(os.path.realpath(__file__))


def bq_to_dataframe(query_string, verbose=False):  # -> pd.DataFrame
    """
    Queries Google Bigquery and save the results in a Pandas DataFrame
    :param query_string: Query to be executed (str)
    :param verbose: Whether or not the query duration should be printed (boolean, default: False)
    :return: Query results (Pandas.DataFrame)
    """
    start = datetime.datetime.now()

    bqclient = bigquery.Client()
    bqstorageclient = bigquery_storage.BigQueryReadClient()

    dataframe = (
        bqclient.query(query_string)
            .result()
            .to_dataframe(bqstorage_client=bqstorageclient)
    )
    end = datetime.datetime.now()

    if verbose:
        print('********************')
        print('Query Duration: ', end - start)
    return dataframe


def reduce_memory_usage(df, verbose=True):
    """
    Reduce the required memory of a dataframe by downcasting the numerical data types
    :param df: pandas.DataFrame to be converted
    :param verbose: Whether of not the compression rate should be printed (boolean, default: True)
    :return: pandas.DataFrame with downcasted data types
    """
    start_mem = df.memory_usage().sum() / 1024 ** 2

    # getting columns names with int and float dtypes
    float_cols = df.select_dtypes(include=['float']).columns
    int_cols = df.select_dtypes(include=['integer']).columns

    # donwcasting the values
    for col in float_cols:
        df[col] = pd.to_numeric(df[col], downcast='float')
    for col in int_cols:
        df[col] = pd.to_numeric(df[col], downcast='integer')

    end_mem = df.memory_usage().sum() / 1024 ** 2
    if verbose:
        print(
            "Mem. usage decreased to {:5.2f} Mb ({:.1f}% reduction)".format(
                end_mem, 100 * (start_mem - end_mem) / start_mem
            )
        )
    return df


def get_splits(df: pd.core.frame.DataFrame, fh: int = 2, n_splits: int = 5) -> list:
    """
    Get splits for time-series cross validation.
    Generate index to split data into training and test set.
    The returned index (Year, Week) represents the end of the training data.

    :param df: DataFrame to be splitted (must contain columns 'Year' and 'Week')
    :param fh: Forecast horizon (int, min: 1, default: 2)
    :param n_splits: Number of splits (int, min: 1, default: 5)
    :return list of tuples (Week & Year) representing the end of the training period , 
            Example: [(51, 2020), (49, 2020)]
    """
    if not n_splits >= 1:
        raise ValueError("Parameter 'n_Splits' must be at least 1.")
    if not fh >= 1:
        raise ValueError("Parameter 'fh' must be at least 1.")

    splits = []

    calendar_weeks = [tuple(x) for x in df[['Week', 'Year']
                                           ].drop_duplicates().to_records(index=False)]
    calendar_weeks.sort(key=lambda tup: tup[1])  # sort list of tuples
    for i in range(n_splits):
        splits.append(calendar_weeks[-(1+fh+fh*i)])
    return splits


def encode_categorical(df, cols, return_encoders = False, downcast_cols=False):
    """
    Encode categorical labels with value between 0 and n_classes-1 using LabelEncoder from Sklearn
    :param df: pandas.DataFrame to be tranformed
    :param cols: List of columns to be encoded
    :param return_encoders: wheter or not a dict containing the LabelEncoders should be returned (default: False)
    :param downcast_cols: Whether or not the numerical data types should be downcasted (default: False)
    :return: pandas.DataFrame with encoded labels, dictionary with fitted encoders {'Column Name': LabelEncoder()} (optional)
    """
    encoders = {}
    for col in cols:
        encoder = LabelEncoder()
        df[col] = encoder.fit_transform(df[col])
        encoders[col] = encoder

    if downcast_cols:
        df = reduce_memory_usage(df)
        
    return df, encoders if return_encoders else df
    

def decode_categorical(df, encoders, downcast_cols=False):
    """
    Decodes categorical labels given a LabelEncoder
    :param df: pandas.DataFrame to be tranformed
    :param encoders: dictionary with fitted encoders,  {'Column Name': LabelEncoder()} 
    :param downcast_cols: Whether or not the numerical data types should be downcasted (default: False)
    :return: pandas.DataFrame with decoded labels
    """
    for col,encoder in encoders.items():
        if col in df:
            df[col] = encoder.inverse_transform(df[col])
        
    if downcast_cols:
        df = reduce_memory_usage(df)
        
    return df

