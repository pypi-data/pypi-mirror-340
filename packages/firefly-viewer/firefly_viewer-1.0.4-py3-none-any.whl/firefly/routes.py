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
            try:
                if key_type == "string":
                    value = client.string_ops.string_get(key)
                    if value is not None:
                        strings.append({"key": key, "value": value})
                elif key_type == "list":
                    list_values = client.list_ops.list_range(key, 0, -1)
                    if list_values is not None:
                        processed_value = KeyService.process_list_values(list_values)
                        lists.append({"key": key, "value": processed_value})
                elif key_type == "hash":
                    hash_values = client.hash_ops.hash_get_all(key)
                    if hash_values is not None:
                        processed_value = KeyService.parse_hash_data(hash_values)
                        hashes.append({"key": key, "value": processed_value})
            except Exception as e:
                logger.warning(f"Error processing key {key}: {e}")

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
        try:
            if key_type == "string":
                value = client.string_ops.string_get(key)
            elif key_type == "hash":
                hash_values = client.hash_ops.hash_get_all(key)
                value = KeyService.parse_hash_data(hash_values)
            elif key_type == "list":
                list_values = client.list_ops.list_range(key, 0, -1)
                value = KeyService.process_list_values(list_values)
        except Exception as e:
            logger.warning(f"Error processing key {key}: {e}")
            return jsonify({
                'success': False,
                'error': f'Error processing key: {str(e)}',
                'connection_status': True
            }), 500

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