from fastapi import APIRouter,HTTPException
from ..ai.ai_script import ai_parse
from ..models.chart_factory import ChartFactory
from ..core.app import App
from .models import *
from ..core.validator import validator
from fastapi import APIRouter, Request, Response, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
import uuid
from .history import SessionManager,SessionData,MAX_HISTORY_ITEMS,add_to_history
charts_router = APIRouter(prefix='/charts', tags=['Creating charts'])
main_app = App()

# Конфигурация JWT


@charts_router.post("/create/text", summary="Create chart by text prompt")
async def create_chart_by_prompt(
    body: TextPrompt,
    request: Request,
    response: Response
):
    """Создать график по текстовому запросу"""
    # Получаем или создаем сессию
    session = SessionManager.get_or_create_session(request)
    
    # Оригинальная логика создания графика
    prompt = body.prompt
    result_json = ai_parse(prompt)
    
    try:
        validator.validate_chart_json(result_json)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model created wrong json")
    
    dataset_result = main_app.connector.create_dataset(result_json["sql"], result_json["table_names"])
    table_source = main_app.connector.get_table(result_json["table_names"][0])
    database_id = table_source["database"]["id"]
    sql_result = main_app.connector.execute_sql_query(result_json["sql"], database_id)
    
    if dataset_result is False:
        raise HTTPException(status_code=500, detail=f"Can't create dataset")
    
    chart_obj = ChartFactory().create(result_json["data"]["chart"], dataset_result.json()["data"])
    answer = main_app.connector.create_chart(chart_obj.to_json())
    
    if answer is False:
        raise HTTPException(status_code=500, detail=f"Can't create chart")
    
    chart_id = answer.json()["id"]
    
    # Формируем ответ
    result_response = {
        "id": chart_id,
        "sql": result_json["sql"],
        "data": sql_result["data"]
    }
    
    # Добавляем в историю сессии
    add_to_history(session, {
        "prompt": prompt,
        "type": "chart",
        "result_id": chart_id,
        "sql_query": result_json["sql"],
        "chart_type": result_json["data"]["chart"]
    })
    
    # Сохраняем сессию
    SessionManager.save_session(response, session)
    
    return {
        "success": True,
        "message": "Chart and dataset created successfully",
        "result": result_response,
        "history_count": len(session.history)
    }