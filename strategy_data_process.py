import pandas as pd
import os
import io
import time
from get_values import *

file_path = os.path.abspath(os.path.dirname(__file__)) + "/static/data/"


def get_strategy_shipan():
    sheet_path = file_path + 'strategy.xlsx'
    strategy_shipan = {}
    strategy_shipan['celuepeizhi'] = get_strategy_shipan_celuepeizhi(sheet_path)
    strategy_shipan['chicangjilu'] = get_strategy_chicangjilu_index(sheet_path)
    strategy_shipan['lishiyeji'] = get_strategy_shipan_lishiyeji(sheet_path)

    return strategy_shipan


def get_strategy_huice():
    sheet_path = file_path + 'strategy.xlsx'
    strategy_huice = {}
    strategy_huice['celuepeizhi'] = get_strategy_huice_celuepeizhi(sheet_path)
    strategy_huice['chicangjilu'] = get_strategy_chicangjilu_index(sheet_path)
    strategy_huice['lishiyeji'] = get_strategy_huice_lishiyeji(sheet_path)

    return strategy_huice


def get_strategy_huice_celuepeizhi(sheet_path):
    return get_strategy_shipan_celuepeizhi(sheet_path)


def get_strategy_huice_lishiyeji(sheet_path):
    return get_strategy_shipan_lishiyeji(sheet_path)


def get_strategy_shipan_lishiyeji(sheet_path):
    '''

    :param sheet_path:
    :return:
        "strategy_shipan": {
        "lishiyeji": {
            "history_annual_yield": 0.3,
            "history_max_back": 0.4,
            "month_performance": {
                [
                    {
                        "date": "2020/02/02",
                        "sum_return": 0.1,
                        "back": 0.1,
                        "sharpe": 0.1,
                        "vol": 0.1
                    },
                    {
                        "date": "2020/02/02",
                        "sum_return": 0.1,
                        "back": 0.1,
                        "sharpe": 0.1,
                        "vol": 0.1
                    }
                ]
            }
        }
        }

    '''

    history_annual_yield = get_annual_yield()
    history_max_back = get_max_back()

    lishiyeji = {
        "history_annual_yield": round(history_annual_yield, 2),
        "history_max_back": round(history_max_back, 2),
        "month_performance": get_one_day_value()

    }
    # lishiyeji = {
    #     "history_annual_yield": 0.3,
    #     "history_max_back": 0.4,
    #     "month_performance":
    #         [
    #             {
    #                 "date": "2020/02/02",
    #                 "sum_return": 0.1,
    #                 "back": 0.1,
    #                 "sharpe": 0.1,
    #                 "vol": 0.1
    #             },
    #             {
    #                 "date": "2020/02/02",
    #                 "sum_return": 0.1,
    #                 "back": 0.1,
    #                 "sharpe": 0.1,
    #                 "vol": 0.1
    #             }
    #         ]
    #
    # }

    return lishiyeji


def get_strategy_huice_lishichicang(sheet_path, start_time, end_time):
    return get_strategy_shipan_lishichicang(sheet_path, start_time, end_time)


def get_strategy_list():
    '''
    :return:
        "strategy_portfolio": [
        {
            "name": "macro1",
            "type": "beta",
            "tc": 0.1,
            "rc": 0.1,
            "ticker": "macro1 index"
        },
        {
            "name": "macro6",
            "type": "altha",
            "tc": 0.1,
            "rc": 0.1,
            "ticker": "macro6 index"
        }
    ]
    '''
    sheet_path = file_path + 'strategy.xlsx'
    param_sheet = pd.read_excel(sheet_path, sheet_name='param')
    strategy_portfolio = []
    for asset in param_sheet.columns:
        strategy_term = {}
        strategy_term['name'] = asset
        strategy_term['type'] = param_sheet.loc['type', asset]
        strategy_term['tc'] = param_sheet.loc['TC', asset]
        strategy_term['rc'] = param_sheet.loc['RC', asset]
        strategy_term['ticker'] = param_sheet.loc['Ticker', asset]
        strategy_portfolio.append(strategy_term)
    return strategy_portfolio


def get_strategy_shipan_lishichicang(sheet_path, start_time, end_time):
    '''

    :param sheet_path:
    :return:
        "strategy_shipan": {
        "lishichicang":
            [
                {
                    "date": "2020/02/02",
                    "macro1": 0.1,
                    "macro6": 0.4,
                    "macro12": 0.5,
                    "macro13": 0.5,
                    "macro14": 0.5
                },
                {
                    "date": "2020/02/02",
                    "macro1": 0.1,
                    "macro6": 0.4,
                    "macro12": 0.5,
                    "macro13": 0.5,
                    "macro14": 0.5
                }
            ]
        }

    '''
    id1_sheet = pd.read_excel(sheet_path, sheet_name='id1')
    lishichicang = []
    for date_index in id1_sheet.index.tolist():
        if date_index > start_time:
            if date_index < end_time:
                chicang_term = {}
                for col in id1_sheet.columns:
                    chicang_term['data'] = date_index
                    chicang_term[col] = round(id1_sheet.loc[date_index, col], 2)
                lishichicang.append(chicang_term)
            else:
                break
        else:
            continue
    return lishichicang


def get_strategy_chicangjilu_index(sheet_path):
    '''
    :param sheet_path:
    :return:
        "chicangjilu":
        [
            "macro1",
            "macro6",
            "macro12",
            "macro13",
            "macro14"
        ]
    '''
    chicang_sheet = pd.read_excel(sheet_path, sheet_name='chicang')
    chicang_list = list(chicang_sheet.columns)
    return chicang_list


def get_strategy_shipan_celuepeizhi(sheet_path):
    '''

    :param sheet_path:
    :return:
        "celuepeizhi": {
            # 当前日期
            "date": "2020/02/02",
            "wuganggan": {
                "asset": {
                    "macro1": 0.1,
                    "macro6": 0.4,
                    "macro12": 0.5
                }
            },
            "ganggan": {
                "ganggan": 2,
                "asset": {
                    "macro1": 0.2,
                    "macro6": 0.3,
                    "macro12": 0.5
                }
            }
        }

    '''
    
    chicang_sheet = pd.read_excel(sheet_path, sheet_name='chicang')
    print("==============="+str(chicang_sheet.index.tolist()))
    celuepeizhi = {}
    celuepeizhi['date'] = time.strftime("%Y-%m-%d")
    asset_list = {}
    for asset in chicang_sheet.columns:
        asset_list[asset] = chicang_sheet.loc['chicang', asset]
    asset_val = {}
    asset_val["asset"] = asset_list
    celuepeizhi['wuganggan'] = asset_val

    asset_list = {}
    for asset in chicang_sheet.columns:
        asset_list[asset] = chicang_sheet.loc['chicang', asset]
    asset_val = {}
    asset_val["asset"] = asset_list
    asset_val["ganggan"] = 2
    celuepeizhi['ganggan'] = asset_val

    return celuepeizhi


if __name__ == '__main__':
    a = get_strategy_shipan()
    # b = get_strategy_huice()
    # c = get_strategy_list()
