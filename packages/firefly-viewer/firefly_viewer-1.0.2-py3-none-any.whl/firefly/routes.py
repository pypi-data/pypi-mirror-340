from flask import Blueprint, render_template, jsonify, request
from .database import DatabaseClient
from .services import KeyService
from .logger import logger

routes = Blueprint('routes', __name__)

@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/api/keys', methods=['GET'])
def get_keys():
    logger.debug("API endpoint /api/keys called")
    try:
        client = DatabaseClient.create_client()
        if not client:
            return jsonify({
                'success': False,
                'error': 'Could not connect to Firefly database',
                'connection_status': False
            })

        pattern = request.args.get('pattern', '*')
        keys = client.string_ops.keys(pattern)
        
        if not keys:
            return jsonify({
                'success': True,
                'data': {'strings': [], 'lists': [], 'hashes': []},
                'connection_status': True
            })

        strings = []
        lists = []
        hashes = []

        for key in keys:
            key_type = DatabaseClient.get_key_type(client, key)
            if key_type == "string":
                value = client.string_ops.string_get(key)
                if value is not None:
                    strings.append({"key": key, "value": value})
            elif key_type == "list":
                value = client.list_ops.list_range(key, 0, -1)
                if value is not None:
                    is_email = 'email' in key.lower()
                    processed_value = KeyService.process_list_values(value, is_email)
                    lists.append({"key": key, "value": processed_value})
            elif key_type == "hash":
                value = client.hash_ops.hash_get_all(key)
                if value is not None:
                    processed_value = KeyService.parse_hash_data(value)
                    hashes.append({"key": key, "value": processed_value})

        return jsonify({
            'success': True,
            'data': {
                'strings': strings,
                'lists': lists,
                'hashes': hashes
            },
            'connection_status': True
        })
    except Exception as e:
        logger.error(f"Error getting keys: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'connection_status': False
        })

@routes.route('/api/key/<key>', methods=['GET'])
def get_key_value(key):
    try:
        client = DatabaseClient.create_client()
        if not client:
            return jsonify({
                'success': False,
                'error': 'Could not connect to Firefly database',
                'connection_status': False
            })

        key_type = DatabaseClient.get_key_type(client, key)
        if not key_type:
            return jsonify({
                'success': False,
                'error': 'Key not found or type not determined',
                'connection_status': True
            }), 404

        value = None
        if key_type == "string":
            value = client.string_ops.string_get(key)
        elif key_type == "hash":
            value = client.hash_ops.hash_get_all(key)
            value = KeyService.parse_hash_data(value)
        elif key_type == "list":
            value = client.list_ops.list_range(key, 0, -1)
            is_email = 'email' in key.lower()
            value = KeyService.process_list_values(value, is_email)

        return jsonify({
            'success': True,
            'data': {
                'key': key,
                'type': key_type,
                'value': value
            },
            'connection_status': True
        })
    except Exception as e:
        logger.error(f"Error getting key value: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'connection_status': False
        })