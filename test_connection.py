import requests
from dotenv import load_dotenv
import os

def test_api_connection():
    # Загружаем переменные окружения
    load_dotenv()
    
    api_key = os.getenv("DEEPSEEK_API_KEY")
    api_url = os.getenv("DEEPSEEK_API_URL")
    
    print(f"Проверяем подключение к API...")
    print(f"URL: {api_url}")
    print(f"API Key: {api_key[:8]}..." if api_key else "API Key не найден")
    
    try:
        # Пробуем простой запрос к API
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Простой запрос для проверки соединения
        response = requests.get(
            api_url.replace("/chat/completions", ""),  # Базовый URL API
            headers=headers,
            timeout=5
        )
        
        print(f"\nСтатус ответа: {response.status_code}")
        print(f"Ответ API: {response.text[:200]}")  # Показываем первые 200 символов ответа
        
        # Проверяем DNS резолвинг
        print("\nПроверка DNS резолвинга...")
        import socket
        host = api_url.split("//")[-1].split("/")[0]
        ip = socket.gethostbyname(host)
        print(f"DNS резолвинг {host} -> {ip}")
        
    except requests.exceptions.RequestException as e:
        print(f"\nОшибка при подключении: {str(e)}")
    except socket.gaierror as e:
        print(f"\nОшибка DNS резолвинга: {str(e)}")

if __name__ == "__main__":
    test_api_connection()