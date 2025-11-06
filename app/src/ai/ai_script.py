ai_results={
    "1":{
        "sql":"SELECT * FROM threads;",
        "table_names":["threads"],
        "data":
        {
            "chart":{
                "chart_type": "bar",
                "x_axis": "user",
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
    "2":{
        "sql":"SELECT * FROM threads;",
        "table_names":["threads"],
        "data":
        {
                "chart":{
                "chart_type": "scatter",
                "x_axis": "user",
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
        "sql":"SELECT * FROM threads;",
        "table_names":["threads"],
        "data":{
        "dashboard":{
                "name":"ai_dashboard",
                "charts":[
                        {
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
                        
                        },
                        {
                            "chart_type": "scatter",
                            "x_axis": "user",
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
                            
                        },
                        {
                            "chart_type": "bar",
                            "x_axis": "user",
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
                
                        },
                        {
                            "chart_type": "bar",
                            "x_axis": "user",
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
                
                        },
                        {
                            "chart_type": "bar",
                            "x_axis": "user",
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
                
                        },
                        {
                            "chart_type": "bar",
                            "x_axis": "user",
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
                    ]
                }
            }
        }
}

def ai_parse(prompt:str):
    if prompt in ai_results.keys():
        return ai_results[prompt]
    else:
        return {}