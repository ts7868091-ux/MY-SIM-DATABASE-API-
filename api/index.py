from flask import Flask, request, jsonify, render_template_string
import httpx
import asyncio

app = Flask(__name__)

# Original Data Source
SAVITAR_API = "https://pak-data-three.vercel.app/api/lookup?query="

# VIP Professional Documentation UI (Distinct from Savitar)
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Talha SIM & CNIC Intelligence | VIP API</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #00e676;
            --primary-dim: rgba(0, 230, 118, 0.1);
            --secondary: #2979ff;
            --secondary-dim: rgba(41, 121, 255, 0.1);
            --bg: #040509;
            --card-bg: rgba(20, 22, 31, 0.6);
            --card-border: rgba(255, 255, 255, 0.05);
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --glow: 0 0 20px rgba(0, 230, 118, 0.2);
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background-color: var(--bg);
            color: var(--text-main);
            font-family: 'Poppins', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
            overflow-x: hidden;
            background-image: radial-gradient(circle at 10% 10%, rgba(0, 230, 118, 0.05) 0%, transparent 20%),
                              radial-gradient(circle at 90% 90%, rgba(41, 121, 255, 0.05) 0%, transparent 20%);
        }

        .dashboard {
            width: 100%;
            max-width: 900px;
            background: var(--card-bg);
            backdrop-filter: blur(10px);
            border: 1px solid var(--card-border);
            border-radius: 24px;
            padding: 40px;
            position: relative;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
        }

        /* Top Bar */
        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
            border-bottom: 1px solid var(--card-border);
            padding-bottom: 20px;
        }
        .api-title { font-size: 20px; font-weight: 700; color: var(--text-main); letter-spacing: 0.5px; }
        .api-title span { color: var(--primary); text-shadow: var(--glow); }
        .status-group { display: flex; gap: 10px; }
        .badge {
            font-size: 11px;
            font-weight: 600;
            padding: 6px 14px;
            border-radius: 50px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .badge-vip { background: var(--secondary-dim); color: var(--secondary); border: 1px solid rgba(41, 121, 255, 0.2); }
        .badge-live { background: var(--primary-dim); color: var(--primary); border: 1px solid rgba(0, 230, 118, 0.2); box-shadow: var(--glow); }

        /* Welcome Section */
        .welcome { margin-bottom: 30px; }
        .welcome h2 { font-size: 28px; font-weight: 600; margin-bottom: 5px; }
        .welcome p { color: var(--text-muted); font-size: 14px; font-weight: 300; }

        /* Key Metrics */
        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        .metric-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--card-border);
            padding: 20px;
            border-radius: 16px;
            transition: all 0.3s ease;
        }
        .metric-card:hover { border-color: rgba(255, 255, 255, 0.1); background: rgba(255, 255, 255, 0.03); transform: translateY(-3px); }
        .metric-card.vip { border-color: rgba(41, 121, 255, 0.3); box-shadow: 0 0 15px rgba(41, 121, 255, 0.1); }
        .metric-label { font-size: 11px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px; }
        .metric-value { font-size: 18px; font-weight: 600; color: var(--text-main); }
        .metric-value.highlight { color: var(--primary); text-shadow: var(--glow); }

        /* Documentation Section */
        .doc-section { margin-bottom: 30px; }
        .section-header { font-size: 16px; font-weight: 600; color: var(--text-main); margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }
        .section-header::after { content: ""; flex: 1; height: 1px; background: var(--card-border); }
        
        /* Table/Info List */
        .info-list { font-size: 14px; color: #cbd5e1; }
        .info-item { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.02); }
        .info-key { color: var(--text-muted); font-weight: 400; }
        .info-value { font-weight: 500; text-align: right; }

        /* Code Block */
        .code-container { margin-top: 15px; }
        .code-header { font-size: 12px; color: var(--text-muted); margin-bottom: 5px; }
        .code-block {
            background: #010101;
            padding: 18px 25px;
            border-radius: 12px;
            font-family: 'Consolas', monospace;
            font-size: 13px;
            color: #d1d5db;
            overflow-x: auto;
            border: 1px solid #1a1b26;
            line-height: 1.5;
        }
        .method-get { color: var(--primary); font-weight: 600; }
        .param { color: #f472b6; }
        .value { color: #e2e8f0; }

        /* Footer */
        footer {
            margin-top: 50px;
            padding-top: 25px;
            border-top: 1px solid var(--card-border);
            text-align: center;
            font-size: 11px;
            color: var(--text-muted);
            letter-spacing: 0.5px;
        }

        /* Responsive */
        @media (max-width: 600px) {
            .dashboard { padding: 25px; }
            .top-bar { flex-direction: column; align-items: flex-start; gap: 10px; }
            .metrics { grid-template-columns: 1fr; }
            .welcome h2 { font-size: 22px; }
        }
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="top-bar">
            <div class="api-title"><span>TALHA</span> INTELLIGENCE</div>
            <div class="status-group">
                <span class="badge badge-vip">VIP ACCESS</span>
                <span class="badge badge-live">SYSTEM ONLINE</span>
            </div>
        </div>

        <div class="welcome">
            <h2>Core Dashboard</h2>
            <p>Advanced SIM & CNIC intelligence API with proxy-secured live fetch technology.</p>
        </div>

        <div class="metrics">
            <div class="metric-card">
                <div class="metric-label">Developer</div>
                <div class="metric-value highlighting">Talha</div>
            </div>
            <div class="metric-card vip">
                <div class="metric-label">License Type</div>
                <div class="metric-value" style="color: var(--secondary); font-weight: 700;">Premium VIP</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">API Version</div>
                <div class="metric-value highlight">v3.1</div>
            </div>
        </div>

        <div class="doc-section">
            <div class="section-header">USAGE GUIDELINES</div>
            <div class="info-list">
                <div class="info-item">
                    <span class="info-key">Lookup Method</span>
                    <span class="info-value">GET Request</span>
                </div>
                <div class="info-item">
                    <span class="info-key">Query Parameter</span>
                    <span class="info-value"><span class="param">query</span></span>
                </div>
                <div class="info-item">
                    <span class="info-key">Valid Format 1</span>
                    <span class="info-value">03XXXXXXXXX (11 Digits)</span>
                </div>
                <div class="info-item">
                    <span class="info-key">Valid Format 2</span>
                    <span class="info-value">13XXXXXXXXXXX (CNIC)</span>
                </div>
            </div>
        </div>

        <div class="doc-section">
            <div class="section-header">API ENDPOINT</div>
            <div class="code-container">
                <div class="code-header">Core Lookup Endpoint</div>
                <div class="code-block">
                    <span class="method-get">GET</span> /api/lookup?<span class="param">query</span>=<span class="value">03XXXXXXXXX</span>
                </div>
            </div>
            <div class="code-container">
                <div class="code-header">Live Example (Copy to Test)</div>
                <div class="code-block" style="color: var(--text-muted);">
                    https://my-sim-database-api.vercel.app/api/lookup?query=<span class="value" style="color: #6ee7b7;">03352438092</span>
                </div>
            </div>
        </div>

        <footer>
            PROPRIETARY INTELLIGENCE SYSTEM | DEVELOPED BY TALHA | ALL RIGHTS RESERVED © 2026
        </footer>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/api/lookup')
def lookup():
    query = request.args.get('query')
    if not query:
        return jsonify({"status": "error", "message": "No query provided"}), 400

    async def fetch_data():
        try:
            async with httpx.AsyncClient(timeout=25.0, verify=False) as client:
                response = await client.get(f"{SAVITAR_API}{query}")
                return response.json()
        except:
            return None

    data = asyncio.run(fetch_data())
    if not data:
        return jsonify({"status": "error", "message": "Source API Down"}), 500

    # Custom Response
    return jsonify({
        "query": data.get("query", query),
        "results": data.get("results", []),
        "developer": "Talha",
        "status": "success"
    })
  
