import redis

from flask import Flask, jsonify, request

from src.settings import app_settings, redis_settings
from src.utils import int_to_enc, short_str_enc


def create_app():
    app = Flask(__name__)
    redis_client = redis.Redis(
        host=redis_settings.host,
        port=6379,
        db=0,
        password=redis_settings.password,
    )

    @app.route("/shorten-url", methods=["POST"])
    def shorten_url():
        try:
            data = request.json
            long_url = data.get("url")

            if long_url:
                short_url = short_str_enc(long_url)
                redis_client.set(short_url, long_url)

                return jsonify({"success": True, "short_url": short_url}), 201
            else:
                return jsonify({"success": False, "error": "URL missing"}), 400
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    @app.route("/get-long-url/<short_url>", methods=["GET"])
    def get_long_url(short_url):
        try:
            long_url = redis_client.get(short_url)
            if long_url:
                return (
                    jsonify({"success": True, "long_url": long_url.decode("utf-8")}),
                    200,
                )
            else:
                return jsonify({"success": False, "error": "Short URL not found"}), 404
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        debug=True,
        host="0.0.0.0",
        port=app_settings.port,
    )
