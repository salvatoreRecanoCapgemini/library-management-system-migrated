

from flask import Flask, jsonify
from queries import get_program_metrics

app = Flask(__name__)

@app.route('/program_metrics/<int:program_id>', methods=['GET'])
def get_program_metrics_route(program_id):
    metrics = get_program_metrics(program_id)
    return jsonify(metrics)