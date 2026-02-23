from flask import Flask, jsonify, request
import json
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).parent
VENDORS_PATH = BASE_DIR / "data" / "vendors.json"
INVOICES_PATH = BASE_DIR / "data" / "invoices.json"

def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.get("/vendors/<vendor_id>")
def get_vendor(vendor_id: str):
    vendors = load_json(VENDORS_PATH)
    match = next((v for v in vendors if v["vendor_id"] == vendor_id), None)
    if not match:
        return jsonify({"error": "vendor_not_found"}), 404
    return jsonify(match)

@app.get("/invoices/exists")
def invoice_exists():
    invoice_id = request.args.get("invoice_id", "").strip()
    if not invoice_id:
        return jsonify({"error": "missing_invoice_id"}), 400

    invoices = load_json(INVOICES_PATH)
    exists = any(inv["invoice_id"] == invoice_id for inv in invoices)
    return jsonify({"invoice_id": invoice_id, "exists": exists})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
