import requests
import json
from deepseek_config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL

class DeepSeekTradingAnalyzer:
    def __init__(self):
        self.api_key = DEEPSEEK_API_KEY
        self.api_url = DEEPSEEK_API_URL
        
    def analyze_message(self, message_text, channel_info=""):
        """Анализирует сообщение через DeepSeek API"""
        
        prompt = self.create_trading_prompt(message_text, channel_info)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system", 
                    "content": "Ты опытный трейдер-аналитик. Анализируй сообщения из трейдинг-чатов и давай структурированную оценку сигналов."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response_data = response.json()
            
            if 'choices' in response_data:
                analysis = response_data['choices'][0]['message']['content']
                return self.parse_analysis(analysis)
            else:
                return {"error": "Ошибка API", "response": response_data}
                
        except Exception as e:
            return {"error": f"Ошибка запроса: {str(e)}"}
    
    def create_trading_prompt(self, message, context):
        return f"""
        🔍 АНАЛИЗ ТРЕЙДИНГ СИГНАЛА
        
        📝 СООБЩЕНИЕ ДЛЯ АНАЛИЗА:
        "{message}"
        
        📊 КОНТЕКСТ:
        Канал: {context}
        
        🎯 ЗАДАЧА:
        Проанализируй это сообщение как трейдинг-сигнал и дай структурированную оценку.
        
        📋 ФОРМАТ ОТВЕТА (JSON):
        {{
            "signal_type": "BUY/SELL/HOLD/DISCUSSION",
            "confidence_level": 1-10,
            "risk_level": "LOW/MEDIUM/HIGH",
            "assets_mentioned": ["список", "тикеров"],
            "price_targets": {{"entry": "", "target": "", "stop_loss": ""}},
            "timeframe": "SHORT/MEDIUM/LONG_TERM",
            "summary": "краткий вывод",
            "recommendation": "детальная рекомендация",
            "key_risks": "основные риски"
        }}
        
        Проанализируй и верни ответ в указанном JSON формате.
        """
    
    def parse_analysis(self, analysis_text):
        """Парсит анализ от DeepSeek"""
        try:
            # Пытаемся найти JSON в ответе
            if '{' in analysis_text and '}' in analysis_text:
                json_start = analysis_text.find('{')
                json_end = analysis_text.rfind('}') + 1
                json_str = analysis_text[json_start:json_end]
                return json.loads(json_str)
            else:
                return {"raw_analysis": analysis_text}
        except:
            return {"raw_analysis": analysis_text}

# Тестовый запуск
if __name__ == "__main__":
    analyzer = DeepSeekTradingAnalyzer()
    
    # Тестовое сообщение
    test_message = "BUY PEPE NOW! Target 0.000012, stop loss 0.000008. Chart looks bullish!"
    
    print("🧪 Тестируем анализатор...")
    result = analyzer.analyze_message(test_message, "Test Channel")
    print("📊 Результат анализа:")
    print(json.dumps(result, indent=2, ensure_ascii=False))