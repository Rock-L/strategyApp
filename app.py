from flask import Flask, render_template
from flask import jsonify
from flask import request
import json
import pandas as pd
import os
from strategy_data_process import *
from asset_data_process import *
from datetime import datetime

app = Flask(__name__)

file_path = os.path.abspath(os.path.dirname(__file__)) + "/static/data/"


#########
# 多策略实盘/策略配置模块数据
@app.route('/ll/strategy_shipan', methods=['POST'])
def strategy_shipan():
    res = get_strategy_shipan()
    return jsonify(res)


@app.route('/ll/asset_shipan', methods=['POST'])
def asset_shipan():
    res = get_asset_shipan()
    return jsonify(res)


#########
# 多策略回测/策略配置模块数据
@app.route('/ll/strategy_huice', methods=['POST'])
def strategy_huice():
    res = get_strategy_huice()
    return jsonify(res)


@app.route('/ll/asset_huice', methods=['POST'])
def asset_huice():
    res = get_asset_huice()
    return jsonify(res)


#########
# 策略组合/策略数据列表
@app.route('/ll/strategy_list', methods=['POST'])
def strategy_list():
    res = get_strategy_list()
    return jsonify(res)


@app.route('/ll/asset_list', methods=['POST'])
def asset_list():
    res = get_asset_list()
    return jsonify(res)


#########
@app.route('/ll/strategy_shipan_search', methods=['POST'])
def strategy_shipan_search():
    params = eval(json.loads(request.get_data(as_text=True)))
    start_time = params["firstTime"]  # 获取get请求参数
    end_time = params["lastTime"]  # 获取get请求参数
    print(start_time)
    print(end_time)
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    # start_time = datetime.strptime('2020-05-02', '%Y-%m-%d')
    # end_time = datetime.strptime('2020-05-06', '%Y-%m-%d')
    sheet_path = file_path + 'lishichicang.xlsx'
    res = get_strategy_shipan_lishichicang(sheet_path, start_time, end_time)
    return jsonify(res)


@app.route('/ll/asset_shipan_search', methods=['POST'])
def asset_shipan_search():
    params = eval(json.loads(request.get_data(as_text=True)))
    start_time = params["firstTime"]  # 获取get请求参数
    end_time = params["lastTime"]  # 获取get请求参数
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    # start_time = datetime.strptime('2020-05-02', '%Y-%m-%d')
    # end_time = datetime.strptime('2020-05-06', '%Y-%m-%d')
    sheet_path = file_path + 'lishichicang.xlsx'
    res = get_asset_shipan_lishichicang(sheet_path, start_time, end_time)
    return jsonify(res)


#########
@app.route('/ll/strategy_huice_search', methods=['POST'])
def strategy_huice_search():
    params = eval(json.loads(request.get_data(as_text=True)))
    start_time = params["firstTime"]  # 获取get请求参数
    end_time = params["lastTime"]  # 获取get请求参数
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    # start_time = datetime.strptime('2020-05-02', '%Y-%m-%d')
    # end_time = datetime.strptime('2020-05-06', '%Y-%m-%d')
    sheet_path = file_path + 'lishichicang.xlsx'
    res = get_strategy_huice_lishichicang(sheet_path, start_time, end_time)
    return jsonify(res)


@app.route('/ll/asset_huice_search', methods=['POST'])
def asset_huice_search():
    params = eval(json.loads(request.get_data(as_text=True)))
    start_time = params["firstTime"]  # 获取get请求参数
    end_time = params["lastTime"]  # 获取get请求参数
    start_time = datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.strptime(end_time, '%Y-%m-%d')
    # start_time = datetime.strptime('2020-05-02', '%Y-%m-%d')
    # end_time = datetime.strptime('2020-05-06', '%Y-%m-%d')
    sheet_path = file_path + 'lishichicang.xlsx'
    res = get_asset_huice_lishichicang(sheet_path, start_time, end_time)
    return jsonify(res)


@app.route('/ll/assessment_list', methods=['POST'])
def assessment_list():
    sheet_path = file_path + "pe.xlsx"
    return jsonify(list(pd.read_excel(sheet_path).columns))

@app.route('/ll/assessment', methods=['POST'])
def pe():
    params = eval(json.loads(request.get_data(as_text=True)))
    date1 = params["date1"]  # 获取get请求参数
    date2 = params["date2"]  # 获取get请求参数
    asset_list = params["asset_list"]  # 获取get请求参数

    res = get_pe(date1, date2,asset_list)
    return jsonify(res)


@app.route('/ll/eco', methods=['POST'])
def eco():
    params = eval(json.loads(request.get_data(as_text=True)))
    country = params["country"]  # 获取get请求参数
    print("country is : {}".format(country))

    sheet_path = file_path + "eco.xlsx"
    country_sheet = pd.read_excel(sheet_path, sheetname=country)

    res = []

    for ticker in set(country_sheet["Ticker"]):
        term = {}
        index_list = country_sheet[country_sheet["Ticker"] == ticker].index.tolist()
        if len(index_list) == 0:
            continue

        valid_index = index_list[0]
        for index_ in index_list:
            if country_sheet['Date Time'].iloc[index_] > country_sheet['Date Time'][0]:
                valid_index = index_
        print("{} : {}".format(ticker, valid_index))
        term['ticker'] = ticker
        term['指标名称'] = country_sheet["Event"].iloc[valid_index]
        term['分类'] = "生产"
        term['最新数据日期'] = country_sheet["last time"].iloc[valid_index]
        term['更新日期'] = country_sheet["Date Time"].iloc[valid_index]
        term['调查值'] = country_sheet["Survey"].iloc[valid_index]
        term['实际值'] = country_sheet["Actual"].iloc[valid_index]
        term['前值'] = country_sheet["Prior"].iloc[valid_index]

        res.append(term)

    return jsonify(res)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
