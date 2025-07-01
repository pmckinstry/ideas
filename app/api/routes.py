from flask import request, jsonify
from app.api import api_bp

@api_bp.route('/hello')
def hello():
    """Simple API endpoint"""
    return jsonify({
        'message': 'Hello from the API!',
        'status': 'success'
    })

@api_bp.route('/data', methods=['GET', 'POST'])
def data():
    """API endpoint for data operations"""
    if request.method == 'POST':
        data = request.get_json()
        return jsonify({
            'message': 'Data received successfully',
            'data': data,
            'status': 'success'
        })
    
    return jsonify({
        'message': 'GET request successful',
        'data': {'sample': 'data'},
        'status': 'success'
    }) 