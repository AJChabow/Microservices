# helpers.py
import io
import pandas as pd
import requests

# Global Variables
API_KEY = '_mbKWXPVxH7o-BnBWVrb8spzN37A9j_TXOevHQ5DWtjeUWdBh1'
BASE_URL = 'https://servicio.mapama.gob.es/apisiar/API/v1/Datos'


# Read Excel file
def read_excel(file_path):
    df = pd.read_excel(file_path)
    return df


# Calculate percentage of shaded area
def percent_shaded_area(tree_diameter, row_spacing, plant_spacing):
    tree_area = 3.14 * ((tree_diameter / 2) ** 2)
    plantation_frame = row_spacing * plant_spacing
    return (tree_area / plantation_frame) * 100


# Load crop data from Excel file
def load_crop_data(crop, file_path):
    df = read_excel(file_path)
    # Strip any leading/trailing spaces and handle case sensitivity
    df.iloc[:, 0] = df.iloc[:, 0].str.strip().str.lower()
    crop = crop.strip().lower()

    crop_df = df.loc[df.iloc[:, 0] == crop]

    if crop_df.empty:
        raise ValueError(f"Crop '{crop}' not found in the Excel file")

    crop_data = crop_df.iloc[0, 1:].values.tolist()
    return crop_data


# Get weather data from SIAR network
def get_weather_data(start_date, end_date, station):
    url = f"{BASE_URL}/Diarios/Estacion?Id={station}&FechaInicial={start_date}&FechaFinal={end_date}&ClaveAPI={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()['Datos']
    except requests.RequestException as e:
        print(f"Error during request: {e}")


# Standard sum Kc * ET0
def standard_sum_kc_et0(weatherData, crop_data):
    sum = 0
    for day in weatherData:
        date = day['Fecha']
        month = date[5:7]
        kc = crop_data[int(month) - 1]
        et0 = day['EtPMon']
        kc_et0 = kc * et0
        sum += kc_et0
    return sum


# Calculate net evapotranspiration
def calculate_net_evapotranspiration(weatherData, crop_data, percent_shaded_area):
    sum_kc_et0 = 0
    if crop_data[-1] == 1:
        if percent_shaded_area >= 67:
            return standard_sum_kc_et0(weatherData, crop_data)
        elif percent_shaded_area < 67:
            kc = 0.03 + (0.017865 * percent_shaded_area) - (0.0001293 * (percent_shaded_area ** 2))
            for day in weatherData:
                et0 = day['EtPMon']
                kc_et0 = kc * et0
                sum_kc_et0 += kc_et0
    elif crop_data[-1] == 2:
        if percent_shaded_area >= 66:
            return standard_sum_kc_et0(weatherData, crop_data)
        elif percent_shaded_area < 66:
            for day in weatherData:
                kc = crop_data[int(month) - 1] * (0.0267 * percent_shaded_area) - (
                            0.000175 * (percent_shaded_area ** 2))
                et0 = day['EtPMon']
                kc_et0 = kc * et0
                sum_kc_et0 += kc_et0
    elif crop_data[-1] == 3:
        return standard_sum_kc_et0(weatherData, crop_data)
    return sum_kc_et0


# Calculate effective precipitation
def calculate_effective_precipitation(weatherData, crop_data, percent_shaded_area):
    sum_effective_precipitation = 0
    monthly_fpe_factor = [0.75, 0.75, 0.75, 0.75, 0.75, 0.25, 0.25, 0.25, 0.25, 0.75, 0.75, 0.75]
    if crop_data[-1] == 3:
        for day in weatherData:
            precipitation = day['PePMon']
            month = day['Fecha'][5:7]
            fpe_factor = monthly_fpe_factor[int(month) - 1]
            fpe_precipitation = precipitation * fpe_factor
            sum_effective_precipitation += fpe_precipitation
        return sum_effective_precipitation
    elif crop_data[-1] == 1 or crop_data[-1] == 2:
        fpe_factor = percent_shaded_area * 1.25
        if fpe_factor > 0.80:
            fpe_factor = 0.80
        for day in weatherData:
            precipitation = day['PePMon']
            fpe_precipitation = precipitation * fpe_factor
            sum_effective_precipitation += fpe_precipitation
    return sum_effective_precipitation


# Calculate gross irrigation needs
def calculate_irrigation_needs(net_et, ea_efficiency, plot_coefficient):
    return net_et * (1 - plot_coefficient) / ea_efficiency


# Calculate irrigation rate and time
def calculate_irrigation_rate_and_time(irrigation_needs, plantation_frame, flow_rate, num_emitters, modulation_factor):
    liters_per_plant = irrigation_needs * plantation_frame * modulation_factor
    irrigation_hours = liters_per_plant / (flow_rate * num_emitters)
    return liters_per_plant, irrigation_hours
