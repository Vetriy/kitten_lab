import os
import socket
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

NODE_ID = os.getenv("NODE_ID", socket.gethostname()[-4:])
NODE_COLOR = os.getenv("NODE_COLOR", "#6C5CE7")


@app.route("/")
def home():
    html = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Node {NODE_ID}</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, {NODE_COLOR} 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }}
            .card {{
                background: white;
                border-radius: 24px;
                padding: 40px;
                max-width: 500px;
                width: 100%;
                text-align: center;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                animation: slideIn 0.5s ease;
            }}
            @keyframes slideIn {{
                from {{ opacity: 0; transform: translateY(20px); }}
                to {{ opacity: 1; transform: translateY(0); }}
            }}
            .emoji {{ font-size: 64px; margin-bottom: 20px; }}
            h1 {{
                color: #2D3436;
                font-size: 28px;
                margin-bottom: 10px;
            }}
            .node-id {{
                display: inline-block;
                background: {NODE_COLOR};
                color: white;
                padding: 8px 24px;
                border-radius: 50px;
                font-weight: 600;
                font-size: 18px;
                margin: 15px 0;
            }}
            .info {{
                color: #636E72;
                margin: 20px 0;
                line-height: 1.6;
            }}
            .refresh {{
                background: #6C5CE7;
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 12px;
                font-size: 16px;
                cursor: pointer;
                transition: transform 0.2s, background 0.2s;
                margin-top: 20px;
            }}
            .refresh:hover {{
                background: #5B4CDB;
                transform: scale(1.05);
            }}
            .footer {{
                margin-top: 30px;
                font-size: 12px;
                color: #B2BEC3;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="emoji">🐱</div>
            <h1>Привет от ноды!</h1>
            <div class="node-id">Node {NODE_ID}</div>
            <p class="info">
                Этот запрос был обработан сервером с идентификатором <strong>{NODE_ID}</strong>.<br>
                Обновите страницу, чтобы увидеть балансировку нагрузки в действии!
            </p>
            <button class="refresh" onclick="location.reload()">Обновить</button>
            <p class="footer">
                Hostname: {socket.gethostname()}<br>
                Load Balancer: Nginx Round-Robin
            </p>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "node_id": NODE_ID,
        "hostname": socket.gethostname()
    })


@app.route("/api/node")
def node_info():
    return jsonify({
        "node_id": NODE_ID,
        "hostname": socket.gethostname(),
        "color": NODE_COLOR
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)