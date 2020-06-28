performance_data = {
    "id": id,
    "strategy_shipan": {
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
        },
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
        },
        "chicangtiaozheng": {
            "macro1",
            "macro6",
            "macro12",
            "macro13",
            "macro14"
        },
        "lishichicang": [
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
}

performance_data = {
    "id": id,
    "zichan_shipan": {
        "lishichicang": [
            {
                "date": "2020/02/02",
                "美股": 0.1,
                "日股": 0.4,
                "英股": 0.5,
                "德股": 0.5,
                "澳股": 0.5
            },
            {
                "date": "2020/02/02",
                "美股": 0.1,
                "日股": 0.4,
                "英股": 0.5,
                "德股": 0.5,
                "澳股": 0.5
            }
        ]
    }
}

portfolio_data = {
    "asset_portfolio": [
        {
            "name": "美股",
            "type": "equity",
            "tc": 0.1,
            "rc": 0.1,
            "ticker": "美股 index"
        },
        {
            "name": "日债",
            "type": "bond",
            "tc": 0.1,
            "rc": 0.1,
            "ticker": "日债 index"
        }
    ]
}
portfolio_data = {
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
}
