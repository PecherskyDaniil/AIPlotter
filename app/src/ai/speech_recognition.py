from pydub import AudioSegment
import tempfile
import os
import json
import io
from ..core.logger import get_logger
class VoskRecognizer:
    def __init__(self, model_path: str = None):
        self.logger=get_logger("speech_recognition")
        try:
            from vosk import Model, KaldiRecognizer
            import wave
            
            if model_path is None:
                model_path = "src/ai/ai_models/vosk-model-small-ru-0.22"
            
            if not os.path.exists(model_path):
                raise Exception(f"Модель Vosk не найдена по пути: {model_path}")
            
            self.model = Model(model_path)
            self.wave = wave
            
        except ImportError:
            raise Exception("Vosk не установлен. pip install vosk")
    
    def convert_to_wav(self, audio_data: bytes, original_format: str) -> str:
        """Конвертирует аудио в WAV формат 16kHz mono"""
        try:
            audio = AudioSegment.from_file(io.BytesIO(audio_data), format=original_format)
            audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
            
            
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                audio.export(temp_file.name, format="wav")
                self.logger.info("Audio converted to wav format")
                return temp_file.name
            
                
        except Exception as e:
            self.logger.error(f"Error while converting audio to wav {e}")
            raise Exception(f"Ошибка конвертации аудио: {str(e)}")
    
    def recognize_speech(self, audio_file_path: str) -> dict:
        """Распознает речь из аудио файла"""
        try:
            from vosk import KaldiRecognizer
            
            with self.wave.open(audio_file_path, "rb") as wf:

                if (wf.getnchannels() != 1 or 
                    wf.getsampwidth() != 2 or 
                    wf.getcomptype() != "NONE"):
                    self.logger.error("Error while converting audio to text: audio should be WAV mon 16kHZ")
                    raise Exception("Аудио файл должен быть в формате WAV mono 16kHz")
                
                recognizer = KaldiRecognizer(self.model, wf.getframerate())
                recognizer.SetWords(True)
                
                results = []
                while True:
                    data = wf.readframes(4000)
                    if len(data) == 0:
                        break
                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        results.append(result)
                
                final_result = json.loads(recognizer.FinalResult())
                results.append(final_result)
                
                full_text = " ".join([result.get("text", "") for result in results if result.get("text")])
                
                self.logger.info("Audio successfully recognized and converted to speech")
                return {
                    "text": full_text.strip(),
                    "confidence": 1.0,  
                    "status": "success",
                    "recognizer": "vosk"
                }
                
        except Exception as e:
            self.logger.error(f"Error while converting audio to text {e}")
            return {
                "text": "",
                "error": f"Ошибка распознавания: {str(e)}",
                "status": "error"
            }