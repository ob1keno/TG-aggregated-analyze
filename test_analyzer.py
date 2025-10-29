from deepseek_analyzer import DeepSeekTradingAnalyzer
from deepseek_config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL
import unittest

class TestDeepSeekAnalyzer(unittest.TestCase):
    def setUp(self):
        """Подготовка к тестам"""
        self.analyzer = DeepSeekTradingAnalyzer()
        
    def test_config_loaded(self):
        """Проверка загрузки конфигурации"""
        self.assertIsNotNone(DEEPSEEK_API_KEY, "API ключ не загружен")
        self.assertIsNotNone(DEEPSEEK_API_URL, "API URL не загружен")
        
    def test_analyzer_initialization(self):
        """Проверка инициализации анализатора"""
        self.assertEqual(self.analyzer.api_key, DEEPSEEK_API_KEY)
        self.assertEqual(self.analyzer.api_url, DEEPSEEK_API_URL)
        
    def test_message_analysis(self):
        """Проверка анализа сообщения"""
        message = "Покупаем BTC по 35000$, цель 40000$, стоп 33000$"
        result = self.analyzer.analyze_message(message, "Тестовый канал")
        
        # Проверяем наличие всех необходимых полей
        self.assertIn('signal_type', result, "Отсутствует тип сигнала")
        self.assertIn('confidence_level', result, "Отсутствует уровень уверенности")
        self.assertIn('risk_level', result, "Отсутствует уровень риска")
        self.assertIn('assets_mentioned', result, "Отсутствует список активов")
        self.assertIn('price_targets', result, "Отсутствуют целевые цены")
        
        # Проверяем типы данных
        self.assertIsInstance(result.get('assets_mentioned', []), list, "assets_mentioned должен быть списком")
        self.assertIsInstance(result.get('price_targets', {}), dict, "price_targets должен быть словарем")

if __name__ == "__main__":
    unittest.main()
    
    # Анализируем сообщение
    result = analyzer.analyze_message(message, "Тестовый канал")
    
    # Выводим результат
    print("\nРезультат анализа:")
    print("-" * 50)
    print(f"Тип сигнала: {result.get('signal_type', 'Не определен')}")
    print(f"Уверенность: {result.get('confidence_level', 'Не определена')}")
    print(f"Уровень риска: {result.get('risk_level', 'Не определен')}")
    print(f"Упомянутые активы: {', '.join(result.get('assets_mentioned', []))}")
    print(f"Целевые цены: {result.get('price_targets', {})}")
    print(f"Временной горизонт: {result.get('timeframe', 'Не определен')}")
    print(f"Итог: {result.get('summary', 'Нет данных')}")
    print(f"Рекомендация: {result.get('recommendation', 'Нет данных')}")
    print(f"Ключевые риски: {result.get('key_risks', 'Не определены')}")

if __name__ == "__main__":
    test_simple()