import unittest
import time
from mock_server import run_mock_server
from deepseek_analyzer import DeepSeekTradingAnalyzer


class TestWithMockServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Запускаем мок-сервер
        cls.server, cls.thread = run_mock_server(port=5000)
        # Небольшая пауза, чтобы сервер поднялся
        time.sleep(0.2)

    @classmethod
    def tearDownClass(cls):
        # Останавливаем сервер
        try:
            cls.server.shutdown()
        except Exception:
            pass
        cls.thread.join(timeout=1)

    def test_analyze_with_mock(self):
        analyzer = DeepSeekTradingAnalyzer()
        # Перекрываем URL на локальный мок
        analyzer.api_url = 'http://127.0.0.1:5000/v1/chat/completions'
        analyzer.api_key = 'test'
        analyzer.session.headers.update({
            'Authorization': 'Bearer test'
        })

        result = analyzer.analyze_message("Покупаем BTC по 35000$, цель 40000$", "Тестовый канал")

        # Проверяем что распарсили корректно
        self.assertIn('signal_type', result)
        self.assertEqual(result.get('signal_type'), 'BUY')
        self.assertIsInstance(result.get('assets_mentioned'), list)


if __name__ == '__main__':
    unittest.main()
