from ..ai.speech_recognition import VoskRecognizer
from fastapi import APIRouter,HTTPException, UploadFile, File, HTTPException
from ..ai.ai_script import ai_parse
from ..models.dashboard_model import DashboardModel
from ..core.app import App
from .models import *
from ..core.validator import validator

import uuid
import os
router = APIRouter(prefix='/main', tags=['Main api requests'])
try:
    vosk_recognizer = VoskRecognizer("src/ai/ai_models/vosk-model-small-ru-0.22")
    RECOGNIZER_AVAILABLE = True
except Exception as e:
    print(f"Vosk не доступен: {e}")
    RECOGNIZER_AVAILABLE = False


@router.post("/recognize",summary="Recognize voixe from audio")
async def recognize_speech_from_audio(file: UploadFile = File(...)):
    if not RECOGNIZER_AVAILABLE:
        raise HTTPException(status_code=503, detail="Сервис распознавания временно недоступен")
    
    try:
        # Проверяем тип файла
        allowed_types = ['audio/webm', 'audio/wav', 'audio/mpeg', 'audio/ogg', 'audio/m4a']
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Неподдерживаемый формат аудио")
        
        # Читаем файл
        contents = await file.read()
        
        # Определяем формат файла
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'webm'
        
        # Конвертируем в WAV
        wav_file_path = vosk_recognizer.convert_to_wav(contents, file_extension)
        
        try:
            # Распознаем речь
            recognition_result = vosk_recognizer.recognize_speech(wav_file_path)
            
            # Очищаем временные файлы
            if os.path.exists(wav_file_path):
                os.remove(wav_file_path)
            
            return {
                **recognition_result,
                "filename": file.filename,
                "file_size": len(contents),
                "processed_at": str(uuid.uuid4())
            }
            
        except Exception as e:
            # Очищаем временные файлы в случае ошибки
            if os.path.exists(wav_file_path):
                os.remove(wav_file_path)
            raise e
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))