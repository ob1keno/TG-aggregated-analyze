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

MONITORING_CHANNELS = [
    "@channel1",
    "@channel2", 
    "@channel3"
]

ANALYSIS_PROMPTS = {
    'trading_signal': """
    Анализ торгового сигнала...
    """,
    'news_analysis': """
    Анализ новостей...
    """,
    'technical_analysis': """
    Анализ технического анализа...
    """
}