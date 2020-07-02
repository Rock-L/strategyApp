import pandas as pd
import numpy as np
from datetime import datetime
import os

file_path = os.path.abspath(os.path.dirname(__file__)) + "/static/data/"


def get_annual_yield():
    sheet_path = file_path + 'strategy.xlsx'
    net_value_sheet = pd.read_excel(sheet_path, sheet_name='net_value')
    res = net_value_sheet['nav'][-1] / net_value_sheet['nav'][0] - 1
    return res


def get_max_back():
    sheet_path = file_path + 'strategy.xlsx'
    net_value_sheet = pd.read_excel(sheet_path, sheet_name='net_value')
    back_list = []
    for i, date_value in enumerate(net_value_sheet.index.tolist()):
        if i == 0:
            continue
        x = net_value_sheet.loc[date_value, 'nav'] / max(list(net_value_sheet['nav'])[:i]) - 1
        back_list.append(x)
    return max(back_list)


def get_pe(date1str, date2str, asset_list):
    sheet_path = file_path + 'pe.xlsx'
    pe_sheet = pd.read_excel(sheet_path, sheet_name='pe')

    date1 = datetime.strptime(date1str, '%Y-%m-%d')
    date2 = datetime.strptime(date2str, '%Y-%m-%d')

    if date1 not in pe_sheet.index.tolist():
        return {'error': str(date1) + " is not valid"}
    elif date2 not in pe_sheet.index.tolist():
        return {'error': str(date2) + " is not valid"}

    column_list = []
    left_one_std_list = []
    left_two_std_list = []
    right_one_std_list = []
    right_two_std_list = []
    average_list = []
    date1_list = []
    date2_list = []
    print("===========" + str(asset_list))
    print(type(asset_list))
    for column in asset_list:
        aver = np.mean(pe_sheet[column])
        std = np.std(pe_sheet[column])

        left_one_std = [val for val in pe_sheet[column] if val < (aver - std)]
        left_two_std = [val for val in pe_sheet[column] if val < (aver - 2 * std)]
        right_one_std = [val for val in pe_sheet[column] if val < (aver + std)]
        right_two_std = [val for val in pe_sheet[column] if val < (aver + 2 * std)]
        average = [val for val in pe_sheet[column] if val < aver]
        date1_ = [val for val in pe_sheet[column] if val < pe_sheet.loc[date1, column]]
        date2_ = [val for val in pe_sheet[column] if val < pe_sheet.loc[date2, column]]

        left_one_std_list.append(round((len(left_one_std) + 1) / len(pe_sheet[column]) * 100, 1))
        left_two_std_list.append(round((len(left_two_std) + 1) / len(pe_sheet[column]) * 100, 1))
        right_one_std_list.append(round((len(right_one_std) + 1) / len(pe_sheet[column]) * 100, 1))
        right_two_std_list.append(round((len(right_two_std) + 1) / len(pe_sheet[column]) * 100, 1))
        average_list.append(round((len(average) + 1) / len(pe_sheet[column]) * 100, 1))
        date1_list.append(round((len(date1_) + 1) / len(pe_sheet[column]) * 100, 1))
        date2_list.append(round((len(date2_) + 1) / len(pe_sheet[column]) * 100, 1))
        column_list.append(column)

    res = {}
    res["column"] = column_list
    res["-Sigma"] = left_one_std_list
    res["-2Sigma"] = left_two_std_list
    res["+Sigma"] = right_one_std_list
    res["+2Sigma"] = right_two_std_list
    res["average"] = average_list
    res["date1"] = date1_list
    res["date2"] = date2_list

    return res


def get_one_day_value():
    '''
    {
        "date": "2020/02/02",
        "sum_return": 0.1,
        "back": 0.1,
        "sharpe": 0.1,
        "vol": 0.1
    }
    :return:
    term_list
    '''
    sheet_path = file_path + 'strategy.xlsx'
    net_value_sheet = pd.read_excel(sheet_path, sheet_name='net_value')
    term_list = []
    for i, date_value in enumerate(net_value_sheet.index.tolist()):
        print(date_value)
        if i == 0 or i == 1:
            continue
        one_day_term = {}
        sum_return = net_value_sheet.loc[date_value, 'nav'] / net_value_sheet['nav'][0] - 1
        back = net_value_sheet.loc[date_value, 'nav'] / max(list(net_value_sheet['nav'])[:i]) - 1
        annual_yield = (net_value_sheet.loc[date_value, 'nav'] / net_value_sheet['nav'][0]) ** (365 / i) - 1

        std_list = []
        for wav_i in range(i + 1):
            if wav_i == 0:
                continue

            res1 = list(net_value_sheet['nav'])[wav_i]
            res2 = list(net_value_sheet['nav'])[wav_i - 1]
            res = np.log(res1 / res2)
            std_list.append(res)

        annual_wav = np.std(std_list) * np.sqrt(260)
        sharpe = annual_yield / annual_wav

        one_day_term['date'] = date_value.strftime('%Y-%m-%d')
        one_day_term['sum_return'] = round(sum_return, 4)
        one_day_term['back'] = round(back, 4)
        one_day_term['sharpe'] = round(sharpe, 4)
        one_day_term['vol'] = round(annual_wav, 4)
        # one_day_term['date'] = date_value.strftime('%Y-%m-%d')
        # one_day_term['sum_return'] = 0.1
        # one_day_term['back'] = 0.1
        # one_day_term['sharpe'] = 0.1
        # one_day_term['vol'] = 0.1
        # "date": "2020/02/02",
        #                 "sum_return": 0.1,
        #                 "back": 0.1,
        #                 "sharpe": 0.1,
        #                 "vol": 0.1
        term_list.append(one_day_term)
    return term_list


def get_fci_res(country):
    sheet_path = file_path + 'fci_res.xlsx'

    if country == 'usfci':
        us_sheet = pd.read_excel(sheet_path, sheet_name='usfci')
        res = []
        for date_index in us_sheet.index.tolist():
            res_term = {}
            res_term['date'] = date_index.strftime('%Y-%m-%d')
            res_term["US-货币FCI"] = us_sheet.loc[date_index, 'US-货币FCI']
            res_term["US-债券FCI"] = us_sheet.loc[date_index, 'US-债券FCI']
            res_term["US-股票FCI"] = us_sheet.loc[date_index, 'US-股票FCI']
            res_term["拟合US-FCI"] = us_sheet.loc[date_index, '拟合US-FCI']
            res.append(res_term)
        return res

    elif country == 'eufci':
        us_sheet = pd.read_excel(sheet_path, sheet_name='eufci')
        res = []
        for date_index in us_sheet.index.tolist():
            res_term = {}
            res_term['date'] = date_index.strftime('%Y-%m-%d')
            res_term["EU-货币FCI"] = us_sheet.loc[date_index, 'EU-货币FCI']
            res_term["EU-债券FCI"] = us_sheet.loc[date_index, 'EU-债券FCI']
            res_term["EU-股票FCI"] = us_sheet.loc[date_index, 'EU-股票FCI']
            res_term["欧元区FCI"] = us_sheet.loc[date_index, '欧元区FCI']
            res.append(res_term)
        return res

    elif country == 'useuas':
        us_sheet = pd.read_excel(sheet_path, sheet_name='useuas')
        res = []
        for date_index in us_sheet.index.tolist():
            res_term = {}
            res_term['date'] = date_index.strftime('%Y-%m-%d')
            res_term["BFCIUS Index"] = us_sheet.loc[date_index, 'BFCIUS Index']
            res_term["BFCIEU Index"] = us_sheet.loc[date_index, 'BFCIEU Index']
            res_term["CIFCEMAS Index"] = us_sheet.loc[date_index, 'CIFCEMAS Index']
            res.append(res_term)
        return res


def get_fci(country):
    '''
    计算过程复杂，应做成时时计算，展示时直接读取结果表
    :param country:
    :return:
    '''
    sheet_path = file_path + 'fci.xlsx'
    currency_list = [
        ".TED G Index"
        , ".USLIBOIS Index"
        , ".CP3MOSPD Index"
    ]

    bond_list = [
        ".BAA10YB Index"
        , "LF98OAS Index"
        , ".MAAA10YB Index"
        , "USSN0C10 Curncy"
    ]

    stock_list = [
        "SPX Index"
        , "VIX Index"
    ]

    if country == 'usfci':
        us_sheet = pd.read_excel(sheet_path, sheet_name='usfci')
        us_param_sheet = pd.read_excel(sheet_path, sheet_name='usfci-param')

        for asset in us_sheet.columns:
            for date_index in us_sheet.index.tolist():
                index_value = us_sheet.index.tolist().index(date_index)
                value = us_sheet.loc[date_index, asset]
                mean = us_sheet[asset].iloc[index_value:index_value + 1825].mean()
                std = us_sheet[asset].iloc[index_value:index_value + 1825].std()
                std_value = (value - mean) / std

                us_sheet.loc[date_index, 'std' + asset] = std_value
                us_sheet.loc[date_index, "currency_weighted"] = us_sheet.loc[date_index, 'std' + asset] \
                                                                * us_param_sheet.loc['因子符号', asset] \
                                                                * us_param_sheet.loc['权重', asset]

        for date_index in us_sheet.index.tolist():
            us_sheet.loc[date_index, "currency_res"] = 0
            for asset in currency_list:
                us_sheet.loc[date_index, "currency_res"] += us_sheet.loc[date_index, asset]

        for date_index in us_sheet.index.tolist():
            us_sheet.loc[date_index, "bond_res"] = 0
            for asset in currency_list:
                us_sheet.loc[date_index, "bond_res"] += us_sheet.loc[date_index, asset]

        for date_index in us_sheet.index.tolist():
            us_sheet.loc[date_index, "stock_res"] = 0
            for asset in currency_list:
                us_sheet.loc[date_index, "stock_res"] += us_sheet.loc[date_index, asset]

        res = {}
        res["currency_res"] = us_sheet["currency_res"].tolist()
        res["bond_res"] = us_sheet["bond_res"].tolist()
        res["stock_res"] = us_sheet["stock_res"].tolist()
        res["date"] = us_sheet.index.tolist()

        return res


if __name__ == '__main__':
    # get_annual_yield()
    # a = get_one_day_value()
    # a = get_pe(1, 2, [])
    get_fci_res('usfci')
    get_fci_res('eufci')
    get_fci_res('useuas')
    print('yes')
