# test_lambda_function.py
import json
import pytest
from lambda_function import lambda_handler


@pytest.fixture
def apigw_event():
    """ Generates API GW Event"""
    return {
        "body": json.dumps({
            "TREE_DIAMETER": 6.0,
            "ROW_SPACING": 6.0,
            "PLANT_SPACING": 6.0,
            "QU_FLOW_RATE": 3.5,
            "NUMBER_OF_EMITTERS_PP": 6,
            "EA_IRRIGATION_EFFICIENCY": 0.85,
            "PLOT_COEFFICIENT": 0.1,
            "IRR_MODULATION_FACTOR": 1.0,
            "CROP": "Cítricos",
            "START_DATE": "2024-05-01",
            "END_DATE": "2024-05-07",
            "STATION": "A01"
        }),
        "httpMethod": "POST"
    }


@pytest.fixture
def invalid_apigw_event():
    """ Generates API GW Event with an invalid crop"""
    return {
        "body": json.dumps({
            "TREE_DIAMETER": 1.0,
            "ROW_SPACING": 5.0,
            "PLANT_SPACING": 5.0,
            "QU_FLOW_RATE": 2.0,
            "NUMBER_OF_EMITTERS_PP": 2,
            "EA_IRRIGATION_EFFICIENCY": 0.8,
            "PLOT_COEFFICIENT": 0.1,
            "IRR_MODULATION_FACTOR": 1.0,
            "CROP": "invalid_crop_name",
            "START_DATE": "2024-05-01",
            "END_DATE": "2024-05-07",
            "STATION": "station_id"
        }),
        "httpMethod": "POST"
    }


def test_lambda_handler(apigw_event):
    # Mock context object if needed
    context = {}

    # Call the Lambda function handler
    response = lambda_handler(apigw_event, context)

    # Verify the response
    print(response)
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["message"] == "Calculation done successfully"
    assert "Net Evapotranspiration" in body
    assert "Liters per plant" in body
    assert "Irrigation hours" in body


def test_lambda_handler_invalid_crop(invalid_apigw_event):
    # Mock context object if needed
    context = {}

    # Call the Lambda function handler with invalid crop
    response = lambda_handler(invalid_apigw_event, context)

    # Verify the response
    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert body == "Crop 'invalid_crop_name' not found in the Excel file"
