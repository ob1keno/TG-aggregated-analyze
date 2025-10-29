import sqlite3
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

class AnalysisDB:
    """SQLite хранилище для результатов анализа."""
    
    def __init__(self, db_path: str = "analysis.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Инициализация БД и создание таблиц."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id INTEGER NOT NULL,
                    chat_id INTEGER NOT NULL,
                    topic_id INTEGER,
                    author TEXT,
                    text TEXT NOT NULL,
                    timestamp INTEGER NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS analysis_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id INTEGER NOT NULL,
                    signal_type TEXT,
                    confidence_level INTEGER,
                    risk_level TEXT,
                    assets_mentioned TEXT,  -- JSON array
                    price_targets TEXT,     -- JSON object
                    timeframe TEXT,
                    summary TEXT,
                    recommendation TEXT,
                    key_risks TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (message_id) REFERENCES messages(id)
                )
            """)
            # Индексы для быстрого поиска
            conn.execute("CREATE INDEX IF NOT EXISTS idx_messages_chat ON messages(chat_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_messages_topic ON messages(topic_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_analysis_signal ON analysis_results(signal_type)")

    def save_analysis(self, message: Dict[str, Any], analysis: Dict[str, Any]) -> int:
        """Сохраняет сообщение и результат анализа."""
        with sqlite3.connect(self.db_path) as conn:
            # Сохраняем сообщение
            cursor = conn.execute(
                """
                INSERT INTO messages (message_id, chat_id, topic_id, author, text, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    message["message_id"],
                    message["chat_id"],
                    message.get("topic_id"),
                    message.get("author"),
                    message["text"],
                    message["timestamp"]
                )
            )
            msg_db_id = cursor.lastrowid

            # Сохраняем анализ
            conn.execute(
                """
                INSERT INTO analysis_results 
                (message_id, signal_type, confidence_level, risk_level, 
                assets_mentioned, price_targets, timeframe, summary, 
                recommendation, key_risks)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    msg_db_id,
                    analysis.get("signal_type"),
                    analysis.get("confidence_level"),
                    analysis.get("risk_level"),
                    json.dumps(analysis.get("assets_mentioned", []), ensure_ascii=False),
                    json.dumps(analysis.get("price_targets", {}), ensure_ascii=False),
                    analysis.get("timeframe"),
                    analysis.get("summary"),
                    analysis.get("recommendation"),
                    analysis.get("key_risks")
                )
            )
            return msg_db_id

    def get_latest_analyses(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Получает последние результаты анализа."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """
                SELECT 
                    m.message_id, m.chat_id, m.topic_id, m.author, m.text,
                    m.timestamp, ar.*
                FROM messages m
                JOIN analysis_results ar ON m.id = ar.message_id
                ORDER BY ar.created_at DESC
                LIMIT ?
                """,
                (limit,)
            )
            results = []
            for row in cursor:
                result = dict(row)
                # Преобразуем JSON-строки обратно в объекты
                result["assets_mentioned"] = json.loads(result["assets_mentioned"])
                result["price_targets"] = json.loads(result["price_targets"])
                results.append(result)
            return results

    def search_by_signal(self, signal_type: str) -> List[Dict[str, Any]]:
        """Поиск анализов по типу сигнала."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """
                SELECT 
                    m.message_id, m.chat_id, m.topic_id, m.author, m.text,
                    m.timestamp, ar.*
                FROM messages m
                JOIN analysis_results ar ON m.id = ar.message_id
                WHERE ar.signal_type = ?
                ORDER BY ar.created_at DESC
                """,
                (signal_type,)
            )
            results = []
            for row in cursor:
                result = dict(row)
                result["assets_mentioned"] = json.loads(result["assets_mentioned"])
                result["price_targets"] = json.loads(result["price_targets"])
                results.append(result)
            return results

    def search_by_asset(self, asset: str) -> List[Dict[str, Any]]:
        """Поиск анализов по упомянутому активу."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """
                SELECT 
                    m.message_id, m.chat_id, m.topic_id, m.author, m.text,
                    m.timestamp, ar.*
                FROM messages m
                JOIN analysis_results ar ON m.id = ar.message_id
                WHERE ar.assets_mentioned LIKE ?
                ORDER BY ar.created_at DESC
                """,
                (f'%"{asset}"%',)  # Поиск в JSON массиве
            )
            results = []
            for row in cursor:
                result = dict(row)
                result["assets_mentioned"] = json.loads(result["assets_mentioned"])
                result["price_targets"] = json.loads(result["price_targets"])
                results.append(result)
            return results