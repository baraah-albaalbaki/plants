from flask import Flask, request, jsonify
from models import setup_db, Plant
from flask_cors import CORS

def create_app(test_configuration=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Acces-Control_Allow_Headers','Content-Type, Authorization')
        response.headers.add('Acces-Control_Allow_Methods','GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/plants')
    def get_plants():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        plants = Plant.query.all()
        formatted_plants = [plant.format() for plant in plants]
        return jsonify({
            'success':True,
            'plants':formatted_plants[start:end],
            'total_plants':len(formatted_plants)
        })

    return app