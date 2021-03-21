import sys

from fbprophet import Prophet

sys.path.append('..')
import time
import pandas as pd
import utils
from tqdm import tqdm
from isoweek import Week
from multiprocessing import Pool, cpu_count
import numpy as np
import os


def import_data():
    try:
        print('Import CSV file.')
        df = pd.read_csv('df.csv')
    except:
        # import
        print('No CSV file found. Querying BQ...')
        query = 'SELECT Week, Year, Date, Site_ID, SKU, Sales_QTY, Turnover FROM `globus-datahub-dev.Verteiler_PoC.timeseries_sales_weekly` where Year >= 2015 and (Year <= 2019 OR (Year = 2020 AND Week <= 47)) order by sku, site_id, year, week'
        df = utils.bq_to_dataframe(
            query, verbose=True).pipe(utils.reduce_memory_usage)

        # preprocess
        df.loc[:, 'Sales_QTY'] = df.Sales_QTY.clip(lower=0)
        df.loc[:, 'Turnover'] = df.Turnover.clip(lower=0)

        # transform to Prophet's needs
        df = df.rename(columns={target_variable: "y"})
        tqdm.pandas()
        df['ds'] = df.progress_apply(lambda x: Week(x.Year, x.Week).monday().strftime(format='%Y-%m-%d'), axis=1)

        df.to_csv('df.csv', index=False)
    return df

def run_prophet(df_prophet):
    # Stop printing to console
    # https://github.com/facebook/prophet/issues/223
    with suppress_stdout_stderr():
        model = Prophet(daily_seasonality=False, yearly_seasonality=True)
        model.fit(df_prophet)
        future = model.make_future_dataframe(periods=1, include_history=False)
        forecast = model.predict(future)['yhat'].to_list()
    return forecast

class suppress_stdout_stderr(object):
    '''
    A context manager for doing a "deep suppression" of stdout and stderr in
    Python, i.e. will suppress all print, even if the print originates in a
    compiled C/Fortran sub-function.
       This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    exited (at least, I think that is why it lets exceptions through).

    '''
    def __init__(self):
        # Open a pair of null files
        self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = (os.dup(1), os.dup(2))

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)
        # Close the null files
        os.close(self.null_fds[0])
        os.close(self.null_fds[1])


if __name__ == '__main__':
    target_variable = 'Turnover'  # Either 'Turnover' or 'Sales_QTY'
    forecast_horizon = 1
    n_splits = 1  # Number of cross validation splits

    start = time.time()

    df = import_data()

    list_of_df = [
        df[['ds', 'y']] for i, df in df.sort_values(by=['ds']).groupby(['SKU', 'Site_ID'])
    ]


    # initiate a pool of workers
    pool = Pool(cpu_count())

    # paralell computation of forecats
    # list of lists containing the forecasts
    results = pool.map(run_prophet, tqdm(list_of_df))

    print(f'Computation took {np.round((time.time() - start) / 60, 2)} minutes in total.')
    print(f'Computation took {np.round((time.time() - start) / df.shape[0], 2)} seconds per item.')
