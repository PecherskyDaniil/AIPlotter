from ..ai.ai_script import ai_parse
from ..models.dashboard_model import DashboardModel
from ..core.app import App
from .models import *
from ..core.validator import validator
from fastapi import APIRouter, Request, Response, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import uuid
from .history import SessionManager,SessionData,MAX_HISTORY_ITEMS,add_to_history
dashboards_router = APIRouter(prefix='/dashboards', tags=['Creating dashboards'])
main_app=App()
@dashboards_router.post("/create/text", summary="Create dashboard by text prompt")
async def create_dashboard_by_prompt(
    body: TextPrompt,
    request: Request,
    response: Response
):
    """Создать дашборд по текстовому запросу"""
    # Получаем или создаем сессию
    session = SessionManager.get_or_create_session(request)
    
    # Оригинальная логика создания дашборда
    prompt = body.prompt
    result_json = ai_parse(prompt)
    
    try:
        validator.validate_dashboard_json(result_json)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model created wrong json")
    
    dataset_result = main_app.connector.create_dataset(result_json["sql"], result_json["table_names"])
    table_source = main_app.connector.get_table(result_json["table_names"][0])
    database_id = table_source["database"]["id"]
    sql_result = main_app.connector.execute_sql_query(result_json["sql"], database_id)
    
    if dataset_result is False:
        raise HTTPException(status_code=500, detail=f"Can't create dataset")
    
    # Создаем дашборд и все графики
    dashboard_obj = DashboardModel() 
    dashboard_obj.from_model_dict(result_json["data"]["dashboard"], dataset_result.json()["data"])
    
    chart_ids = []
    for chart_obj in dashboard_obj.charts:
        chart_result = main_app.connector.create_chart(chart_obj.to_json())
        if chart_result is False:
            raise HTTPException(status_code=500, detail=f"Can't create chart")
        chart_obj.chart_id = chart_result.json()["id"]
        chart_ids.append(chart_result.json()["id"])
    
    dashboard_result = main_app.connector.create_dashboard(dashboard_obj.to_json())
    if dashboard_result is False:
        raise HTTPException(status_code=500, detail=f"Can't create dashboard")
    
    dashboard_id = dashboard_result.json()["id"]
    
    # Формируем ответ
    result_response = {
        "id": dashboard_id,
        "sql": result_json["sql"],
        "data": sql_result["data"],
        "chart_ids": chart_ids,
        "chart_count": len(chart_ids)
    }
    
    # Добавляем в историю сессии
    add_to_history(session, {
        "prompt": prompt,
        "type": "dashboard",
        "result_id": dashboard_id,
        "sql_query": result_json["sql"],
        "chart_type": "dashboard"
    })
    
    # Сохраняем сессию
    SessionManager.save_session(response, session)
    
    return {
        "success": True,
        "message": "Dashboard, charts and dataset created successfully",
        "result": result_response,
        "history_count": len(session.history)
    }
