from src.core.app import App
from src.core.settings_manager import SettingsManager
from src.ai.ai_script import ai_parse
from src.models.dashboard_model import DashboardModel

from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates

from src.api import chart_router
from src.api import dashboard_router
from src.api import main_router
settings_manager=SettingsManager()
settings_manager.filename="config.ini"
settings_manager.load()

main_app=App()
main_app.load_from_settings(settings=settings_manager.settings)
main_app.start()

fastapi_app=FastAPI()
templates = Jinja2Templates(directory="src/api/templates")

@fastapi_app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "main.html",
        {
            "request":request,
            "base_url": f"http://{settings_manager.settings.superset_host}:{settings_manager.settings.superset_port}",
        }
    )

fastapi_app.include_router(chart_router.router)
fastapi_app.include_router(dashboard_router.router)
fastapi_app.include_router(main_router.router)
#data=ai_parse("4")
#result=app.connector.create_dataset(data["sql"],data["table_names"])

#dashboard_obj=DashboardModel() 
#dashboard_obj.from_model_dict(data["data"]["dashboard"],result.json()["data"])
#for chart_obj in dashboard_obj.charts:
#    result=app.connector.create_chart(chart_obj.to_json())
#    chart_obj.chart_id=result.json()["id"]
#print(app.connector.create_dashboard(dashboard_obj.to_json()).json())

