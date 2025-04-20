import datetime
import random
import string
import hashlib

def generate_serial_id(secret_key: str, prefix: str = "RES") -> str:
    ## timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    
    # random seed 
    rand_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    # secret key
    hash_input = f"{secret_key}-{timestamp}-{rand_part}"
    hash_digest = hashlib.sha256(hash_input.encode()).hexdigest()[:6].upper()

    # combine id
    return f"{prefix}-{timestamp}-{rand_part}-{hash_digest}"
