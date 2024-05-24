import json
import pytest
from irrigation_handler.lambda_function import lambda_handler
import pandas as pd

@pytest.fixture
def excel_test_cases():
    """Loads test cases from the Excel file"""
    test_cases_path = 'unit_tests_for_riego_ivia.xlsx'
    df = pd.read_excel(test_cases_path)
    return df

def convert_to_serializable(test_case):
    # Convert the DataFrame row to a serializable dictionary
    serializable_case = {}
    for key, value in test_case.items():
        if isinstance(value, pd.Timestamp):
            serializable_case[key] = value.strftime('%Y-%m-%d')
        elif isinstance(value, (int, float, bool)):
            serializable_case[key] = value
        elif isinstance(value, str):
            try:
                # Attempt to convert to float if possible
                serializable_case[key] = float(value)
            except ValueError:
                serializable_case[key] = value
        else:
            serializable_case[key] = str(value)
    return serializable_case

@pytest.mark.parametrize("index", range(0, 2))  # Adjust the range based on the number of test cases you want to run
def test_lambda_handler_with_excel(index, excel_test_cases):
    test_case = excel_test_cases.iloc[index]
    serializable_case = convert_to_serializable(test_case)

    # Ensure that percentage fields are converted to floats
    serializable_case['Eficiencia %'] = float(serializable_case['Eficiencia %'])
    serializable_case['Coeficiente Parcela %'] = float(serializable_case['Coeficiente Parcela %'])

    # Ensure that 'Marco DP' and 'Marco DF' are converted to floats
    serializable_case['Marco DP'] = float(serializable_case['Marco DP'])
    serializable_case['Marco DF'] = float(serializable_case['Marco DF'])

    event = {
        "body": json.dumps({
            "TREE_DIAMETER": serializable_case['Diametro De Copa'],
            "ROW_SPACING": serializable_case['Marco DP'],
            "PLANT_SPACING": serializable_case['Marco DF'],
            "QU_FLOW_RATE": serializable_case['Caudal unitario'],
            "NUMBER_OF_EMITTERS_PP": serializable_case['Numero de Emisores'],
            "EA_IRRIGATION_EFFICIENCY": serializable_case['Eficiencia %'] / 100,
            "PLOT_COEFFICIENT": serializable_case['Coeficiente Parcela %'] / 100,
            "IRR_MODULATION_FACTOR": 1.0,  # Assume a constant value if not provided in Excel
            "CROP": serializable_case['Cultivo'],
            "START_DATE": serializable_case['Periodo Desde'],
            "END_DATE": serializable_case['Periodo Hasta'],
            "STATION": serializable_case['Estacion'],
            "STATION_ID": serializable_case['Estacion_ID']
        }),
        "httpMethod": "POST"
    }

    # Mock context object if needed
    context = {}

    # Call the Lambda function handler
    response = lambda_handler(event, context)

    # Verify the response
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["message"] == "Calculation done successfully"
    # Verify the response with expected values from Excel
    assert round(body["Net Evapotranspiration"], 2) == round(serializable_case['ETo'], 2)
    assert round(body["Liters per plant"], 2) == round(serializable_case['Litros/planta'], 2)
    # Convert and compare irrigation hours if necessary
    # assert body["Irrigation hours"] == serializable_case['Horas Riego']
