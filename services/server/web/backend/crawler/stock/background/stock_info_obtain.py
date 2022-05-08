import yfinance as yf
import os
# import sys
from module.generate_code import createRandomCode
from pandas_datareader import data as pdr
from module.date import DateTimeTools as DT
import matplotlib.pyplot as plt
from module.handle_exception import HandleException as help
from module.log_generate import Loggings
from module.reptile import RequestPageSource
from crawler.config import Initialization as Init
import pandas as pd
# import math
from decimal import Decimal, ROUND_HALF_UP


logger = Loggings()

def write_iterator_to_log(iterator):
    [logger.info(read_iterator_info) for read_iterator_info in iterator]

def write_iterator_multiple_to_log(iterator):
    for outside_index, outside in enumerate(iterator, 1):
        logger.info(f'The {outside_index} iterator')
        logger.info('------------------------------------------------------')
        for inner_index, inner_iterator in enumerate(outside, 1):
            logger.info(f"The {inner_index} data is {inner_iterator}")
        logger.info('------------------------------------------------------')

class StockInfoObtain():
    """
        :Parameters:
            ticker : str
                Valid ticker stock company name or number: 2317.TW,FB,6758.T
            country : str
                Stock country please enter that abbreviation, example TW is Taiwan county abbreviation
            auth_user : str
                Login user
            task id : str
                Current execute task id
    """
    def __init__(self, **kwargs):
        self.__base_url = Init.base_url_list['stock']['yahoo_finance'][-1]
        self.__country = kwargs['country']
        self.__ticker = kwargs['ticker']
        self.__auth_user = kwargs['auth_user']
        self.__task_id = kwargs['task_id']
        self.__country_refre_dict = {
            'JP': '.T',
            'TW': '.TW',
            'HK': '.HK',
            'KR': '.KS',
            'UK': '.L',
            'FR': '.PA'
        }
        self.__col = ['ticker', 'username', 'task', 'trade_date',
                    'open_price', 'high_price', 'low_price',
                    'close_price', 'adj_close_price', 'volume']

    def __check_dir_is_exists(self, path):
        if os.path.exists(path) is False:
            os.makedirs(path)

    def __check_nan_exists(self, check_val):
        return str(check_val).lower().find("nan")

    def __round_down(self, f):
        return Decimal(str(f)).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

    def __regular_data(self, cols, rows):
        result = []
        for data in rows:
            format_date = DT.format_date_str(data[0].to_pydatetime().date())
            temp = list(data)
            temp[0] = format_date
            temp[1] = 0 if temp[1] is None or self.__check_nan_exists(str(temp[6])) != -1 else self.__round_down(temp[1])
            temp[2] = 0 if temp[2] is None or self.__check_nan_exists(str(temp[6])) != -1 else self.__round_down(temp[2])
            temp[3] = 0 if temp[3] is None or self.__check_nan_exists(str(temp[6])) != -1 else self.__round_down(temp[3])
            temp[4] = 0 if temp[4] is None or self.__check_nan_exists(str(temp[6])) != -1 else self.__round_down(temp[4])
            temp[5] = 0 if temp[5] is None or self.__check_nan_exists(str(temp[6])) != -1 else self.__round_down(temp[5])
            temp[6] = 0 if temp[6] is None or self.__check_nan_exists(str(temp[6])) != -1 else int(temp[6])
            temp.insert(0, self.__ticker),
            temp.insert(1, self.__auth_user),
            temp.insert(2, self.__task_id)
            result.append(dict(zip(cols, temp[:10]))) if any(temp[4:]) is True else logger.debug(temp[4:])
        return result
    
    def __regular_data_for_api_v7(self, cols, rows):
        result = []
        for data in rows:
            temp = list(data)
            temp[1] = 0 if temp[1] is None or self.__check_nan_exists(str(temp[6])) != -1 else self.__round_down(temp[1])
            temp[2] = 0 if temp[2] is None or self.__check_nan_exists(str(temp[6])) != -1 else self.__round_down(temp[2])
            temp[3] = 0 if temp[3] is None or self.__check_nan_exists(str(temp[6])) != -1 else self.__round_down(temp[3])
            temp[4] = 0 if temp[4] is None or self.__check_nan_exists(str(temp[6])) != -1 else self.__round_down(temp[4])
            temp[5] = 0 if temp[5] is None or self.__check_nan_exists(str(temp[6])) != -1 else self.__round_down(temp[5])
            temp[6] = 0 if temp[6] is None or self.__check_nan_exists(str(temp[6])) != -1 else int(temp[6])
            temp.insert(0, self.__ticker),
            temp.insert(1, self.__auth_user),
            temp.insert(2, self.__task_id)
            result.append(dict(zip(cols, temp))) if any(temp[4:]) is True else logger.warning(f'{self.__ticker} no data in {temp[3]}')
        return result

    def __regular_data_for_api_v8(self, cols, rows):
        result = []
        for date, open_price, high_price, low_price, close_price, adjclose_price, volume in zip(
            rows[0], rows[1], rows[2], rows[3], rows[4], rows[5], rows[6],
        ):
            date = DT.convert_timestamp_to_datetime(date) if date else '1990-01-01'
            # logger.warning([date, open_price, high_price, low_price, close_price, adjclose_price, volume])
            open_price = 0 if open_price is None or self.__check_nan_exists(str(open_price)) != -1 else self.__round_down(open_price)
            high_price = 0 if high_price is None or self.__check_nan_exists(str(high_price)) != -1 else self.__round_down(high_price)
            low_price = 0 if low_price is None or self.__check_nan_exists(str(low_price)) != -1 else self.__round_down(low_price)
            close_price = 0 if close_price is None or self.__check_nan_exists(str(close_price)) != -1 else self.__round_down(close_price)
            adjclose_price = 0 if adjclose_price is None or self.__check_nan_exists(str(adjclose_price)) != -1 else self.__round_down(adjclose_price)
            # volume = 0 if volume is None or self.__check_nan_exists(str(volume)) != -1 else self.__round_down(volume)
            volume = 0 if volume is None or self.__check_nan_exists(str(volume)) != -1 else volume
            temp = [
                self.__ticker, self.__auth_user, self.__task_id,
                date, open_price, high_price,
                low_price, close_price, adjclose_price, volume
            ]
            # logger.debug(temp)
            result.append(dict(zip(cols, temp))) if any(temp[4:]) is True else logger.warning(f'{self.__ticker} no data in {temp[3]}')
        return result

    def __to_dict(self, cols, rows):
        result = []
        [result.append(dict(zip(cols, data[:6]))) for data in rows]
        return result

    def __to_csv(self, data=None, output_path=None):
        if data is None or output_path is None:
            raise ValueError("data and output path is required.")
        df = pd.DataFrame(data)
        self.__check_dir_is_exists(output_path)
        df.to_csv(f'{output_path}\{self.__ticker}_{createRandomCode()}.csv', index=True, header=True)

    # call yahoo finance python package obtain info
    def obtain_history_records(self, start=None, end=None, period=None):
        result = {
            'json_rows': '',
            'full_ticker': self.__ticker
        }
        try:
            # logger.info(f'ticker: {self.__ticker}')
            if start is None and end is None and period is None:
                raise ValueError("start date and end date and period is required.")
            if self.__country is not None and self.__country in self.__country_refre_dict:
                self.__ticker = self.__ticker + self.__country_refre_dict[self.__country]
                result['full_ticker'] = self.__ticker
            yf.pdr_override()
            # data = yf.download(self.__ticker, period=period) if period is not None else yf.download(self.__ticker, start=start, end=end)
            data = pdr.get_data_yahoo(self.__ticker, period=period) if period is not None else pdr.get_data_yahoo(self.__ticker, start=start, end=end)
            # self.__to_csv(data=data, output_path='./')
            rows = list(data.itertuples())
            if len(rows) > 0:
                info = sorted(self.__regular_data(self.__col, rows), key=lambda x: x['trade_date'], reverse=True)
                result['json_rows'] = info
            # logger.info(result['json_rows'])
            # logger.info(result['json_rows'][0])
        except Exception as e:
            logger.error(help.show_exp_detail_message(e))
        return result
    
    # call yahoo finance api version 7 obtain info
    def obtain_history_records_v1(self, start=None, end=None):
        result = {
            'json_rows': '',
            'full_ticker': self.__ticker
        }
        rows = []
        try:
            if start is None and end is None:
                raise Exception('The start date and end date is required')
            start_date = int(DT.get_datetime_convert_to_timestamp(start))
            end_date = int(DT.get_datetime_convert_to_timestamp(end))
            if self.__country is not None and self.__country in self.__country_refre_dict:
                self.__ticker = self.__ticker + self.__country_refre_dict[self.__country]
                result['full_ticker'] = self.__ticker
            
            #TODO method 1 (v8 after can not be use)
            full_url = f'{self.__base_url}v7/finance/download/{self.__ticker}?period1={start_date}&period2={end_date}&interval=1d&events=history'
            df = pd.read_csv(full_url)
            rows = list(df.itertuples(index=False))
            logger.warning(full_url)

            if len(rows) > 0:
                info = sorted(self.__regular_data_for_api_v7(self.__col, rows), key=lambda x: x['trade_date'], reverse=True)
                result['json_rows'] = info
                # output_path = f'./output/csv/v7'
                # if not os.path.exists(output_path):
                #     os.makedirs(output_path)
                # df = pd.DataFrame(result['json_rows'])
                # df.to_csv(f"{output_path}/{self.__ticker}.csv", encoding='utf-8-sig')
        except Exception as e:
            logger.error(help.show_exp_detail_message(e))
        return result
    
    # call yahoo finance api version 8 obtain info
    def obtain_history_records_v2(self, start=None, end=None):
        result = {
            'json_rows': '',
            'full_ticker': self.__ticker
        }
        rows = []
        try:
            if start is None and end is None:
                raise Exception('The start date and end date is required')
            start_date = int(DT.get_datetime_convert_to_timestamp(start))
            end_date = int(DT.get_datetime_convert_to_timestamp(end))
            if self.__country is not None and self.__country in self.__country_refre_dict:
                self.__ticker = self.__ticker + self.__country_refre_dict[self.__country]
                result['full_ticker'] = self.__ticker

            # for method 2
            full_url = f'{self.__base_url}v8/finance/chart/{self.__ticker}?symbol={self.__ticker}&period1={start_date}&period2={end_date}&interval=1d&events=history'
            logger.warning(full_url)

            #TODO method 2
            with RequestPageSource(
                url=full_url, mode=False,
                headers={'User-Agent': 'Mozilla/5.0'}
            ) as res:
                res_json = res.json()['chart']['result'][0]
                stock_info = res_json['indicators']['quote'][0]
                rows.extend(
                    [
                        res_json['timestamp'], stock_info['open'],
                        stock_info['high'], stock_info['low'],
                        stock_info['close'], res_json['indicators']['adjclose'][0]['adjclose'],
                        stock_info['volume']
                    ])
            if len(rows) > 0:
                info = sorted(self.__regular_data_for_api_v8(self.__col, rows), key=lambda x: x['trade_date'], reverse=True)
                result['json_rows'] = info
                # write_iterator_to_log(result['json_rows'])
                # output_path = f'./output/csv/v8'
                # if not os.path.exists(output_path):
                #     os.makedirs(output_path)
                # df = pd.DataFrame(result['json_rows'])
                # df.to_csv(f"{output_path}/{self.__ticker}.csv", encoding='utf-8-sig')
        except Exception as e:
            logger.error(help.show_exp_detail_message(e))
        return result