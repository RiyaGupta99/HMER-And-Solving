import os
import json
import base64
import shutil
from main import main
from io import BytesIO
from calculator import calculate
from flask import Flask, jsonify, request
#from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

root = os.getcwd()

app = Flask(__name__)
CORS(app)

@app.route('/predict',methods=['POST'])
def predict():
    if 'internals' in os.listdir():
        shutil.rmtree('internals')
    if 'segmented' in os.listdir():
        shutil.rmtree('segmented')
    os.mkdir('segmented')
    try:
        argImage = request.json['image']
        operation = BytesIO(base64.urlsafe_b64decode(argImage))
    except Exception as e:
        return json.dumps({
            'error': str(e)
            })
    try:
        operation = main(operation)
    except Exception as e:
        return json.dumps({
            'error': str(e)
            })
    os.mkdir('internals')
    #shutil.move('segmented', 'internals')
    shutil.move('input.png', 'internals')
    shutil.move('segmented_characters.csv', 'internals')
    try:
        formatted_equation, solution = calculate(operation)
    except Exception as e:
        return json.dumps({
            'error': str(e)
            })
    try:
        f = open("minus.txt","w").close()
        res = ''
        if type(solution) is dict:
            for key,value in solution.items():
                res = res + str(key) + ":" + str(value) + "    "
        else:
            res = " ".join(str(x) for x in solution)
    except Exception as e:
        return json.dumps({
            'error': str(e)
            })
    graphString = '' 
    if os.path.exists('graph.png'): 
        with open('graph.png','rb') as imageFile:
            graph = base64.b64encode(imageFile.read()) 
        graphString = graph.decode('utf-8')
    return json.dumps({
        'Entered_equation': operation,
        'Formatted_equation': formatted_equation,
        'solution': res,
        'graph': graphString
    })

@app.route('/feedback',methods=['GET','POST'])
def feedback():
    if request.method == 'GET':
        try:
            segmentedDir = os.path.join(os.getcwd(),'segmented')
            files = sorted(list(os.walk(segmentedDir))[0][2])
            filesBase64 = dict()
            for f in files:
                filePath = os.path.join(segmentedDir,f)
                fileStringDecoded = ''
                with open(filePath,'rb') as imageFile:
                    fileEncoded = base64.b64encode(imageFile.read())
                fileStringDecoded = fileEncoded.decode('utf-8')
                filesBase64[f] = fileStringDecoded
            return json.dumps(filesBase64)
        except Exception as e:
            return json.dumps({'error':str(e)})
    elif request.method == 'POST':
        data = request.get_json()
        print(data)
        return json.dumps({'status':'success'})
    else:
        return json.dumps({'error':'incorrect request method'})
