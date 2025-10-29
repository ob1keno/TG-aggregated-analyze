import requests
from dotenv import load_dotenv
import os
import json

def test_api_request():
    load_dotenv()
    
    api_key = os.getenv("DEEPSEEK_API_KEY")
    api_url = os.getenv("DEEPSEEK_API_URL")
    
    print("🔄 Отправляем тестовый запрос...")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "user",
                "content": "Say 'Hello, world!'"
            }
        ],
        "temperature": 0.1
    }
    
    try:
        response = requests.post(
            api_url,
            headers=headers,
            json=data,
            timeout=10
        )
        
        print(f"\n📡 Статус ответа: {response.status_code}")
        print("\n📝 Ответ API:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Ошибка при запросе: {str(e)}")

if __name__ == "__main__":
    test_api_request()