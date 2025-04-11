import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import qis
from enum import Enum

# analytics
from option_chain_analytics import OptionsDataDFs
from option_chain_analytics.ts_loaders import ts_data_loader_wrapper, DataSource


class UnitTests(Enum):
    PLOT_FUNDING_RATE = 1
    PLOT_MARK_VS_INDEX = 2


def run_unit_test(unit_test: UnitTests):

    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 1000)


    ticker = 'ETH'  # BTC, ETH

    options_data_dfs = OptionsDataDFs(**ts_data_loader_wrapper(ticker=ticker, data_source=DataSource.TARDIS_LOCAL))

    if unit_test == UnitTests.PLOT_FUNDING_RATE:

        daily_1h = qis.generate_dates_schedule(time_period=options_data_dfs.get_start_end_date(), freq='h')

        daily_8h = qis.generate_dates_schedule(time_period=options_data_dfs.get_start_end_date(), freq='D',
                                               hour_offset=8)

        # deribit extrapolates funding rate by 8.0
        funding_rate_1h = options_data_dfs.get_funding_rate(freq=None, is_rescale_to_one_hour=True)
        funding_rate_1 = options_data_dfs.get_funding_rate(freq='h', index=daily_1h)
        funding_rate_2 = options_data_dfs.get_funding_rate(freq='D', index=daily_8h)
        print(f"funding_rate_1=\n{funding_rate_1}")
        print(f"funding_rate_2=\n{funding_rate_2}")

        cumrates = pd.concat([funding_rate_1h.cumsum(0).rename('1h'),
                              funding_rate_1.cumsum(0).rename('H at index'),
                              funding_rate_2.cumsum(0).rename('D at index')],
                             axis=1).dropna()

        funding_rate_annual = 365.0*funding_rate_1h.resample('D').sum()

        with sns.axes_style("darkgrid"):
            fig, axs = plt.subplots(3, 1, figsize=(10, 7), tight_layout=True)
            kwargs = dict(x_date_freq='ME', legend_stats=qis.LegendStats.FIRST_AVG_LAST, framealpha=0.9)
            qis.plot_time_series(df=funding_rate_1h, title='funding_rate', ax=axs[0], **kwargs)
            qis.plot_time_series(df=funding_rate_annual, title='funding_rate_annual', ax=axs[1], **kwargs)
            qis.plot_time_series(df=cumrates, title='cum_funding_rate', ax=axs[2], **kwargs)

    elif unit_test == UnitTests.PLOT_MARK_VS_INDEX:
        ts1 = options_data_dfs.spot_data[['index_price', 'mark_price']]
        index_mark = ts1.iloc[:, 0].subtract(ts1.iloc[:, 1]).rename('index-mark')
        funding_rate = options_data_dfs.spot_data[['funding_rate']]
        df = pd.concat([index_mark, funding_rate], axis=1)
        npdf = df.iloc[:, 0].to_numpy()
        df['hue'] = np.where(npdf > 0.025/100.0, '>0', np.where(npdf < -0.025/100.0, '<0', '0'))

        qis.plot_time_series(df=index_mark)
        qis.plot_scatter(df=df.iloc[:-365, :], hue='hue', order=1)

    plt.show()


if __name__ == '__main__':

    unit_test = UnitTests.PLOT_MARK_VS_INDEX

    is_run_all_tests = False
    if is_run_all_tests:
        for unit_test in UnitTests:
            run_unit_test(unit_test=unit_test)
    else:
        run_unit_test(unit_test=unit_test)
