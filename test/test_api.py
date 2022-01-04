import os
import sys
from pathlib import Path
from fastapi.testclient import TestClient
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)
from src.app import app
from src.schema import Model_List


with TestClient(app) as myclient:
    
    def test_swagger_ui():
        validate = myclient.get("/docs")
        assert validate is not None

    def test_list_url():
        validate = myclient.get("/")
        assert validate.status_code == 200 
        assert validate is not None
        assert next(item for item in validate.json() if item["name"] == "swagger_ui_html")
   

    def test_models_list():
        validate = myclient.get("/listmodels")
        jsonify = validate.json()
        assert validate.status_code == 200 
        assert jsonify["message"] == "OK"  
        assert type(jsonify['data']) == list  
        assert isinstance(jsonify['data'][0]["Model Type"], str)
        assert isinstance(jsonify['data'][0]["Accuracy"], float)
        assert jsonify['data'][0]["Accuracy"] < jsonify['data'][2]["Accuracy"]


    def test_models():
        fname = os.path.join(os.path.dirname(__file__), 'stock_prediction.csv')
        for val in Model_List.List_params():
            if val is not '':
                validate = myclient.post("/models?types="+ str(val) , files={"file": ("upload_file", open(fname, "rb"), fname)})
                jsonify = validate.json()
                assert validate.status_code == 200
                assert jsonify['message'] == 'OK'
                assert jsonify['Model Type'] == str(val)
                assert len(jsonify['data']) != 0
                assert "Close" in jsonify['data'][0]
                assert "Predictions" in jsonify['data'][0]

   
    