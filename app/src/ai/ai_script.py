ai_results={
    "1":{
        "sql":"SELECT * FROM reqs;",
        "table_names":["reqs"],
        "data":
        {
            "chart":{
                "chart_type": "bar",
                "x_axis": "Год",
                "metrics": [
                        {
                        "column_name":"НомерОбращения",
                        "aggregate":"COUNT"
                        }
                        ],
                "group_by":["Управление"],
                "filters": [
                    {
                        "column": "Год",
                        "operator": "IN",
                        "comparator": [2020,2021,2022,2023]
                    }
                ]
            }
        }
    },
    "2":{
        "sql":"SELECT * FROM reqs;",
        "table_names":["reqs"],
        "data":
        {
                "chart":{
                "chart_type": "scatter",
                "x_axis": "Дата",
                "metrics": [
                        {
                        "column_name":"НомерОбращения",
                        "aggregate":"COUNT"
                        }
                        ],
                "group_by":["Состояние"],
                "filters": [
                    {
                        "column": "Год",
                        "operator": "==",
                        "comparator": 2021
                    }
                ]
            }
        }
    },
    "3":{
        "sql":"SELECT * FROM threads;",
        "table_names":["threads"],
        "data":
        {
                "chart":{
                "chart_type": "pie",
                "metrics": [
                        {
                        "column_name":"reply_users_count",
                        "aggregate":"SUM"
                        },
                        {
                        "column_name":"thread_ts",
                        "aggregate":"COUNT_DISTINCT"
                        },
                        ],
                "group_by":["team"],
                "filters": [
                    {
                        "column": "type",
                        "operator": "IN",
                        "comparator": ["message"]
                    }
                ]
            }
        }
    },
    "4":{
        "sql":"SELECT * FROM reqs;",
        "table_names":["reqs"],
        "data":{
        "dashboard":{
                "name":"requests_dashboard",
                "charts":[
                        {
                            "chart_type": "bar",
                            "x_axis": "Год",
                            "metrics": [
                                    {
                                    "column_name":"НомерОбращения",
                                    "aggregate":"COUNT"
                                    }
                                    ],
                            "group_by":["Управление"],
                            "filters": [
                                {
                                    "column": "Год",
                                    "operator": "IN",
                                    "comparator": [2020,2021,2022,2023]
                                }
                            ]
                        },

                        {
                            "chart_type": "pie",
                            "metrics": [
                                    {
                                    "column_name":"НомерОбращения",
                                    "aggregate":"COUNT"
                                    }
                                    ],
                            "group_by":["Тип"],
                            "filters": [
                                {
                                    "column": "Год",
                                    "operator": "IN",
                                    "comparator": [2020,2021,2022,2023]
                                }
                            ]
                        },
                        {
                        "chart_type": "scatter",
                        "x_axis": "Дата",
                        "metrics": [
                                {
                                "column_name":"НомерОбращения",
                                "aggregate":"COUNT"
                                }
                                ],
                        "group_by":["Состояние"],
                        "filters": [
                            {
                                "column": "Год",
                                "operator": "IN",
                                "comparator": [2020,2021,2022,2023]
                            }
                        ]
                    }
                    ]
                }
            }
        }
}

def ai_parse(prompt:str,type="dashboard"):
    if prompt in ai_results.keys():
        return ai_results[prompt]
    else:
        return {}