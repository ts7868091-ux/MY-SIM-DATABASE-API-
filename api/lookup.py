from flask import Flask, request, jsonify, render_template_string
import httpx
import asyncio

app = Flask(__name__)

# Savitar API (Original Source)
SAVITAR_API = "https://pak-data-three.vercel.app/api/lookup?query="

# Stylish Dashboard UI
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Talha SIM Data API</title>
    <style>
        body { background-color: #0f172a; color: white; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: #1e293b; padding: 30px; border-radius: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.6); text-align: center; border: 1px solid #334155; }
        h1 { color: #38bdf8; }
        .status { color: #34d399; font-weight: bold; margin-top: 15px; border: 1px solid #059669; padding: 5px 15px; border-radius: 50px; display: inline-block; }
    </style>
</head>
<body>
    <div class="card">
        <h1>💫 TALHA DATA API</h1>
        <p>API is Running Successfully for your Bot.</p>
        <div class="status">● ONLINE</div>
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
        return jsonify({"error": "No query provided"}), 400

    async def fetch_data():
        try:
            async with httpx.AsyncClient(timeout=20.0, verify=False) as client:
                response = await client.get(f"{SAVITAR_API}{query}")
                return response.json()
        except:
            return None

    data = asyncio.run(fetch_data())

    if not data:
        return jsonify({"error": "Source API Down"}), 500

    # Custom Response
    return jsonify({
        "query": data.get("query", query),
        "results": data.get("results", []),
        "developer": "Talha",
        "status": "success"
    })
  
