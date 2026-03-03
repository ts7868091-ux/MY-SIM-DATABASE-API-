from flask import Flask, request, jsonify
import httpx
import os

app = Flask(__name__)

# Original Source API
SOURCE_API = "https://pak-data-three.vercel.app/api/lookup?query="


# ---------------- FETCH FUNCTION ----------------
def fetch_api(query):
    try:
        with httpx.Client(timeout=90.0) as client:
            r = client.get(SOURCE_API + query)
            if r.status_code == 200:
                return r.json()
    except Exception:
        return None
    return None


# ---------------- HOME ROUTE ----------------
@app.route("/")
def home():
    return {
        "status": "running",
        "developer": "Talha",
        "message": "Talha Intelligence API is Live 🚀"
    }


# ---------------- LOOKUP ROUTE ----------------
@app.route("/api/lookup")
def lookup():
    query = request.args.get("query")

    if not query:
        return jsonify({
            "status": "error",
            "message": "No query provided"
        }), 400

    # First Search
    data = fetch_api(query)

    if not data or not data.get("results"):
        return jsonify({
            "status": "fail",
            "message": "Record Not Available"
        }), 404

    # Deep CNIC Search
    first_record = data["results"][0]
    cnic = first_record.get("cnic")

    if cnic and cnic != query:
        deep_data = fetch_api(cnic)
        if deep_data and deep_data.get("results"):
            data = deep_data

    return jsonify({
        "status": "success",
        "query": query,
        "results_count": len(data["results"]),
        "results": data["results"]
    })


# ---------------- RAILWAY PORT FIX ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
