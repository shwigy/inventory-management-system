"""Flask application factory."""
from flask import Flask, jsonify
from flask_cors import CORS

from src.routes.inventory_routes import inventory_bp


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(inventory_bp)

    @app.route("/", methods=["GET"])
    def index():
        return jsonify({"message": "Inventory Management System API"}), 200

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
