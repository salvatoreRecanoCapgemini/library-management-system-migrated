

from flask import Flask, jsonify, request
from app.services import query_database

app = Flask(__name__)

class ProgramMetricsController:
    def get_program_metrics(self, program_id):
        if request.method == 'GET':
            metrics = query_database(program_id)
            return jsonify(metrics)

@app.route('/program_metrics/<program_id>', methods=['GET'])
def get_program_metrics(program_id):
    controller = ProgramMetricsController()
    return controller.get_program_metrics(program_id)