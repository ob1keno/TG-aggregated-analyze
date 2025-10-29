from deepseek_analyzer import DeepSeekTradingAnalyzer

def test_simple():
    analyzer = DeepSeekTradingAnalyzer()
    
    # Тестовое сообщение
    message = "Покупаем BTC по 35000$, цель 40000$, стоп 33000$"
    
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