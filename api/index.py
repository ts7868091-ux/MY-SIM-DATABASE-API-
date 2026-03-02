from flask import Flask, request, jsonify, render_template_string
import httpx
import asyncio

app = Flask(__name__)

# Core Source API
SAVITAR_API = "https://pak-data-three.vercel.app/api/lookup?query="

# VIP CSS & HTML Documentation
VIP_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TALHA INTEL - VIP API ACCESS</title>
    <style>
        :root { --accent: #00f2ff; --bg: #05070a; --glass: rgba(255, 255, 255, 0.03); --border: rgba(0, 242, 255, 0.2); }
        body { background: var(--bg); color: #fff; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; overflow: hidden; }
        .container { position: relative; width: 90%; max-width: 700px; padding: 40px; background: var(--glass); backdrop-filter: blur(15px); border: 1px solid var(--border); border-radius: 30px; box-shadow: 0 0 40px rgba(0, 242, 255, 0.1); }
        .header { border-bottom: 2px solid var(--border); padding-bottom: 20px; margin-bottom: 30px; }
        h1 { font-size: 28px; letter-spacing: 2px; color: var(--accent); margin: 0; text-transform: uppercase; font-weight: 800; }
        .badge { background: var(--accent); color: #000; padding: 4px 12px; border-radius: 4px; font-size: 10px; font-weight: bold; margin-top: 10px; display: inline-block; }
        .stats-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 30px; }
        .stat-box { background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px; border-left: 3px solid var(--accent); }
        .stat-label { font-size: 10px; color: #888; text-transform: uppercase; }
        .stat-val { font-size: 16px; font-weight: 600; color: #eee; }
        .doc-box { background: #000; padding: 20px; border-radius: 15px; border: 1px solid #111; font-family: monospace; position: relative; }
        .doc-box::before { content: "ENDPOINT"; position: absolute; top: -10px; left: 20px; background: var(--bg); padding: 0 10px; font-size: 10px; color: var(--accent); }
        .method { color: #00ff88; }
        .url { color: #aaa; }
        .query { color: var(--accent); }
        footer { margin-top: 30px; text-align: center; font-size: 11px; color: #444; letter-spacing: 2px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Talha Intelligence</h1>
            <span class="badge">PREMIUM VIP API V3</span>
        </div>
        <div class="stats-grid">
            <div class="stat-box">
                <div class="stat-label">System Developer</div>
                <div class="stat-val">Talha</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">System Status</div>
                <div class="stat-val" style="color:#00ff88;">● Operational</div>
            </div>
        </div>
        <div class="doc-box">
            <span class="method">GET</span> <span class="url">/api/lookup?</span><span class="query">query=03XXXXXXXXX</span>
            <br><br>
            <span style="color: #555;">// Smart CNIC Deep-Search is Enabled</span>
        </div>
        <footer>
            SECURED BY TALHA PROXY LAYER © 2026
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
        return jsonify({"status": "error", "message": "No query provided", "developer": "Talha"}), 400

    # Step 1: Search the number
    data = asyncio.run(fetch_api(query))
    
    # Step 2: Smart Error Check
    if not data or not data.get("results") or len(data.get("results")) == 0:
        return jsonify({
            "status": "fail",
            "message": "Record Not Available",
            "developer": "Talha"
        }), 404

    # Step 3: Deep Search Logic (CNIC based)
    final_results = data.get("results", [])
    cnic = final_results[0].get("cnic")

    # Agar user ne number diya tha aur humein CNIC mil gaya, to dobara pure CNIC ka data nikalein
    if cnic and cnic != "N/A" and query != cnic:
        deep_data = asyncio.run(fetch_api(cnic))
        if deep_data and deep_data.get("results"):
            final_results = deep_data["results"]

    # Step 4: Fully Customized Response
    return jsonify({
        "status": "success",
        "developer": "Talha",
        "query": query,
        "results_count": len(final_results),
        "results": final_results,
        "engine": "CNIC-Deep-Search-v3"
    })
