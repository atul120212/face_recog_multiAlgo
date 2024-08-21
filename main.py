from flask import Flask, jsonify, request
import numpy as np
from typing import List, Optional
import json
import base64
import os
from Utilities import generate_uuid
from recognize import Recogonise
from pydantic import BaseModel
from EmployeInput import Employee

# creating a Flask app
app = Flask(__name__)


# on the terminal type: curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.
@app.route('/api/Recognize', methods=['POST'])
def Recognize():
    data = json.loads(request.data)
    print(data)
    base64file = data.get("base64File", None)
    base64FileExt = data.get("base64FileExt", None)
    file_bytes = base64.b64decode(base64file, validate=True)
    uid = generate_uuid() + base64FileExt
    temp_folder = os.path.join('Temp')
    tempfile = os.path.join(temp_folder, uid)

    e = Employee(id='aa', base64File='fsdg', base64FileExt='gdgf')

    with open(tempfile, "wb") as f:
        f.write(file_bytes)
    Recogonise(uid)
    return jsonify({'Status': 'ok', 'RecognizeObject': e.dict()}), 200


if __name__ == '__main__':
    app.run()
