from flask import Flask, request, jsonify
import httpx

app = Flask(__name__)

SAVITAR_API = "https://pak-data-three.vercel.app/api/lookup?query="

def fetch_api(query):
    try:
        with httpx.Client(timeout=60.0) as client:
            r = client.get(SAVITAR_API + query)
            if r.status_code == 200:
                return r.json()
    except:
        return None
    return None

@app.route("/")
def home():
    return "Talha Intelligence API Running 🚀"

@app.route("/api/lookup")
def lookup():
    query = request.args.get("query")

    if not query:
        return jsonify({"status": "error", "message": "No query"}), 400

    data = fetch_api(query)

    if not data or not data.get("results"):
        return jsonify({
            "status": "fail",
            "message": "Record Not Available"
        }), 404

    # Deep CNIC Search
    first = data["results"][0]
    cnic = first.get("cnic")

    if cnic and cnic != query:
        deep = fetch_api(cnic)
        if deep and deep.get("results"):
            data = deep

    return jsonify({
        "status": "success",
        "query": query,
        "results_count": len(data["results"]),
        "results": data["results"]
    })

if __name__ == "__main__":
    app.run()
