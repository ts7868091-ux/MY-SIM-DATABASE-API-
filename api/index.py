from flask import Flask, request, jsonify, render_template_string
import httpx
import asyncio

app = Flask(__name__)

# Core Source API
SAVITAR_API = "https://pak-data-three.vercel.app/api/lookup?query="

# Aapka Pasandida VIP Dashboard Design
VIP_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TALHA SIM & CNIC Intelligence | VIP API</title>
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
            background-image: radial-gradient(circle at 10% 10%, rgba(0, 230, 118, 0.05) 0%, transparent 20%),
                              radial-gradient(circle at 90% 90%, rgba(41, 121, 255, 0.05) 0%, transparent 20%);
        }

        .dashboard {
            width: 100%;
            max-width: 850px;
            background: var(--card-bg);
            backdrop-filter: blur(15px);
            border: 1px solid var(--card-border);
            border-radius: 24px;
            padding: 40px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
        }

        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 40px;
            border-bottom: 1px solid var(--card-border);
            padding-bottom: 20px;
        }
        .api-title { font-size: 22px; font-weight: 700; color: var(--text-main); }
        .api-title span { color: var(--primary); text-shadow: var(--glow); }
        
        .badge {
            font-size: 11px;
            font-weight: 600;
            padding: 6px 14px;
            border-radius: 50px;
            text-transform: uppercase;
        }
        .badge-vip { background: var(--secondary-dim); color: var(--secondary); border: 1px solid rgba(41, 121, 255, 0.2); }
        .badge-live { background: var(--primary-dim); color: var(--primary); border: 1px solid rgba(0, 230, 118, 0.2); box-shadow: var(--glow); }

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
        }
        .metric-label { font-size: 11px; color: var(--text-muted); text-transform: uppercase; }
        .metric-value { font-size: 18px; font-weight: 600; color: var(--text-main); }

        .code-block {
            background: #010101;
            padding: 20px;
            border-radius: 12px;
            font-family: 'Consolas', monospace;
            font-size: 13px;
            color: #d1d5db;
            border: 1px solid #1a1b26;
            margin-top: 10px;
        }
        .method { color: var(--primary); font-weight: bold; }

        footer {
            margin-top: 40px;
            text-align: center;
            font-size: 11px;
            color: var(--text-muted);
            border-top: 1px solid var(--card-border);
            padding-top: 20px;
        }
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="top-bar">
            <div class="api-title"><span>TALHA</span> INTELLIGENCE</div>
            <div class="status-group">
                <span class="badge badge-vip">PREMIUM VIP</span>
                <span class="badge badge-live">● SYSTEM LIVE</span>
            </div>
        </div>

        <div class="metrics">
            <div class="metric-card">
                <div class="metric-label">Developer</div>
                <div class="metric-value">Talha</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Search Engine</div>
                <div class="metric-value" style="color: var(--primary);">CNIC Deep-Search v3</div>
            </div>
        </div>

        <h3 style="font-size: 16px; margin-bottom: 10px;">API ENDPOINT</h3>
        <div class="code-block">
            <span class="method">GET</span> /api/lookup?query=<span style="color: #6ee7b7;">03XXXXXXXXX</span>
        </div>

        <footer>
            POWERED BY TALHA SECURE GATEWAY © 2026 | ALL DATA PROXIED
        </footer>
    </div>
</body>
</html>
"""

async def fetch_api(query_val):
    try:
        async with httpx.AsyncClient(timeout=25.0, verify=False) as client:
            response = await client.get(f"{SAVITAR_API}{query_val}")
            return response.json()
    except:
        return None

@app.route('/')
def home():
    return render_template_string(VIP_HTML)

@app.route('/api/lookup')
def lookup():
    query = request.args.get('query')
    if not query:
        return jsonify({"status": "error", "message": "No query", "developer": "Talha"}), 400

    # Step 1: Initial Search
    data = asyncio.run(fetch_api(query))
    
    # Step 2: Clean Error Logic
    if not data or not data.get("results") or len(data.get("results")) == 0:
        return jsonify({
            "status": "fail",
            "message": "Record Not Available",
            "developer": "Talha"
        }), 404

    # Step 3: Deep Search logic
    final_results = data.get("results", [])
    cnic = final_results[0].get("cnic")

    # Smart Check: Agar query mobile number tha, to CNIC se mazeed records nikalein
    if cnic and cnic != "N/A" and query != cnic:
        deep_data = asyncio.run(fetch_api(cnic))
        if deep_data and deep_data.get("results"):
            final_results = deep_data["results"]

    # Step 4: Final Custom Response
    return jsonify({
        "status": "success",
        "developer": "Talha",
        "query": query,
        "results_count": len(final_results),
        "results": final_results,
        "system_notice": "Deep search completed via CNIC"
    })
    
