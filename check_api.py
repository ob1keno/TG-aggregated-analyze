import requests
from dotenv import load_dotenv
import os
import json

def check_api_key():
    # Загружаем переменные окружения
    load_dotenv()
    
    api_key = os.getenv("DEEPSEEK_API_KEY")
    api_url = "https://api.deepseek.com/v1"  # Базовый URL
    
    print("🔑 Проверка API ключа")
    print(f"API Key: {api_key[:8]}..." if api_key else "API Key не найден")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # Пробуем получить информацию о ключе
        response = requests.get(
            f"{api_url}/key-info",  # Endpoint для проверки ключа
            headers=headers,
            timeout=10
        )
        
        print("\n📡 Ответ сервера:")
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 200:
            info = response.json()
            print("\n✅ Информация о ключе:")
            print(json.dumps(info, indent=2, ensure_ascii=False))
        elif response.status_code == 401:
            print("\n❌ Ошибка: Неверный API ключ")
        elif response.status_code == 402:
            print("\n❌ Ошибка: Требуется оплата или пополнение баланса")
        else:
            print(f"\n❌ Ошибка: {response.text}")
        
        # Проверяем доступные модели
        print("\n🤖 Проверка доступных моделей...")
        models_response = requests.get(
            f"{api_url}/models",
            headers=headers,
            timeout=10
        )
        
        if models_response.status_code == 200:
            models = models_response.json()
            print("\nДоступные модели:")
            print(json.dumps(models, indent=2, ensure_ascii=False))
        else:
            print(f"\n❌ Ошибка при получении списка моделей: {models_response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Ошибка при подключении: {str(e)}")

if __name__ == "__main__":
    check_api_key()