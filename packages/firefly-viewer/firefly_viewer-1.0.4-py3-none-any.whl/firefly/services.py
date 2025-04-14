from .logger import logger

class KeyService:
    @staticmethod
    def parse_hash_data(hash_data):
        """
        Process hash data from Redis.
        
        Args:
            hash_data: Hash data from Redis, should be a dictionary
            
        Returns:
            Processed dictionary of hash fields and values
        """
        if hash_data is None:
            return {}
        
        try:
            if isinstance(hash_data, dict):
                return {k: KeyService._parse_value(v) for k, v in hash_data.items()}
            return hash_data
        except Exception as e:
            logger.error(f"Error parsing hash data: {e}")
            return {} if hash_data is None else hash_data

    @staticmethod
    def _parse_value(value):
        """
        Parse a value, handling special formats like arrays.
        
        Args:
            value: The value to parse
            
        Returns:
            Parsed value
        """
        if not isinstance(value, str):
            return value

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
        """
        Clean a Redis value by removing protocol prefixes.
        
        Args:
            value: The Redis value to clean
            
        Returns:
            Cleaned value
        """
        if isinstance(value, str) and value.startswith(('+', '-', ':', '`', '*')):
            return value[1:].strip()
        return value

    @staticmethod
    def process_list_values(values):
        """
        Process list values.
        
        Args:
            values: List of values to process
            
        Returns:
            Processed list of values
        """
        if values is None:
            return []
            
        try:
            return list(values)  # Just ensure it's a list
        except Exception as e:
            logger.error(f"Error processing list values: {e}")
            return values if isinstance(values, list) else []