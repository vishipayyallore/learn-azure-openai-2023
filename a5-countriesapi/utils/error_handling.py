from flask import jsonify


def handle_error_response(error_message, status_code):
    return jsonify({'error': error_message}), status_code
