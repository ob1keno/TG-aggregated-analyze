from dotenv import load_dotenv
import os

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем значения из переменных окружения
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL")

# Проверяем наличие необходимых переменных окружения
if not DEEPSEEK_API_KEY or not DEEPSEEK_API_URL:
    raise ValueError("Не найдены необходимые переменные окружения. Проверьте файл .env")

# Категории веток для анализа
THREAD_CATEGORIES = {
    'ido_ico': {
        'keywords': ['ico', 'ido', 'initial', 'offering', 'seed', 'private sale'],
        'priority': 'high',
        'requires_immediate_action': True
    },
    'degen': {
        'keywords': ['meteor', 'alpha', 'call'],
        'admin_focus': True,
        'priority': 'high',
        'action_required': True
    },
    'premarket': {
        'keywords': ['presale', 'spread', 'listing', 'launch'],
        'priority': 'medium',
        'price_tracking': True
    },
    'action_required': {
        'keywords': ['important', 'urgent', 'action', 'now', 'alert'],
        'priority': 'critical',
        'requires_immediate_action': True
    }
}

ANALYSIS_PROMPTS = {
    'ido_ico': """
    Анализ ICO/IDO сообщения:
    1. Определить стадию (seed/private/public)
    2. Цены и условия входа
    3. Важные даты
    4. Требуемые действия
    5. Риски и особые условия
    """,
    'degen': """
    Анализ сообщения от админа:
    1. Определить тип призыва к действию
    2. Срочность и важность
    3. Необходимые действия
    4. Потенциальные риски
    5. Временные рамки
    """,
    'premarket': """
    Анализ премаркета/спредов:
    1. Текущая цена и спред
    2. Изменение с последнего апдейта
    3. Ликвидность и объем
    4. Рекомендуемые действия
    5. Риски
    """,
    'action_required': """
    Анализ важного сообщения:
    1. Тип требуемого действия
    2. Срочность
    3. Шаги для выполнения
    4. Дедлайны
    5. Последствия невыполнения
    """
}

# Настройки мониторинга
MONITORING_CONFIG = {
    'check_interval': 60,  # секунды
    'max_history_load': 100,  # сообщений
    'admin_messages_priority': True,
    'action_alerts': True,
}