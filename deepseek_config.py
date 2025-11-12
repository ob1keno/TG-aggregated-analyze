"""
DeepSeek API Configuration - Безопасная версия
Читает все конфиденциальные данные из переменных окружения
"""

from dotenv import load_dotenv
import os

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем API ключ из переменных окружения
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")

# Проверяем наличие обязательных переменных окружения
if not DEEPSEEK_API_KEY:
    raise ValueError(
        "DEEPSEEK_API_KEY не найден в переменных окружения!\n"
        "Создайте файл .env и добавьте:\n"
        "DEEPSEEK_API_KEY=ваш-новый-api-ключ"
    )

# Настройки по умолчанию
DEFAULT_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-coder")
DEFAULT_TEMPERATURE = float(os.getenv("DEEPSEEK_TEMPERATURE", "0.1"))
DEFAULT_MAX_TOKENS = int(os.getenv("DEEPSEEK_MAX_TOKENS", "2048"))

# Категории веток для анализа
КАТЕГОРИИ_ВЕТОК = {
    'ido_ico': {
        'ключевые_слова': ['ico', 'ido', 'сид', 'пресейл', 'привата', 'паблик'],
        'приоритет': 'высокий',
        'требует_действий': True
    },
    'деген': {
        'ключевые_слова': ['метеор', 'альфа', 'колл', 'инфа', 'админ'],
        'фокус_на_админе': True,
        'приоритет': 'высокий',
        'требует_действий': True
    },
    'премаркет': {
        'ключевые_слова': ['пресейл', 'спред', 'листинг', 'запуск', 'открытие'],
        'приоритет': 'средний',
        'отслеживание_цен': True
    },
    'важное': {
        'ключевые_слова': ['важно', 'срочно', 'внимание', 'алерт', 'успеть'],
        'приоритет': 'критический',
        'требует_действий': True
    }
}

ШАБЛОНЫ_АНАЛИЗА = {
    'ido_ico': """
    Анализ ICO/IDO сообщения:
    1. Определить стадию (сид/привата/паблик)
    2. Цены и условия входа
    3. Важные даты
    4. Требуемые действия
    5. Риски и особые условия
    """,
    'деген': """
    Анализ сообщения от админа:
    1. Тип информации (метеор/альфа/инсайд)
    2. Срочность и важность
    3. Необходимые действия
    4. Потенциальные риски
    5. Временные рамки
    """,
    'премаркет': """
    Анализ премаркета/спредов:
    1. Текущая цена и спред
    2. Изменение с прошлого апдейта
    3. Ликвидность и объём торгов
    4. Рекомендуемые действия
    5. Риски входа
    """,
    'важное': """
    Анализ важного сообщения:
    1. Суть требуемых действий
    2. Срочность выполнения
    3. Конкретные шаги
    4. Сроки исполнения
    5. Последствия пропуска
    """
}

# Настройки мониторинга
НАСТРОЙКИ_МОНИТОРИНГА = {
    'интервал_проверки': int(os.getenv("MONITOR_INTERVAL", "60")),  # секунды
    'макс_история': int(os.getenv("MAX_HISTORY", "100")),  # сообщений
    'приоритет_админских': os.getenv("PRIORITY_ADMIN", "true").lower() == "true",
    'оповещения_действий': os.getenv("ENABLE_NOTIFICATIONS", "true").lower() == "true"
}

def get_api_config():
    """Возвращает конфигурацию API"""
    return {
        'api_key': DEEPSEEK_API_KEY,
        'api_url': DEEPSEEK_API_URL,
        'model': DEFAULT_MODEL,
        'temperature': DEFAULT_TEMPERATURE,
        'max_tokens': DEFAULT_MAX_TOKENS
    }

def validate_config():
    """Проверяет корректность конфигурации"""
    if not DEEPSEEK_API_KEY:
        return False, "API ключ не установлен"
    
    if not DEEPSEEK_API_KEY.startswith('sk-'):
        return False, "Некорректный формат API ключа"
    
    if len(DEEPSEEK_API_KEY) < 20:
        return False, "API ключ слишком короткий"
    
    return True, "Конфигурация корректна"

# Автоматическая валидация при импорте
is_valid, message = validate_config()
if not is_valid:
    raise ValueError(f"Ошибка конфигурации DeepSeek: {message}")

print(f"✅ DeepSeek конфигурация загружена успешно")
print(f"   API URL: {DEEPSEEK_API_URL}")
print(f"   Модель: {DEFAULT_MODEL}")
print(f"   API ключ: {DEEPSEEK_API_KEY[:8]}...{DEEPSEEK_API_KEY[-4:]} (скрыт)")