from flask import Flask, request, jsonify, render_template_string
import httpx

app = Flask(__name__)

# Savitar API Link
SAVITAR_API = "https://pak-data-three.vercel.app/api/lookup?query="

# HTML Template for the Landing Page
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Talha SIM Data API</title>
    <style>
        body { background-color: #0f172a; color: white; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: #1e293b; padding: 2rem; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); text-align: center; border: 1px solid #334155; }
        h1 { color: #38bdf8; margin-bottom: 0.5rem; }
        p { color: #94a3b8; }
        .status { display: inline-block; padding: 5px 15px; background: #065f46; color: #34d399; border-radius: 20px; font-size: 0.8rem; margin-top: 10px; }
        .footer { margin-top: 20px; font-size: 0.7rem; color: #64748b; }
    </style>
</head>
<body>
    <div class="card">
        <h1>💫 Talha Data API</h1>
        <p>Advanced SIM Database API is Running...</p>
        <div class="status">● API ONLINE</div>
        <div class="footer">Developed by Talha | Powering Telegram Bots</div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    # Jab koi browser mein link khole to ye page dikhega
    return render_template_string(HTML_PAGE)

@app.route('/api/lookup', methods=['GET'])
async def lookup():
    query = request.args.get('query')
    if not query:
        return jsonify({"status": "error", "message": "No query provided"}), 400

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{SAVITAR_API}{query}")
            data = response.json()

        # Apne naam ke saath result bhejain
        return jsonify({
            "query": data.get("query"),
            "results": data.get("results"),
            "developer": "Talha"
        })
    except:
        return jsonify({"status": "error", "message": "API Down"}), 500

if __name__ == '__main__':
    app.run(debug=True)

