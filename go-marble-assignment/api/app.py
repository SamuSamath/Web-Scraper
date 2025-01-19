from flask import Flask, request, jsonify
from scraper import scrape_reviews

app = Flask(__name__)

@app.route("/api/reviews", methods=["GET"])
def get_reviews():
    url = request.args.get("page")
    if not url:
        return jsonify({"error": "Missing 'page' parameter"}), 400

    try:
        reviews = scrape_reviews(url)
        response = {
            "reviews_count": len(reviews),
            "reviews": reviews
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)