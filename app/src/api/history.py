from fastapi import APIRouter,HTTPException
from ..models.chart_factory import ChartFactory
from ..core.app import App
from .models import *
from fastapi import APIRouter, Request, Response, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta
import uuid
from typing import Optional, Dict, Any, List
from pydantic import BaseModel

charts_router = APIRouter(prefix='/charts', tags=['Creating charts'])
main_app = App()

# Конфигурация JWT для сессий
SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
SESSION_COOKIE_NAME = "app_session"
SESSION_EXPIRE_DAYS = 7
MAX_HISTORY_ITEMS = 20

class HistoryItem(BaseModel):
    id: str
    prompt: str
    type: str  # 'chart' или 'dashboard'
    result_id: str  # ID графика или дашборда
    sql_query: str
    chart_type: Optional[str] = None
    created_at: str

class SessionData(BaseModel):
    session_id: str
    history: List[Dict[str, Any]] = []
    created_at: datetime
    last_activity: datetime

class SessionManager:
    @staticmethod
    def create_session_id() -> str:
        """Создание уникального ID сессии"""
        return str(uuid.uuid4())
    
    @staticmethod
    def encode_session(data: SessionData) -> str:
        """Кодирование данных сессии в JWT токен"""
        payload = {
            "session_id": data.session_id,
            "history": data.history,
            "created_at": data.created_at.isoformat(),
            "last_activity": data.last_activity.isoformat(),
            "exp": datetime.utcnow() + timedelta(days=SESSION_EXPIRE_DAYS)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    @staticmethod
    def decode_session(token: str) -> Optional[SessionData]:
        """Декодирование JWT токена в данные сессии"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            
            created_at = datetime.fromisoformat(payload["created_at"].replace('Z', '+00:00'))
            last_activity = datetime.fromisoformat(payload["last_activity"].replace('Z', '+00:00'))
            
            return SessionData(
                session_id=payload["session_id"],
                history=payload["history"],
                created_at=created_at,
                last_activity=last_activity
            )
        except (JWTError, KeyError, ValueError):
            return None
    
    @staticmethod
    def get_or_create_session(request: Request) -> SessionData:
        """Получить существующую сессию или создать новую"""
        token = request.cookies.get(SESSION_COOKIE_NAME)
        
        if token:
            session_data = SessionManager.decode_session(token)
            if session_data:
                # Обновляем время последней активности
                session_data.last_activity = datetime.now()
                return session_data
        
        # Создаем новую сессию
        return SessionData(
            session_id=SessionManager.create_session_id(),
            history=[],
            created_at=datetime.now(),
            last_activity=datetime.now()
        )
    
    @staticmethod
    def save_session(response: Response, session_data: SessionData):
        """Сохранить сессию в cookie"""
        token = SessionManager.encode_session(session_data)
        
        response.set_cookie(
            key=SESSION_COOKIE_NAME,
            value=token,
            httponly=True,
            max_age=SESSION_EXPIRE_DAYS * 24 * 3600,
            samesite="lax",
            # secure=True  # Для продакшена с HTTPS
        )

def add_to_history(session: SessionData, item_data: Dict[str, Any]):
    """Добавить запись в историю сессии"""
    history_item = {
        "id": str(uuid.uuid4()),
        "prompt": item_data["prompt"],
        "type": item_data["type"],
        "result_id": item_data["result_id"],
        "sql_query": item_data["sql_query"],
        "chart_type": item_data.get("chart_type"),
        "created_at": datetime.now().isoformat()
    }
    
    # Добавляем в начало истории
    session.history.insert(0, history_item)
    
    # Ограничиваем количество записей
    if len(session.history) > MAX_HISTORY_ITEMS:
        session.history = session.history[:MAX_HISTORY_ITEMS]
    
    # Обновляем время активности
    session.last_activity = datetime.utcnow()

# Общие эндпоинты для работы с историей
@charts_router.get("/history", summary="Get query history from session")
async def get_history(request: Request):
    """Получить историю запросов из сессии"""
    session = SessionManager.get_or_create_session(request)
    
    return {
        "success": True,
        "history": session.history,
        "count": len(session.history),
        "session_created": session.created_at.isoformat(),
        "last_activity": session.last_activity.isoformat(),
        "session_id": session.session_id
    }

@charts_router.get("/history/{item_id}", summary="Get specific history item")
async def get_history_item(item_id: str, request: Request):
    """Получить конкретную запись из истории"""
    session = SessionManager.get_or_create_session(request)
    
    for item in session.history:
        if item.get("id") == item_id:
            return {
                "success": True,
                "item": item
            }
    
    raise HTTPException(status_code=404, detail="History item not found")

@charts_router.delete("/history/{item_id}", summary="Delete history item")
async def delete_history_item(
    item_id: str,
    request: Request,
    response: Response
):
    """Удалить запись из истории"""
    session = SessionManager.get_or_create_session(request)
    
    # Фильтруем историю
    initial_count = len(session.history)
    session.history = [item for item in session.history if item.get("id") != item_id]
    
    # Сохраняем изменения
    SessionManager.save_session(response, session)
    
    return {
        "success": True,
        "deleted": initial_count > len(session.history),
        "remaining_count": len(session.history)
    }

@charts_router.delete("/history", summary="Clear all history")
async def clear_history(
    request: Request,
    response: Response
):
    """Очистить всю историю"""
    session = SessionManager.get_or_create_session(request)
    session.history = []
    
    SessionManager.save_session(response, session)
    
    return {
        "success": True,
        "message": "History cleared"
    }

@charts_router.get("/session/info", summary="Get session information")
async def get_session_info(request: Request):
    """Получить информацию о текущей сессии"""
    session = SessionManager.get_or_create_session(request)
    
    return {
        "success": True,
        "session_id": session.session_id,
        "history_count": len(session.history),
        "session_created": session.created_at.isoformat(),
        "last_activity": session.last_activity.isoformat(),
        "session_active_minutes": int((datetime.utcnow() - session.created_at).total_seconds() / 60)
    }