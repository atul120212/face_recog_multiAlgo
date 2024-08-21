import time
import uuid


def generate_uuid():
    now = time.time()
    mlsec = repr(now).split('.')[1][:3]
    return time.strftime("%Y%m%d%H%M%S".format(mlsec)) + '_' + str(uuid.uuid4().hex)[:8]