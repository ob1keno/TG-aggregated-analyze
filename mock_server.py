from flask import Flask, request, jsonify
import json
import threading


def create_app():
    app = Flask(__name__)

    @app.route('/v1/chat/completions', methods=['POST', 'GET'])
    def chat_completions():
        # Простая заглушка: возвращаем строку с JSON в поле message.content
        analysis = {
            "signal_type": "BUY",
            "confidence_level": 8,
            "risk_level": "MEDIUM",
            "assets_mentioned": ["BTC"],
            "price_targets": {"entry": "35000", "target": "40000", "stop_loss": "33000"},
            "timeframe": "SHORT",
            "summary": "Позитивный сигнал",
            "recommendation": "Вход частичный",
            "key_risks": "Волатильность"
        }
        content = json.dumps(analysis, ensure_ascii=False)
        return jsonify({"choices": [{"message": {"content": content}}]})

    return app


def run_mock_server(host='127.0.0.1', port=5000):
    """Запускает сервер в фоновом потоке и возвращает объект сервера (werkzeug) для shutdown."""
    from werkzeug.serving import make_server

    app = create_app()
    server = make_server(host, port, app)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    return server, thread
