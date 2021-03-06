### TODO: Make a Flask app which acts as a prediction engine, it will receives data from a client and send back the
### TODO: predictions to the client in the form of JSON

from flask import Flask, request
from flask_cors import CORS, cross_origin
import urllib.parse
import json

import joblib
import importlib
import pandas as pd
app = Flask(__name__)
CORS(app, support_credentials=True)

def __str2Class(module_name, type):
    # load the module, will raise ImportError if module cannot be loaded
    class_name = '_' + str(module_name)
    module_name = type + '.' + module_name

    m = importlib.import_module(module_name)
    # get the class, will raise AttributeError if class cannot be found
    c = getattr(m, class_name)
    return c



@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
#         data = str(request.json).split("data=")[-1]
#         data = urllib.parse.unquote(data)[:-1]

#         ## Format of JSON = { "data":"rows wise data","id":"roll number }
#         data = request.args.get("data")
#         app.logger.info(data)
#         print("JSON LOADED---------------------------------->>",app.logger.info(data))
#         # JSON data converted to dictionary
#         data = json.loads(data)
#         print("DATA---------------------------------->",data)
        data= request.get_json(force=True)
        data= dict(data)

        id = data["id"]
        print(data['data'])
        data = pd.DataFrame(data["data"])
        print(data)

#         get required files by parsing ID
        pickleFile = str(id) + ".pkl"
#         pickleFile= "my.pkl"
        transformationFile = str(id)

        #loading the model and the transformation class
        model = joblib.load(r"Files/"+pickleFile)
        myClass = __str2Class(transformationFile,"Files")
        myClassInstance = myClass()

        predictions = myClassInstance.getPredictions(data,model)
#         predictions = [{"document_id":"251","out_date":"1970-01-08"},{"document_id":"341","out_date":"1972-02-14"}]
        # TODO: send back a JSON of predictions ( in this case predicted date ) with document_id as the primary key
        # TODO: example  [{"document_id":"251","out_date":"1970-01-08"},{"document_id":"341","out_date":"1972-02-14"}]
        print(predictions)
        # return str(predictions)
        return json.dumps(predictions)
if __name__ == '__main__':
    app.run(debug=True)