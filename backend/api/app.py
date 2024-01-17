from threading import Thread
from celery import Celery
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from flask import Flask, request, jsonify, url_for
from backend.services.scraper_service import get_search_results, run_serp_spider
from backend.tasks import run_serp_spider
from seo_crawler.seo_crawler.spiders.serp_spider import SerpSpider
# from backend.services.content_generation_service import generate_new_blog_post

app = Flask(__name__)

# Initialize Celery
def make_celery(app):
    celery = Celery(app.import_name)
    celery.config_from_object('backend.celery_config')
    return celery

celery = make_celery(app)

@app.route('/api/search', methods=['POST'])
def search():
    try:
        keyword = request.json['keyword']
    except (TypeError, KeyError):
        return jsonify({"error": "Invalid request, keyword missing."}), 400

    # Get the search results from SerpAPI
    search_results = get_search_results(keyword)

    return jsonify(search_results=search_results)

@app.route('/api/task_status/<task_id>', methods=['GET'])
def task_status(task_id):
    # Logic for retrieving and returning the task status from its ID (using Celery)
    task = run_serp_spider.AsyncResult(task_id)
    return jsonify({
        'status': task.status,
        'result': task.result
    }), 200

@app.route('/api/task/<task_id>', methods=['GET'])
def get_task_status(task_id):
    task = celery.AsyncResult(task_id)
    response = {
        'task_id': task_id,
        'task_status': task.status,
        'task_result': task.result
    }
    return jsonify(response), 200

@app.route('/api/crawl', methods=['POST'])
def crawl():
    data = request.get_json()  # Use get_json() to parse incoming JSON data
    if not data or 'urls' not in data:
        return jsonify({"error": "Invalid request, 'urls' missing."}), 400

    urls = data['urls']
    if not isinstance(urls, list):
        return jsonify({"error": "'urls' should be a list."}), 400

    # Make sure all members of urls are indeed URLs (you can add a validation step here)

    result = run_serp_spider.delay(urls)

    # Return a URL where the API consumer can check the result or status of the task
    # For example, you may implement another route to check task status by id
    # check_url = url_for('task_status', task_id=result.id, _external=True)

    return jsonify({
        "message": "Crawl started",
        "task_id": result.id
        # "check_status_at": check_url
    }), 202


if __name__ == '__main__':
    app.run(debug=True)