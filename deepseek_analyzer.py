from typing import Dict, Any, Optional
import requests
import json
import logging
import re
from dataclasses import dataclass
from deepseek_config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TradingAnalysis:
    """Структура данных для результата анализа"""
    signal_type: str
    confidence_level: int
    risk_level: str
    assets_mentioned: list
    price_targets: Dict[str, str]
    timeframe: str
    summary: str
    recommendation: str
    key_risks: str

class DeepSeekTradingAnalyzer:
    """Анализатор торговых сигналов с использованием DeepSeek API"""
    
    def __init__(self):
        self.api_key: str = DEEPSEEK_API_KEY
        self.api_url: str = DEEPSEEK_API_URL
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

    def analyze_message(self, message_text: str, channel_info: str = "") -> Dict[str, Any]:
        """
        Анализ торгового сообщения
        
        Args:
            message_text (str): Текст для анализа
            channel_info (str): Информация о канале источника
            
        Returns:
            Dict[str, Any]: Результат анализа или информация об ошибке
        """
        if not self._validate_input(message_text):
            return {"error": "Некорректный входной текст"}

        try:
            response = self._make_api_request(message_text, channel_info)
            return self._process_response(response)
        except Exception as e:
            logger.error(f"Ошибка при анализе: {str(e)}")
            return {"error": str(e)}

    def _validate_input(self, text: str) -> bool:
        """Проверка входных данных"""
        return bool(text and isinstance(text, str) and len(text.strip()) > 0)

    def _make_api_request(self, message: str, context: str) -> requests.Response:
        """Выполнение запроса к API"""
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": self._get_system_prompt()
                },
                {
                    "role": "user",
                    "content": self._create_trading_prompt(message, context)
                }
            ],
            "temperature": 0.3,
            "max_tokens": 1000
        }

        response = self.session.post(
            self.api_url,
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        return response

    def _process_response(self, response: requests.Response) -> Dict[str, Any]:
        """Обработка ответа от API"""
        data = response.json()
        if 'choices' not in data or not data['choices']:
            raise ValueError("Некорректный ответ API")
            
        analysis = data['choices'][0]['message']['content']
        return self._parse_analysis(analysis)

    def _get_system_prompt(self) -> str:
        """Системный промпт для API"""
        return """Ты опытный трейдер-аналитик. Анализируй сообщения из трейдинг-чатов 
                 и давай структурированную оценку сигналов."""

    def _create_trading_prompt(self, message: str, context: str) -> str:
        """Создание промпта для анализа"""
        return f"""
        🔍 АНАЛИЗ ТРЕЙДИНГ СИГНАЛА

        📝 СООБЩЕНИЕ: "{message.strip()}"
        📊 КОНТЕКСТ: {context}

        Проанализируй сообщение и верни JSON:
        {{
            "signal_type": "BUY/SELL/HOLD/DISCUSSION",
            "confidence_level": 1-10,
            "risk_level": "LOW/MEDIUM/HIGH",
            "assets_mentioned": ["тикеры"],
            "price_targets": {{"entry": "", "target": "", "stop_loss": ""}},
            "timeframe": "SHORT/MEDIUM/LONG_TERM",
            "summary": "краткий вывод",
            "recommendation": "рекомендация",
            "key_risks": "риски"
        }}"""

    def _parse_analysis(self, analysis_text: str) -> Dict[str, Any]:
        """Парсинг результата анализа"""
        try:
            json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
            if not json_match:
                return {"raw_analysis": analysis_text}
                
            data = json.loads(json_match.group())
            return TradingAnalysis(**data).__dict__
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка парсинга JSON: {e}")
            return {"raw_analysis": analysis_text}
        except Exception as e:
            logger.error(f"Ошибка обработки анализа: {e}")
            return {"error": str(e), "raw_analysis": analysis_text}

def main():
    """Тестовый запуск"""
    analyzer = DeepSeekTradingAnalyzer()
    test_message = "BUY PEPE NOW! Target 0.000012, stop loss 0.000008. Chart looks bullish!"
    
    logger.info("🧪 Тестирование анализатора...")
    result = analyzer.analyze_message(test_message, "Test Channel")
    print("📊 Результат анализа:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()