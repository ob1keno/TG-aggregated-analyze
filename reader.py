import time
import json
import logging
from typing import Callable, Dict, Any, Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MessageReader:
    """Прототип reader'а с поддержкой режима 'mock'.

    В mock режиме он просто генерирует тестовые сообщения и передаёт их в обработчик.
    В будущем сюда можно добавить Telethon/pyrogram интеграцию.
    """

    def __init__(self, mode: str = "mock", mock_count: int = 3):
        self.mode = mode
        self.mock_count = mock_count
        self._running = False

    def start(self, handler: Callable[[Dict[str, Any]], Any]):
        """Запускает reader и передаёт сообщения в handler.

        handler получает словарь с полями: text, author, chat_id, message_id, topic_id, timestamp
        """
        self._running = True
        if self.mode == "mock":
            self._run_mock(handler)
        else:
            raise NotImplementedError("Только mock режим реализован в прототипе")

    def stop(self):
        self._running = False

    def _run_mock(self, handler: Callable[[Dict[str, Any]], Any]):
        for i in range(1, self.mock_count + 1):
            if not self._running:
                break
            msg = {
                "text": f"Тестовое сообщение #{i}: покупаем BTC по 35000$, цель 40000$",
                "author": "test_user",
                "chat_id": -1001234567890,
                "message_id": i,
                "topic_id": None,
                "timestamp": int(time.time())
            }
            logger.info(f"Mock reader -> sending message #{i}")
            try:
                handler(msg)
            except Exception as e:
                logger.exception(f"Ошибка в обработчике сообщения: {e}")
            time.sleep(0.5)
