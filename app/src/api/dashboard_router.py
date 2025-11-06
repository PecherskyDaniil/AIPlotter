from fastapi import APIRouter,HTTPException
from ..ai.ai_script import ai_parse
from ..models.dashboard_model import DashboardModel
from ..core.app import App
from .models import *
from ..core.validator import validator
router = APIRouter(prefix='/dashboards', tags=['Creating dashboards'])
main_app=App()
@router.post("/create/text",summary="Create dashboard by text prompt")
async def create_dashboard_by_prompt(body:TextPrompt):
    prompt=body.prompt
    result_json=ai_parse(prompt)
    try:
        validator.validate_dashboard_json(result_json)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model created wrong json")
    dataset_result=main_app.connector.create_dataset(result_json["sql"],result_json["table_names"])
    if dataset_result is False:
        raise HTTPException(status_code=500, detail=f"Can't create dataset")
    dashboard_obj=DashboardModel() 
    dashboard_obj.from_model_dict(result_json["data"]["dashboard"],dataset_result.json()["data"])
    for chart_obj in dashboard_obj.charts:
        chart_result=main_app.connector.create_chart(chart_obj.to_json())
        if chart_result is False:
            raise HTTPException(status_code=500, detail=f"Can't create chart")
        chart_obj.chart_id=chart_result.json()["id"]
    dashboard_result=main_app.connector.create_dashboard(dashboard_obj.to_json())
    if dashboard_result is False:
        raise HTTPException(status_code=500, detail=f"Can't create dashboard")
    return Response(
        success=True,
        message="Dashboard, charts and dataset created successfully",
        result=dashboard_result.json())
