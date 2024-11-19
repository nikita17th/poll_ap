import logging
from collections import defaultdict

import geoip2.database
from bson.objectid import ObjectId
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

from utils import init_question_data, get_geolocation, finalize_question_data, process_timestamps

app = Flask(__name__)
CORS(app)
client = MongoClient('mongodb://mongodb:27017/')
db = client['survey_db']
surveys_collection = db['surveys']
GEOIP_DB_PATH = 'GeoLite2-City.mmdb'
geoip_reader = geoip2.database.Reader(GEOIP_DB_PATH)


@app.route('/surveys', methods=['POST'])
def create_survey():
    try:
        data = request.json
        if not data.get('title') or not data.get('questions'):
            return jsonify({'error': 'Title and questions are required'}), 400
        questions = data.get('questions')
        for question in questions:
            if not question.get('type') or not question.get('data'):
                return jsonify({'error': 'Some questions has not type or data'}), 400
            type_q = question.get('type')
            data_q = question.get('data')
            if data_q.get('text', '') == '':
                return jsonify({'error': 'Some questions has not title'}), 400
            if type_q in ['multiple', 'single']:
                if not data_q.get('options'):
                    return jsonify({'error': 'Some questions has no one option'}), 400

        survey_document = {
            'title': data['title'],
            'questions': data['questions'],
        }
        result = surveys_collection.insert_one(survey_document)

        return jsonify({'id': str(result.inserted_id)}), 201
    except Exception as e:
        logging.error(e)
        return jsonify({'error': str(e)}), 500


@app.route('/surveys', methods=['GET'])
def get_surveys():
    surveys = surveys_collection.find()
    results = []
    for survey in surveys:
        results.append({
            'id': str(survey['_id']),
            'title': survey['title'],
            'questions': survey['questions']
        })

    return jsonify(results), 200


@app.route('/survey/<survey_id>', methods=['GET'])
def get_survey(survey_id):
    survey = db.surveys.find_one({'_id': ObjectId(survey_id)})
    if survey:
        return jsonify({'title': survey['title'], 'questions': survey['questions']})
    else:
        return jsonify({'error': 'Survey not found'}), 404


def get_client_ip():
    if 'X-Forwarded-For' in request.headers:
        ip = request.headers['X-Forwarded-For'].split(',')[0]
    else:
        ip = request.remote_addr
    return ip


@app.route('/survey/<survey_id>/submit', methods=['POST'])
def submit_answers(survey_id):
    try:
        data = request.json
        responses = data.get('responses', {})
        if not responses:
            return jsonify({'error': 'Not have responses participated in this survey.'}), 400

        for response in responses:
            response_data = response.get('data')
            if not response_data:
                return jsonify({'error': 'Some responses nas not answer.'}), 400

        client_ip = get_client_ip()

        existing_answer = db.answers.find_one({
            'survey_id': ObjectId(survey_id),
            'ip_address': client_ip
        })

        if existing_answer and client_ip != '127.0.0.1':
            return jsonify({'error': 'You have already participated in this survey from this IP address.'}), 403

        result = db.answers.insert_one({
            'survey_id': ObjectId(survey_id),
            'ip_address': client_ip,
            'responses': data['responses'],
            'timestamp': data['timestamp']
        })

        return jsonify({'msg': 'Thank you for participating!', 'id': str(result.inserted_id)}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/survey/<survey_id>/responses', methods=['GET'])
def get_survey_responses(survey_id):
    try:
        if not survey_id:
            return jsonify({'error': 'Empty survey_id'}), 404
        survey_cursor = db.surveys.find({'_id': ObjectId(survey_id)})
        survey_list = list(survey_cursor)

        if not survey_list:
            return jsonify({'error': 'Survey not found'}), 404

        survey = survey_list[0]
        survey_title = survey.get('title', 'Untitled survey')
        questions_list = survey.get('questions', [])
        question_stats = {question['id']: init_question_data(question) for question in questions_list}

        city_data = defaultdict(int)
        country_data = defaultdict(int)
        timestamps = []

        responses_cursor = db.answers.find({'survey_id': ObjectId(survey_id)})
        responses_list = list(responses_cursor)

        for response in responses_list:
            timestamp = response.get('timestamp')
            timestamps.append(timestamp)

            ip_address = response.get('ip_address')
            if ip_address:
                city, country = get_geolocation(ip_address, geoip_reader)
                city_data[city] += 1
                country_data[country] += 1

            for question_response in response['responses']:
                question_id = question_response.get('id')
                question_data = question_response.get('data')

                question = next((q for q in questions_list if q.get('id') == question_id), None)
                if not question:
                    continue

                question_type = question['type']
                data = question_stats[question_id]
                if question_data is not None:
                    if question_type in ['single', 'multiple']:
                        if isinstance(question_data, list):
                            for option in question_data:
                                data['answers'][option] += 1
                        else:
                            data['answers'][question_data] += 1
                    elif question_type == 'text':
                        data['text_lengths'].append(len(question_data))
                        data['text_responses'].append(question_data)

        for data in question_stats.values():
            finalize_question_data(data, len(responses_list))

        aggregated_timestamps = process_timestamps(timestamps)

        return jsonify({
            'question_stats': question_stats,
            'general_info': {
                'city_data': dict(city_data),
                'country_data': dict(country_data),
                'aggregated_timestamps': aggregated_timestamps,
                'total_responses': len(responses_list),
                'survey_title': survey_title,
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
