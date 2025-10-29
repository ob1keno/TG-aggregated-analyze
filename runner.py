import os
import json
import logging
from deepseek_analyzer import DeepSeekTradingAnalyzer
from mock_server import run_mock_server
from reader import MessageReader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RESULTS_FILE = "analysis_results.jsonl"


def save_result(result: dict):
    # append result as json line
    with open(RESULTS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(result, ensure_ascii=False) + "\n")


def handle_message(msg: dict, analyzer: DeepSeekTradingAnalyzer):
    text = msg.get("text", "")
    chat = msg.get("chat_id")
    logger.info(f"Handling message {msg.get('message_id')} from chat {chat}")
    res = analyzer.analyze_message(text, f"chat:{chat}")
    # attach metadata
    out = {
        "message": msg,
        "analysis": res
    }
    save_result(out)
    logger.info(f"Saved analysis for message {msg.get('message_id')}")


def run_demo(mock_port: int = 5000):
    # Запускаем мок-сервер (DeepSeek mock)
    server, thread = run_mock_server(port=mock_port)
    logger.info(f"Mock server started on port {mock_port}")

    # Конфигурируем анализатор на локальный mock
    analyzer = DeepSeekTradingAnalyzer()
    analyzer.api_url = f"http://127.0.0.1:{mock_port}/v1/chat/completions"
    analyzer.api_key = "test"
    analyzer.session.headers.update({"Authorization": "Bearer test"})

    # Очищаем результатный файл
    if os.path.exists(RESULTS_FILE):
        os.remove(RESULTS_FILE)

    # Запускаем Reader в mock режиме
    reader = MessageReader(mode="mock", mock_count=5)

    def _handler(m):
        handle_message(m, analyzer)

    try:
        reader.start(_handler)
    finally:
        # Останавливаем мок-сервер
        try:
            server.shutdown()
        except Exception:
            pass
        thread.join(timeout=1)
        logger.info("Demo finished. Mock server stopped.")


if __name__ == "__main__":
    run_demo()
