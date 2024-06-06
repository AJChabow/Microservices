# lambda_function.py
import json
import os
from helpers import (
    percent_shaded_area, load_crop_data, get_weather_data, calculate_net_evapotranspiration,
    calculate_effective_precipitation, calculate_irrigation_needs, calculate_irrigation_rate_and_time
)

current_dir = os.path.dirname(os.path.abspath(__file__))
EXCEL_FILE_PATH = os.path.join(current_dir, 'CultivaKcMes.xlsx')


def lambda_handler(event, context):
    if event['httpMethod'] != 'POST':
        return {
            'statusCode': 405,
            'body': json.dumps('Only POST requests are accepted')
        }
    data = json.loads(event['body'])

    if not data:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid or missing JSON')
        }
    TREE_DIAMETER = data.get('TREE_DIAMETER')
    ROW_SPACING = data.get('ROW_SPACING')
    PLANT_SPACING = data.get('PLANT_SPACING')
    QU_FLOW_RATE = data.get('QU_FLOW_RATE')
    NUMBER_OF_EMITTERS_PP = data.get('NUMBER_OF_EMITTERS_PP')
    EA_IRRIGATION_EFFICIENCY = data.get('EA_IRRIGATION_EFFICIENCY')
    PLOT_COEFFICIENT = data.get('PLOT_COEFFICIENT')
    IRR_MODULATION_FACTOR = data.get('IRR_MODULATION_FACTOR')
    CROP = data.get('CROP')
    START_DATE = data.get('START_DATE')
    END_DATE = data.get('END_DATE')
    STATION = data.get('STATION')
    try:
        pAs = percent_shaded_area(TREE_DIAMETER, ROW_SPACING, PLANT_SPACING)
        crop_kc_values = load_crop_data(CROP, EXCEL_FILE_PATH)

        end_date = END_DATE
        start_date = START_DATE
        weather_data = get_weather_data(start_date, end_date, STATION)

        net_evapotranspiration = calculate_net_evapotranspiration(weather_data, crop_kc_values, pAs)

        effective_precipitation = calculate_effective_precipitation(weather_data, crop_kc_values, pAs)
        net_et = net_evapotranspiration - effective_precipitation

        gross_irrigation_needs = calculate_irrigation_needs(net_et, EA_IRRIGATION_EFFICIENCY, PLOT_COEFFICIENT)

        liters_per_plant, irrigation_hours = calculate_irrigation_rate_and_time(
            gross_irrigation_needs, ROW_SPACING * PLANT_SPACING, QU_FLOW_RATE, NUMBER_OF_EMITTERS_PP,
            IRR_MODULATION_FACTOR
        )
        response = {
            'message': 'Calculation done successfully',
            'Net Evapotranspiration': net_et,
            'Liters per plant': liters_per_plant,
            'Irrigation hours': irrigation_hours
        }

        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }

    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(str(e))
        }
