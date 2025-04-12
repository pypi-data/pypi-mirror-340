from .logger import logger

class KeyService:
    @staticmethod
    def parse_hash_data(hash_data):
        properly_parsed_hash = {}
        
        if isinstance(hash_data, dict):
            all_pairs = []
            for k in hash_data.keys():
                if '=' in k:
                    all_pairs.append(k)
            for v in hash_data.values():
                if isinstance(v, str) and '=' in v:
                    all_pairs.append(v)
            
            for pair in all_pairs:
                if '=' in pair:
                    field, value = pair.split('=', 1)
                    properly_parsed_hash[field.strip()] = KeyService._parse_value(value.strip())
        
        elif isinstance(hash_data, str):
            lines = hash_data.strip().split('\n')
            for line in lines:
                if '=' in line:
                    field, value = line.split('=', 1)
                    properly_parsed_hash[field.strip()] = KeyService._parse_value(value.strip())
        
        return properly_parsed_hash

    @staticmethod
    def _parse_value(value):
        if value.startswith('[') and value.endswith(']'):
            try:
                array_str = value[1:-1]
                array_values = [v.strip() for v in array_str.split(',')]
                return ", ".join(array_values)
            except Exception as e:
                logger.error(f"Error parsing array value: {e}")
                return value
        return value

    @staticmethod
    def clean_redis_value(value):
        if isinstance(value, str) and value.startswith(('+', '-', ':', '$', '*')):
            return value[1:].strip()
        return value

    @staticmethod
    def format_list(values):
        formatted_items = []
        for i in range(0, len(values), 2):
            if i + 1 < len(values):
                field = KeyService.clean_redis_value(values[i])
                value = KeyService.clean_redis_value(values[i + 1])
                field = field.capitalize()
                formatted_items.append(f"{field}: {value}")
        return formatted_items

    @staticmethod
    def process_list_values(values, is_email=False):
        if is_email and len(values) >= 2 and len(values) % 2 == 0:
            return KeyService.format_list(values)
        else:
            cleaned_values = []
            for v in values:
                cleaned_v = KeyService.clean_redis_value(v)
                cleaned_values.append(cleaned_v)
            return cleaned_values