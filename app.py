import os
import socket
import time
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

APP_NAME = os.getenv("APP_NAME", "devops-lab")
APP_VERSION = os.getenv("APP_VERSION", "local")
PORT = int(os.getenv("PORT", "3000"))


PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>TEOS DevOps Lab</title>
  <style>
    :root {
      --bg: #0b1020;
      --panel: rgba(255, 255, 255, 0.08);
      --panel-strong: rgba(255, 255, 255, 0.13);
      --text: #f8fafc;
      --muted: #aab4c0;
      --accent: #5eead4;
      --accent-2: #60a5fa;
      --ok: #22c55e;
      --warning: #f59e0b;
      --border: rgba(255, 255, 255, 0.14);
      --shadow: 0 24px 80px rgba(0, 0, 0, 0.35);
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      min-height: 100vh;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--text);
      background:
        radial-gradient(circle at 15% 20%, rgba(94, 234, 212, 0.20), transparent 28%),
        radial-gradient(circle at 80% 10%, rgba(96, 165, 250, 0.20), transparent 30%),
        radial-gradient(circle at 50% 95%, rgba(168, 85, 247, 0.18), transparent 35%),
        var(--bg);
    }

    .page {
      width: min(1120px, calc(100% - 32px));
      margin: 0 auto;
      padding: 56px 0;
    }

    .hero {
      display: grid;
      grid-template-columns: 1.3fr 0.7fr;
      gap: 24px;
      align-items: stretch;
    }

    .card {
      background: linear-gradient(180deg, var(--panel), rgba(255,255,255,0.045));
      border: 1px solid var(--border);
      border-radius: 28px;
      box-shadow: var(--shadow);
      backdrop-filter: blur(18px);
    }

    .hero-main {
      padding: 40px;
      position: relative;
      overflow: hidden;
    }

    .hero-main::after {
      content: "";
      position: absolute;
      width: 260px;
      height: 260px;
      right: -80px;
      top: -90px;
      background: radial-gradient(circle, rgba(94, 234, 212, 0.28), transparent 65%);
      pointer-events: none;
    }

    .eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      padding: 8px 12px;
      border-radius: 999px;
      background: rgba(34, 197, 94, 0.12);
      border: 1px solid rgba(34, 197, 94, 0.28);
      color: #bbf7d0;
      font-size: 14px;
      font-weight: 700;
    }

    .pulse {
      width: 9px;
      height: 9px;
      border-radius: 50%;
      background: var(--ok);
      box-shadow: 0 0 0 8px rgba(34, 197, 94, 0.12);
    }

    h1 {
      margin: 28px 0 14px;
      font-size: clamp(40px, 6vw, 76px);
      line-height: 0.95;
      letter-spacing: -0.06em;
    }

    .lead {
      max-width: 720px;
      color: var(--muted);
      font-size: 19px;
      line-height: 1.7;
      margin: 0;
    }

    .highlight {
      color: var(--accent);
      font-weight: 800;
    }

    .hero-side {
      padding: 28px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      gap: 16px;
    }

    .metric {
      padding: 18px;
      border-radius: 20px;
      background: var(--panel-strong);
      border: 1px solid var(--border);
    }

    .metric span {
      display: block;
      color: var(--muted);
      font-size: 13px;
      margin-bottom: 8px;
    }

    .metric strong {
      display: block;
      font-size: 21px;
      word-break: break-word;
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
      margin-top: 24px;
    }

    .feature {
      padding: 24px;
      min-height: 190px;
    }

    .icon {
      width: 42px;
      height: 42px;
      display: grid;
      place-items: center;
      border-radius: 14px;
      background: linear-gradient(135deg, rgba(94,234,212,0.22), rgba(96,165,250,0.22));
      border: 1px solid var(--border);
      font-size: 21px;
      margin-bottom: 18px;
    }

    h2 {
      margin: 0 0 10px;
      font-size: 20px;
      letter-spacing: -0.02em;
    }

    .feature p {
      margin: 0;
      color: var(--muted);
      line-height: 1.6;
      font-size: 15px;
    }

    .status {
      margin-top: 24px;
      padding: 26px;
    }

    .status-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      margin-bottom: 18px;
    }

    .status-header h2 {
      font-size: 24px;
    }

    .badge {
      padding: 8px 12px;
      border-radius: 999px;
      background: rgba(96, 165, 250, 0.13);
      border: 1px solid rgba(96, 165, 250, 0.32);
      color: #bfdbfe;
      font-size: 13px;
      font-weight: 700;
    }

    .kv {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
    }

    .kv div {
      padding: 16px;
      border-radius: 16px;
      background: rgba(0, 0, 0, 0.16);
      border: 1px solid var(--border);
    }

    .kv span {
      display: block;
      color: var(--muted);
      font-size: 12px;
      margin-bottom: 8px;
    }

    .kv strong {
      display: block;
      font-size: 15px;
      word-break: break-word;
    }

    .footer {
      color: var(--muted);
      text-align: center;
      margin-top: 28px;
      font-size: 14px;
    }

    code {
      color: #c4b5fd;
    }

    @media (max-width: 900px) {
      .hero {
        grid-template-columns: 1fr;
      }

      .grid {
        grid-template-columns: 1fr;
      }

      .kv {
        grid-template-columns: 1fr;
      }

      .hero-main {
        padding: 30px;
      }
    }
  </style>
</head>
<body>
  <main class="page">
    <section class="hero">
      <div class="card hero-main">
        <div class="eyebrow">
          <span class="pulse"></span>
          Live DevOps Lab
        </div>

        <h1>TEOS DevOps<br>Portfolio Lab</h1>

        <p class="lead">
          This application is deployed through a real CI/CD pipeline:
          <span class="highlight">GitHub Actions</span> builds a Docker image,
          publishes it to <span class="highlight">GHCR</span>, connects to a Linux server over SSH,
          pulls the new image, restarts Docker Compose and verifies health checks.
        </p>
      </div>

      <aside class="card hero-side">
        <div class="metric">
          <span>App:</span>
          <strong>{{ app_name }}</strong>
        </div>

        <div class="metric">
          <span>Version:</span>
          <strong>{{ app_version }}</strong>
        </div>

        <div class="metric">
          <span>Hostname:</span>
          <strong>{{ hostname }}</strong>
        </div>

        <div class="metric">
          <span>Request path:</span>
          <strong>{{ path }}</strong>
        </div>
      </aside>
    </section>

    <section class="grid">
      <article class="card feature">
        <div class="icon">🐳</div>
        <h2>Dockerized app</h2>
        <p>
          The Python Flask application runs inside a Docker container built by CI
          and pulled by the production server.
        </p>
      </article>

      <article class="card feature">
        <div class="icon">🚀</div>
        <h2>Automated deploy</h2>
        <p>
          Merging into <code>main</code> triggers build, push to registry and remote deployment
          to the server through GitHub Actions.
        </p>
      </article>

      <article class="card feature">
        <div class="icon">🌐</div>
        <h2>Nginx reverse proxy</h2>
        <p>
          Nginx routes traffic to the application service and can distribute requests
          across scaled containers.
        </p>
      </article>

      <article class="card feature">
        <div class="icon">📦</div>
        <h2>GHCR registry</h2>
        <p>
          Images are stored in GitHub Container Registry with tags for deployment
          and repeatable releases.
        </p>
      </article>

      <article class="card feature">
        <div class="icon">🧪</div>
        <h2>Smoke tested</h2>
        <p>
          CI checks compose configuration, builds the image, starts services and verifies
          health/API responses before deployment.
        </p>
      </article>

      <article class="card feature">
        <div class="icon">📈</div>
        <h2>Scalable service</h2>
        <p>
          Multiple app containers can run behind Nginx. Refreshing requests can land
          on different container hostnames.
        </p>
      </article>
    </section>

    <section class="card status">
      <div class="status-header">
        <h2>Runtime status</h2>
        <span class="badge">healthy</span>
      </div>

      <div class="kv">
        <div>
          <span>Container hostname</span>
          <strong>{{ hostname }}</strong>
        </div>
        <div>
          <span>Timestamp UTC</span>
          <strong>{{ timestamp }}</strong>
        </div>
        <div>
          <span>Client IP</span>
          <strong>{{ client_ip }}</strong>
        </div>
        <div>
          <span>Backend port</span>
          <strong>{{ port }}</strong>
        </div>
      </div>
    </section>

    <p class="footer">
      Built as a hands-on DevOps training project: Linux, Docker, Docker Compose,
      Nginx, GitHub Actions, GHCR and SSH deployment.
    </p>
  </main>
</body>
</html>
"""


def page():
    return render_template_string(
        PAGE,
        app_name=APP_NAME,
        app_version=APP_VERSION,
        hostname=socket.gethostname(),
        path=request.path,
        timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        client_ip=request.headers.get("X-Forwarded-For", request.remote_addr),
        port=PORT,
    )


@app.route("/")
def index():
    return page()


@app.route("/api/")
def api_index():
    return page()


@app.route("/api/info")
def api_info():
    return jsonify(
        {
            "app": APP_NAME,
            "version": APP_VERSION,
            "hostname": socket.gethostname(),
            "path": request.path,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "ok",
        }
    )


@app.route("/health")
def health():
    return "OK\n", 200


@app.route("/api/slow")
def slow():
    time.sleep(10)
    return jsonify(
        {
            "status": "ok",
            "message": "Slow endpoint completed",
            "hostname": socket.gethostname(),
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
