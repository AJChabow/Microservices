import flask
import functions_framework
import requests
from datetime import datetime, timedelta
import json
import io
import pandas as pd
from google.cloud import storage






# Your Google Cloud Project ID
project_id = 'cropmindproject'
bucket_name = 'cropinfo'
blob_name = 'CultivaKcMes.xlsx'

client = storage.Client(project=project_id)



# Global Variables
API_KEY = '_mbKWXPVxH7o-BnBWVrb8spzN37A9j_TXOevHQ5DWtjeUWdBh1'
BASE_URL = 'https://servicio.mapama.gob.es/apisiar/API/v1/Datos'

def read_excel_from_gcs(bucket_name, blob_name):
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    # Read the blob's content into memory
    data = blob.download_as_bytes()

    # Use BytesIO to handle the in-memory bytes
    excel_data = io.BytesIO(data)

    # Read the Excel file with pandas
    df = pd.read_excel(excel_data)

    return df



#Calculate percentage of shaded area
def percent_shaded_area(tree_diameter, row_spacing, plant_spacing):
    tree_area = 3.14 * ((tree_diameter/2)**2)
    plantation_frame = row_spacing * plant_spacing
    return (tree_area / plantation_frame) * 100

#returns the crop data for the crop specified in the file
def load_crop_data(crop):
    df = read_excel_from_gcs(bucket_name, blob_name)
    crop_data = df.loc[df.iloc[:, 0] == crop].iloc[0, 1:].values.tolist()
    return crop_data   

#returns weather data from SIAR network
def get_weather_data(start_date, end_date, station):
    url = f"{BASE_URL}/Diarios/Estacion?Id={station}&FechaInicial={start_date}&FechaFinal={end_date}&ClaveAPI={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()['Datos']
    except requests.RequestException as e:
        print(f"Error during request: {e}")

def standard_sum_kc_et0(weatherData, crop_data):
    sum = 0
    #loop through each day in the last week
    for day in weatherData:
        date = day['Fecha']
        month = date[5:7]
        kc = crop_data[int(month)-1]
        et0 = day['EtPMon']
        kc_et0 = kc * et0
        sum += kc_et0
    return sum

def calculate_net_evapotranspiration(weatherData, crop_data, percent_shaded_area):
    sum_kc_et0 = 0
    #crop group check
    if crop_data[-1] == 1:
        if percent_shaded_area >= 67:
            #use standard formula
            return standard_sum_kc_et0(weatherData, crop_data)
        elif percent_shaded_area < 67:
            kc = 0.03 + (0.017865 * percent_shaded_area) - (0.0001293 * (percent_shaded_area**2))
            for day in weatherData:
                date = day['Fecha']
                month = date[5:7]
                et0 = day['EtPMon']
                kc_et0 = kc * et0
                sum_kc_et0 += kc_et0
    elif crop_data[-1] == 2:
        if percent_shaded_area >= 66:
            #use standard formula
            return standard_sum_kc_et0(weatherData, crop_data)
        elif percent_shaded_area < 66:
            for day in weatherData:
                date = day['Fecha']
                month = date[5:7]
                kc = crop_data[int(month)-1] * (0.0267 * percent_shaded_area) - (0.000175 * (percent_shaded_area**2))
                et0 = day['EtPMon']
                kc_et0 = kc * et0
                sum_kc_et0 += kc_et0
    elif crop_data[-1] == 3:
        #use standard formula
        return standard_sum_kc_et0(weatherData, crop_data)
    return sum_kc_et0

#function for summing the last weeks precipitation values, held in the 'PePMon' key multiplied by the FPE factor
def calculate_effective_precipitation(weatherData, crop_data, percent_shaded_area):
    sum_effective_precipitation = 0
    monthly_fpe_factor = [0.75,0.75,0.75,0.75,0.75,0.25,0.25,0.25,0.25,0.75,0.75,0.75]
    if crop_data[-1] == 3:
        for day in weatherData:
            #get the precipitation value for that day
            precipitation = day['PePMon']
            date = day['Fecha']
            #get the month
            month = date[5:7]
            #get the FPE factor for that month
            fpe_factor = monthly_fpe_factor[int(month)-1]
            fpe_precipitation = precipitation * fpe_factor
            sum_effective_precipitation += fpe_precipitation
        #return the sum
        return sum
    elif crop_data[-1] == 1 or crop_data[-1] == 2:
        fpe_factor = percent_shaded_area * 1.25
        if fpe_factor > 0.80:
            fpe_factor = 0.80
        for day in weatherData:
            #get the precipitation value for that day
            precipitation = day['PePMon']
            date = day['Fecha']
            #get the month
            month = date[5:7]
            fpe_precipitation = precipitation * fpe_factor
            sum_effective_precipitation += fpe_precipitation
    return sum_effective_precipitation

#function for calculating gross irrigation needs
def calculate_irrigation_needs(net_et, ea_efficiency, plot_coefficient):
    return net_et * (1 - plot_coefficient) / ea_efficiency

#function for calculating irrigation rate and time
def calculate_irrigation_rate_and_time(irrigation_needs, plantation_frame, flow_rate, num_emitters, modulation_factor):
    liters_per_plant = irrigation_needs * plantation_frame * modulation_factor
    irrigation_hours = liters_per_plant / (flow_rate * num_emitters)    
    return liters_per_plant, irrigation_hours

# Main Script
@functions_framework.http
def iviacalc(request):
    # Import the Flask module and create an instance of the Flask web application
    from flask import jsonify

    # Only allow POST requests
    if request.method != 'POST':
        return 'Only POST requests are accepted', 405

    # Parse JSON from the request
    data = request.get_json(silent=True)

    if not data:
        return 'Invalid or missing JSON', 400

    # Example of setting variables from the JSON payload
    global TREE_DIAMETER, ROW_SPACING, PLANT_SPACING
    global QU_FLOW_RATE, NUMBER_OF_EMITTERS_PP, EA_IRRIGATION_EFFICIENCY
    global PLOT_COEFFICIENT, IRR_MODULATION_FACTOR
    
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

    # Add more variables as needed

    # Perform the calculation
    pAs = percent_shaded_area(TREE_DIAMETER, ROW_SPACING, PLANT_SPACING)
    crop_kc_values = load_crop_data(CROP)

    end_date = END_DATE
    start_date = START_DATE
    weather_data = get_weather_data(start_date, end_date, STATION)

    net_evapotranspiration = calculate_net_evapotranspiration(weather_data, crop_kc_values, pAs)
    effective_precipitation = calculate_effective_precipitation(weather_data, crop_kc_values, pAs)

    net_et = net_evapotranspiration - effective_precipitation
    gross_irrigation_needs = calculate_irrigation_needs(net_et, EA_IRRIGATION_EFFICIENCY, PLOT_COEFFICIENT)

    liters_per_plant, irrigation_hours = calculate_irrigation_rate_and_time(gross_irrigation_needs, ROW_SPACING * PLANT_SPACING, QU_FLOW_RATE, NUMBER_OF_EMITTERS_PP, IRR_MODULATION_FACTOR)

    # Output Results
    print("Net Evapotranspiration:", net_et)
    print("Liters per plant:", liters_per_plant)
    print("Irrigation hours:", irrigation_hours)
    
    # Return a response
    response = {
        'message': 'Calculation done successfully',
        'Net Evapotranspiration': net_et,
        'Liters per plant': liters_per_plant,
        'Irrigation hours': irrigation_hours
        # Include other variables in the response if needed
    }
    return jsonify(response)
    

