from fastapi import APIRouter,HTTPException
from ..ai.ai_script import ai_parse
from ..models.chart_factory import ChartFactory
from ..core.app import App
from .models import *
from ..core.validator import validator
router = APIRouter(prefix='/charts', tags=['Creating charts'])
main_app=App()
@router.post("/create/text",summary="Create chart by text prompt")
async def create_chart_by_prompt(body:TextPrompt):
    prompt=body.prompt
    result_json=ai_parse(prompt)
    try:
        validator.validate_chart_json(result_json)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model created wrong json")
    dataset_result=main_app.connector.create_dataset(result_json["sql"],result_json["table_names"])
    if dataset_result is False:
        raise HTTPException(status_code=500, detail=f"Can't create dataset")
    chart_obj=ChartFactory().create(result_json["data"]["chart"],dataset_result.json()["data"])
    answer=main_app.connector.create_chart(chart_obj.to_json())
    if answer is False:
        raise HTTPException(status_code=500, detail=f"Can't create chart")
    return Response(
        success=True,
        message="Chart and dataset created successfully",
        result=answer.json())
