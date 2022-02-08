from numbers import Number
from flask import Flask, request, jsonify
from api.crud import get_news_by_date_from_db
from api.db import init_db

app = Flask(import_name="MosNews")


@app.before_first_request
def init_app():
    init_db()


@app.errorhandler(404)
def page_not_found_handler(*args, **kwargs):
    return "go to /metro/news to get news by date", 404


@app.errorhandler(500)
def page_not_found_handler(*args, **kwargs):
    return "server is down", 500


@app.route("/metro/news", methods=["GET"])
def get_news_by_date():
    # Проверка входных данных
    try:
        days = int(request.args.get("days", 0))
        if not isinstance(days, Number):
            return "wrong input format", 400
    except ValueError:
        return "wrong input format", 400

    response = get_news_by_date_from_db(days)
    return jsonify(response)
