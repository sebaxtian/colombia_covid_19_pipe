# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
#import geopandas as gpd # geodata processing
# Get geolocation using geocoder
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent='colombia_covid_19_pipe', timeout=None)
# Https requests
import requests
import unidecode
# Dates
import datetime
from datetime import date
from calendar import day_name, month_name

import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
# PDFMiner pdfminer.six
try:
    from pdfminer.high_level import extract_text
except Exception:
    install('pdfminer.six')
    from pdfminer.high_level import extract_text

import tempfile
import os

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

#for dirname, _, filenames in os.walk('/kaggle/input'):
#    for filename in filenames:
#        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.

# %% [markdown]
# # Colombia Covid 19 Pipeline
# Dataset is obtained from [Instituto Nacional de Salud](https://www.ins.gov.co/Noticias/Paginas/Coronavirus.aspx) daily report Coronavirus 2019 from Colombia.
# 
# You can get the official dataset here: 
# [INS - Official Report](https://www.datos.gov.co/Salud-y-Protecci-n-Social/Casos-positivos-de-COVID-19-en-Colombia/gt2j-8ykr)
# 
# The number of new cases are increasing day by day around the world.
# This dataset has information about reported cases from 32 Colombia departments.
# 
# You can get the Google COVID-19 Community Mobility Reports - Colombia.
# 
# You can view and collaborate to the analysis here:
# [colombia_covid_19_analysis](https://www.kaggle.com/sebaxtian/colombia-covid-19-analysis) Kaggle Notebook Kernel.
# %% [markdown]
# ---

# %%
# Any results you write to the current directory are saved as output.
OUTPUT_DIR = './'
if os.path.split(os.path.abspath('.'))[-1] == 'src':
    OUTPUT_DIR = '../output'
# Official Opendata Report, with anomalies
#URL_DATASET = 'https://www.datos.gov.co/api/views/gt2j-8ykr/rows.csv?accessType=DOWNLOAD'

# Official Daily Report Until Now
URL_DATASET = 'https://infogram.com/api/live/flex/4524241a-91a7-4bbd-a58e-63c12fb2952f/7109db63-a83b-4ba7-b5bc-565b2a7ee4bb?'

# %% [markdown]
# ---
# %% [markdown]
# ## Load Local Covid19 Report from Output

# %%
# Load local covid19_df from output
covid19_df = pd.read_csv(os.path.join(OUTPUT_DIR, 'covid19.csv'))
# Report last day
covid19_df.shape

# %% [markdown]
# ---
# %% [markdown]
# ## Get Official Covid19 Daily Report

# %%
# Get Covid19 dataset daily report
# Reading the json as a dict
with requests.get(URL_DATASET) as original_dataset:
    data = original_dataset.json()
#print(data)

# Department Report
#print(data['data'][0])
#department_report = data['data'][0]

# National Report
#print(len(data['data'][1:]))
national_report = data['data'][1:]

# New Cases
new_cases = national_report[0]
#print(new_cases)

# Deaths
new_deaths = national_report[1]
#print(new_deaths)

# Recovered
new_recovered = national_report[2]
#print(new_recovered)

# Recovered Hostpital
new_recovered_hospital = national_report[3]
#print(new_recovered_hospital)


# Get attributes and data
attrs = new_cases[0]
del new_cases[0]
#print('new_cases', new_cases)

# Build dataframe
covid_df = pd.DataFrame(data=new_cases, columns=attrs)

# Size dataframe
covid_df.shape


# %%
# Get Covid19 dataset
#covid_df = pd.read_csv(URL_DATASET)


# %%
# Show dataframe
covid_df.tail()


# %%
# Show original columns
#print(covid_df.columns.values)


# %%
# Rename columns
#covid_df.rename(columns={
#    "Caso": "id_case",
#    "Fecha de diagnóstico": "date",
#    "Ciudad": "city",
#    "Departamento": "dept_dist",
#    "Ubicación": "care",
#    "Edad": "age",
#    "Sexo": "sex",
#    "Tipo": "kind",
#    "Pais de procedencia": "country_origin"}, inplace=True)
covid_df.columns = ['id_case', 'date', 'city', 'dept_dist', 'care', 'age', 'sex', 'kind', 'country_origin']
# Show dataframe
covid_df.head()


# %%
# Clean empty rows
covid_df = covid_df[covid_df['date'] != '']
# Show dataframe
covid_df.tail()


# %%
# Remove accents
covid_df['city'] = covid_df['city'].transform(lambda value: unidecode.unidecode(value))
covid_df['dept_dist'] = covid_df['dept_dist'].transform(lambda value: unidecode.unidecode(value))
# Show dataframe
covid_df.head()


# %%
# Setup date format
def setup_date(value):
    #print('Cosa', value)
    value = value.split('/')
    #print('Values', value)
    if len(value) == 3:
        # Check day
        if len(value[0]) == 1:
            value[0] = '0' + value[0]
        # Check mounth
        if len(value[1]) == 1:
            value[1] = '0' + value[1]
        # Check year
        if len(value[2]) == 2:
            value[2] = value[2] + '20'
        # Return new date format
        return '/'.join(value)
    else:
        return ''
# Check date format
def check_date_format(value):
    try:
        new_date = datetime.datetime.strptime(value, '%d/%m/%Y')
        #print('Fecha Valida:', value)
        return new_date
    except ValueError:
        #print('Fecha con Error:', value)
        #new_date = datetime.datetime.now().strptime('%d/%m/%Y')
        return np.NaN

# Setup date format
covid_df['date'] = covid_df['date'].transform(lambda value: setup_date(value))
covid_df['date'] = covid_df['date'].transform(lambda value: check_date_format(value))
covid_df['date'].fillna(method='bfill', inplace=True)
# Setup date format
covid_df['date'] = [value.strftime('%d/%m/%Y') for value in pd.to_datetime(covid_df['date'], format='%d/%m/%Y')]
# Show dataframe
covid_df.tail()


# %%
# Add Day, Month, Year, Month Name and Day Name
covid_df['day'] = covid_df['date'].transform(lambda value: value.split('/')[0])
covid_df['month'] = covid_df['date'].transform(lambda value: value.split('/')[1])
covid_df['year'] = covid_df['date'].transform(lambda value: value.split('/')[2])
# English
#covid_df['month_name'] = covid_df['month'].transform(lambda value: month_name[int(value)])
#covid_df['day_name'] = covid_df['date'].transform(lambda value: day_name[date(int(value.split('/')[2]), int(value.split('/')[1]), int(value.split('/')[0])).weekday()])
# Spanish
nombre_mes = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
nombre_dia = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
covid_df['month_name'] = covid_df['month'].transform(lambda value: nombre_mes[int(value) - 1])
covid_df['day_name'] = covid_df['date'].transform(lambda value: nombre_dia[date(int(value.split('/')[2]), int(value.split('/')[1]), int(value.split('/')[0])).weekday()])
# Show dataframe
covid_df.head()


# %%
# Update Case ID
#covid_df['id_case'] = covid_df.index
#covid_df.tail()


# %%
# Sort columns
covid_df = covid_df[['id_case', 'date', 'day', 'month', 'year', 'month_name', 'day_name', 'city', 'dept_dist', 'age', 'sex', 'kind', 'country_origin', 'care']]
# Show dataframe
covid_df.head()


# %%
# Setup string title format
covid_df['city'] = covid_df['city'].transform(lambda value: value.title())
covid_df['dept_dist'] = covid_df['dept_dist'].transform(lambda value: value.title())
covid_df['country_origin'] = covid_df['country_origin'].transform(lambda value: value.title())
# Show dataframe
covid_df.tail()

# %% [markdown]
# ## Merge Local Covid19 Report with Official Covid19 Daily Report

# %%
# Merge with the local covid19_df from output
# Temporal update id_case
#covid19_df['id_case'] = covid19_df['id_case'].transform(lambda value: value + 1) OJO
# Check changes
#print(covid_df['id_case'].values[0])
#print(covid19_df['id_case'].values[-1])
if int(covid_df['id_case'].values[0]) > int(covid19_df['id_case'].values[-1]):
    covid_df = pd.concat([covid19_df, covid_df])
else:
    covid_df = covid19_df
# Show dataframe
covid_df.shape
#covid_df.tail()


# %%
# Reset index
covid_df.reset_index(inplace=True)
covid_df.drop(columns=['index'], inplace=True)
# Show dataframe
covid_df.tail()


# %%
# Setup string title format
covid_df['kind'] = covid_df['kind'].transform(lambda value: value.title())
covid_df['care'] = covid_df['care'].transform(lambda value: value.title())
# Show dataframe
covid_df.tail()

# %% [markdown]
# ## Covid 19 Dataset
# > ***Output file***: covid19.csv

# %%
# Save dataframe
covid_df.to_csv(os.path.join(OUTPUT_DIR, 'covid19.csv'), index=False)

# %% [markdown]
# ---
# %% [markdown]
# ## Covid19 Daily Report Dataset Updated

# %%
# Show dataframe
covid_df.head()


# %%
# Show dataframe
covid_df.tail()

# %% [markdown]
# ---
# %% [markdown]
# ## Samples Processed

# %%
# Samples Processed
# Reading the json as a dict
with requests.get('https://infogram.com/api/live/flex/4524241a-91a7-4bbd-a58e-63c12fb2952f/4dc066f9-6be5-4791-aefb-96fe4c523dfd?') as original_dataset:
    data = original_dataset.json()
#print(data['data'][0][0][0])

# Get attributes and data
attrs = data['data'][0][0][0]
del data
#print(attrs)
samples_processed = attrs.split('<b>')[1].split('</b>')[0].replace('.', '')
#print('Samples Processed:', samples_processed)

# %% [markdown]
# ## Samples Descarted

# %%
# Descarted Cases
# Reading the json as a dict
with requests.get('https://infogram.com/api/live/flex/4524241a-91a7-4bbd-a58e-63c12fb2952f/4dc066f9-6be5-4791-aefb-96fe4c523dfd?') as original_dataset:
    data = original_dataset.json()
#print(data['data'][0][1][0])

# Get attributes and data
attrs = data['data'][0][1][0]
del data
#print(attrs)
samples_descarted = attrs.split('<b>')[1].split('</b>')[0].replace('.', '')
#print('Samples Descarted:', samples_descarted)

# %% [markdown]
# ---
# %% [markdown]
# ## Time Line Samples Processed

# %%
# Time Line Samples Processed
# Reading the json as a dict
with requests.get('https://infogram.com/api/live/flex/4524241a-91a7-4bbd-a58e-63c12fb2952f/0a859405-7279-44a1-80d9-ff127bdf4489?') as original_dataset:
    data = original_dataset.json()
#print(data['data'])
#print(data['data'][0])

# Get attributes and data
attrs = data['data'][0][0]
attrs[0] = 'Periodo'
del data['data'][0][0]
#print(attrs)
data = data['data'][0]
#print(data)

# Build dataframe
covid_df_samples_processed = pd.DataFrame(data=data, columns=attrs)

# Size dataframe
covid_df_samples_processed.tail()


# %%
# Rename columns
covid_df_samples_processed.rename(columns={
    "Periodo": "period",
    "Muestras procesadas": "total_samples",
    "Acumulado procesadas": "accum_samples"}, inplace=True)
# Show dataframe
covid_df_samples_processed.tail()


# %%
# Update date format
def update_date_format(period):
    date1 = period.split('-')[0]
    date2 = period.split('-')[1]
    if date1.split('/')[-1] == '20':
        date1 = '/'.join(date1.split('/')[0:-1]) + '/2020'
    if date2.split('/')[-1] == '20':
        date2 = '/'.join(date2.split('/')[0:-1]) + '/2020'
    return date1 + '-' + date2
# Example
#update_date_format('02/03/20-08/03/20')
# Update date format
covid_df_samples_processed['period'] = covid_df_samples_processed['period'].transform(lambda value: update_date_format(value))
# Show dataframe
covid_df_samples_processed.tail()

# %% [markdown]
# ## Time Line Samples Processed
# > ***Output file***: covid19_samples_processed.csv

# %%
# Save dataframe
covid_df_samples_processed.to_csv(os.path.join(OUTPUT_DIR, 'covid19_samples_processed.csv'), index=False)

# %% [markdown]
# ---
# %% [markdown]
# ## Time Line by Care

# %%
# Care Classes
list(set(covid_df['care'].values))


# %%
# Get time line by care [cases, recovered, deaths]
def get_time_line_by_care(care):
    # covid_df_report
    covid_df_report = pd.DataFrame()
    # Check care
    if care == '*':
        covid_df_report = covid_df.groupby('date')['date'].count()
    elif care == 'Recuperado':
        covid_df_report = covid_df[(covid_df['care'] == 'Recuperado') | (covid_df['care'] == 'Recuperado (Hospital)')].groupby('date')['date'].count()
    else:
        covid_df_report = covid_df[covid_df['care'] == care].groupby('date')['date'].count()
    # ---
    # Create dateset
    covid_df_report = pd.DataFrame(data={'date': covid_df_report.index, 'total': covid_df_report.values}, columns=['date', 'total'])
    covid_df_report['date_iso'] = pd.to_datetime(covid_df_report['date'], format='%d/%m/%Y')
    covid_df_report = covid_df_report.sort_values(by=['date_iso'], ascending=True)
    covid_df_report['accum'] = covid_df_report['total'].cumsum()
    covid_df_report = covid_df_report.drop(columns=['date_iso'])
    covid_df_report.reset_index(inplace=True, drop=True)
    # Return
    return covid_df_report

# Time line by cases
covid_df_cases = get_time_line_by_care('*')
#print('covid_df_cases', '\n', covid_df_cases)

# Time line by recovered
covid_df_recovered = get_time_line_by_care('Recuperado')
#print('covid_df_recovered', '\n', covid_df_recovered.head())

# Time line by deaths
covid_df_deaths = get_time_line_by_care('Fallecido')
#print('covid_df_deaths', '\n', covid_df_deaths.head())

# Get total
def get_total(df_target, value):
    num = [i for i in range(len(df_target['date'].values)) if df_target['date'].values[i] == value]
    if num:
        return df_target['total'].values[num[0]]
    return 0

# Get accumulator
def get_accum(df_target, value):
    num = [i for i in range(len(df_target['date'].values)) if df_target['date'].values[i] == value]
    if num:
        return df_target['accum'].values[num[0]]
    return np.nan

# Time line by care [cases, recovered, deaths]
covid_19_time_line_by_care = pd.DataFrame(columns=['date', 'cases', 'accum_cases', 'recovered', 'accum_recovered', 'deaths', 'accum_deaths'])
covid_19_time_line_by_care['date'] = [dti.strftime('%d/%m/%Y') for dti in pd.date_range(start='2020-03-01', end=date.today().isoformat(), freq='D')]

# Cases
covid_19_time_line_by_care['cases'] = covid_19_time_line_by_care['date'].transform(lambda value: get_total(covid_df_cases, value))
covid_19_time_line_by_care['accum_cases'] = covid_19_time_line_by_care['date'].transform(lambda value: get_accum(covid_df_cases, value))
# Recovered
covid_19_time_line_by_care['recovered'] = covid_19_time_line_by_care['date'].transform(lambda value: get_total(covid_df_recovered, value))
covid_19_time_line_by_care['accum_recovered'] = covid_19_time_line_by_care['date'].transform(lambda value: get_accum(covid_df_recovered, value))
# Deaths
covid_19_time_line_by_care['deaths'] = covid_19_time_line_by_care['date'].transform(lambda value: get_total(covid_df_deaths, value))
covid_19_time_line_by_care['accum_deaths'] = covid_19_time_line_by_care['date'].transform(lambda value: get_accum(covid_df_deaths, value))

# Fill NaN values
covid_19_time_line_by_care.fillna(method='ffill', inplace=True)
covid_19_time_line_by_care.fillna(0, inplace=True)
#print(covid_19_time_line_by_care.dtypes)
covid_19_time_line_by_care = covid_19_time_line_by_care.astype({'accum_cases': 'int64', 'accum_recovered': 'int64', 'accum_deaths': 'int64'})

# Remove last day until update it
if covid_df.values[-1][1] != covid_19_time_line_by_care.values[-1][0]:
    covid_19_time_line_by_care.drop([covid_19_time_line_by_care.index[-1]], inplace=True)

# Show dataframe
covid_19_time_line_by_care.tail()

# %% [markdown]
# ## Time Line by Care
# > ***Output file***: covid19_time_line.csv

# %%
# Save dataframe
covid_19_time_line_by_care.to_csv(os.path.join(OUTPUT_DIR, 'covid19_time_line.csv'), index=False)

# %% [markdown]
# ---

# %%
# Care Classes
list(set(covid_df['care'].values))

# %% [markdown]
# ## Time Line by Care by City

# %%
# Time Line by Care by City
cities = []
cities = list(set(covid_df['city'].values))

# Get report by care and city [cases, recovered, deaths]
def get_report_by_care_city(care, city):
    # covid_df_report
    covid_df_report = pd.DataFrame()
    # Check care
    if care == '*':
        covid_df_report = covid_df[covid_df['city'] == city].groupby('date')['date'].count()
    elif care == 'Recuperado':
        covid_df_report = covid_df[((covid_df['care'] == 'Recuperado') | (covid_df['care'] == 'Recuperado (Hospital)')) & (covid_df['city'] == city)].groupby('date')['date'].count()
    else:
        covid_df_report = covid_df[(covid_df['care'] == care) & (covid_df['city'] == city)].groupby('date')['date'].count()
    # Create dateset
    covid_df_report = pd.DataFrame(data={'date': covid_df_report.index, 'total': covid_df_report.values}, columns=['date', 'total'])
    covid_df_report['date_iso'] = pd.to_datetime(covid_df_report['date'], format='%d/%m/%Y')
    covid_df_report = covid_df_report.sort_values(by=['date_iso'], ascending=True)
    covid_df_report['accum'] = covid_df_report['total'].cumsum()
    covid_df_report = covid_df_report.drop(columns=['date_iso'])
    covid_df_report.reset_index(inplace=True, drop=True)
    # Return
    return covid_df_report

# Get time line by care and city
def get_time_line_by_care_city(city):
    # Time line by cases and city
    covid_df_cases = get_report_by_care_city('*', city)
    # Time line by recovered and city
    covid_df_recovered = get_report_by_care_city('Recuperado', city)
    # Time line by deaths and city
    covid_df_deaths = get_report_by_care_city('Fallecido', city)

    # Time line by care and city [cases, recovered, deaths]
    covid_19_time_line_by_care_city = pd.DataFrame(columns=['date', 'cases', 'accum_cases', 'recovered', 'accum_recovered', 'deaths', 'accum_deaths'])
    covid_19_time_line_by_care_city['date'] = [dti.strftime('%d/%m/%Y') for dti in pd.date_range(start='2020-03-01', end=date.today().isoformat(), freq='D')]

    # Cases
    covid_19_time_line_by_care_city['cases'] = covid_19_time_line_by_care_city['date'].transform(lambda value: get_total(covid_df_cases, value))
    covid_19_time_line_by_care_city['accum_cases'] = covid_19_time_line_by_care_city['date'].transform(lambda value: get_accum(covid_df_cases, value))

    # Recovered
    covid_19_time_line_by_care_city['recovered'] = covid_19_time_line_by_care_city['date'].transform(lambda value: get_total(covid_df_recovered, value))
    covid_19_time_line_by_care_city['accum_recovered'] = covid_19_time_line_by_care_city['date'].transform(lambda value: get_accum(covid_df_recovered, value))

    # Deaths
    covid_19_time_line_by_care_city['deaths'] = covid_19_time_line_by_care_city['date'].transform(lambda value: get_total(covid_df_deaths, value))
    covid_19_time_line_by_care_city['accum_deaths'] = covid_19_time_line_by_care_city['date'].transform(lambda value: get_accum(covid_df_deaths, value))

    # Fill NaN values
    covid_19_time_line_by_care_city.fillna(method='ffill', inplace=True)
    covid_19_time_line_by_care_city.fillna(0, inplace=True)
    #print(covid_19_time_line_by_care_city.dtypes)
    covid_19_time_line_by_care_city = covid_19_time_line_by_care_city.astype({'accum_cases': 'int64', 'accum_recovered': 'int64', 'accum_deaths': 'int64'})

    # Remove last day until update it
    if covid_df.values[-1][1] != covid_19_time_line_by_care_city.values[-1][0]:
        covid_19_time_line_by_care_city.drop([covid_19_time_line_by_care_city.index[-1]], inplace=True)

    # Return dataframe
    return covid_19_time_line_by_care_city


# By city
covid_19_time_line_by_care_city = {}
for city in cities:
    #print('city', city)
    # Get time line by care and city
    covid_19_time_line_by_care_city[city] = get_time_line_by_care_city(city)

# %% [markdown]
# ## Time Line by Care and City
# > ***Output file***: covid19_time_line_city.csv

# %%
# Save dataframe
for city in covid_19_time_line_by_care_city:
    #print('city:', city)
    # Save dataframe
    covid_19_time_line_by_care_city[city].to_csv(os.path.join(OUTPUT_DIR, 'covid19_time_line_city_' + city + '.csv'), index=False)

# %% [markdown]
# ---

# %%
# Care Classes
list(set(covid_df['care'].values))

# %% [markdown]
# ## Time Line by Care by Department or District

# %%
# Time Line by Care by Department or District
depts_dists = []
depts_dists = list(set(covid_df['dept_dist'].values))

# Get report by care and dept_dist [cases, recovered, deaths]
def get_report_by_care_dept_dist(care, dept_dist):
    # covid_df_report
    covid_df_report = pd.DataFrame()
    # Check care
    if care == '*':
        covid_df_report = covid_df[covid_df['dept_dist'] == dept_dist].groupby('date')['date'].count()
    elif care == 'Recuperado':
        covid_df_report = covid_df[((covid_df['care'] == 'Recuperado') | (covid_df['care'] == 'Recuperado (Hospital)')) & (covid_df['dept_dist'] == dept_dist)].groupby('date')['date'].count()
    else:
        covid_df_report = covid_df[(covid_df['care'] == care) & (covid_df['dept_dist'] == dept_dist)].groupby('date')['date'].count()
    # Create dateset
    covid_df_report = pd.DataFrame(data={'date': covid_df_report.index, 'total': covid_df_report.values}, columns=['date', 'total'])
    covid_df_report['date_iso'] = pd.to_datetime(covid_df_report['date'], format='%d/%m/%Y')
    covid_df_report = covid_df_report.sort_values(by=['date_iso'], ascending=True)
    covid_df_report['accum'] = covid_df_report['total'].cumsum()
    covid_df_report = covid_df_report.drop(columns=['date_iso'])
    covid_df_report.reset_index(inplace=True, drop=True)
    # Return
    return covid_df_report

# Get time line by care and dept_dist
def get_time_line_by_care_dept_dist(dept_dist):
    # Time line by cases and dept_dist
    covid_df_cases = get_report_by_care_dept_dist('*', dept_dist)
    # Time line by recovered and dept_dist
    covid_df_recovered = get_report_by_care_dept_dist('Recuperado', dept_dist)
    # Time line by deaths and dept_dist
    covid_df_deaths = get_report_by_care_dept_dist('Fallecido', dept_dist)

    # Time line by care and dept_dist [cases, recovered, deaths]
    covid_19_time_line_by_care_dept_dist = pd.DataFrame(columns=['date', 'cases', 'accum_cases', 'recovered', 'accum_recovered', 'deaths', 'accum_deaths'])
    covid_19_time_line_by_care_dept_dist['date'] = [dti.strftime('%d/%m/%Y') for dti in pd.date_range(start='2020-03-01', end=date.today().isoformat(), freq='D')]

    # Cases
    covid_19_time_line_by_care_dept_dist['cases'] = covid_19_time_line_by_care_dept_dist['date'].transform(lambda value: get_total(covid_df_cases, value))
    covid_19_time_line_by_care_dept_dist['accum_cases'] = covid_19_time_line_by_care_dept_dist['date'].transform(lambda value: get_accum(covid_df_cases, value))

    # Recovered
    covid_19_time_line_by_care_dept_dist['recovered'] = covid_19_time_line_by_care_dept_dist['date'].transform(lambda value: get_total(covid_df_recovered, value))
    covid_19_time_line_by_care_dept_dist['accum_recovered'] = covid_19_time_line_by_care_dept_dist['date'].transform(lambda value: get_accum(covid_df_recovered, value))

    # Deaths
    covid_19_time_line_by_care_dept_dist['deaths'] = covid_19_time_line_by_care_dept_dist['date'].transform(lambda value: get_total(covid_df_deaths, value))
    covid_19_time_line_by_care_dept_dist['accum_deaths'] = covid_19_time_line_by_care_dept_dist['date'].transform(lambda value: get_accum(covid_df_deaths, value))

    # Fill NaN values
    covid_19_time_line_by_care_dept_dist.fillna(method='ffill', inplace=True)
    covid_19_time_line_by_care_dept_dist.fillna(0, inplace=True)
    #print(covid_19_time_line_by_care_dept_dist.dtypes)
    covid_19_time_line_by_care_dept_dist = covid_19_time_line_by_care_dept_dist.astype({'accum_cases': 'int64', 'accum_recovered': 'int64', 'accum_deaths': 'int64'})

    # Remove last day until update it
    if covid_df.values[-1][1] != covid_19_time_line_by_care_dept_dist.values[-1][0]:
        covid_19_time_line_by_care_dept_dist.drop([covid_19_time_line_by_care_dept_dist.index[-1]], inplace=True)

    # Return dataframe
    return covid_19_time_line_by_care_dept_dist


# By dept_dist
covid_19_time_line_by_care_dept_dist = {}
for dept_dist in depts_dists:
    #print('dept_dist', dept_dist)
    # Get time line by care and dept_dist
    covid_19_time_line_by_care_dept_dist[dept_dist] = get_time_line_by_care_dept_dist(dept_dist)

# %% [markdown]
# ## Time Line by Care and Department or District
# > ***Output file***: covid19_time_line_dept_dist.csv

# %%
# Save dataframe
for dept_dist in covid_19_time_line_by_care_dept_dist:
    #print('dept_dist:', dept_dist)
    # Save dataframe
    covid_19_time_line_by_care_dept_dist[dept_dist].to_csv(os.path.join(OUTPUT_DIR, 'covid19_time_line_dept_dist_' + dept_dist + '.csv'), index=False)

# %% [markdown]
# ---
# %% [markdown]
# ## Google Community Mobility Reports - Colombia

# %%
# Google Community Mobility Reports - Colombia
google_community_mobility_reports = pd.DataFrame(columns=['date', 'country', 'file', 'url'])
google_community_mobility_reports['date'] = [dti.strftime('%Y-%m-%d') for dti in pd.date_range(start='2020-03-29', end=date.today().isoformat(), freq='D')]
google_community_mobility_reports['country'] = ['Colombia' for country in range(len(google_community_mobility_reports['date'].values))]
google_community_mobility_reports['file'] = [ date + '_CO_Mobility_Report_en.pdf' for date in google_community_mobility_reports['date'].values]
# Get URL report
def get_report_url(file):
    with requests.get('https://www.gstatic.com/covid19/mobility/' + file) as community_mobility_report:
        #print(community_mobility_report.status_code)
        if community_mobility_report.status_code == 200:
            #print('status_code: ', 200)
            #print('url', community_mobility_report.url)
            return community_mobility_report.url
        else:
            return np.nan
# Get URL report
google_community_mobility_reports['url'] = google_community_mobility_reports['file'].transform(lambda value: get_report_url(value))
# Drop any report without URL
google_community_mobility_reports.dropna(inplace=True)
# Reset index
google_community_mobility_reports.reset_index(inplace=True, drop=True)
# Show dataframe
google_community_mobility_reports.head()
#print('community_mobility_report.content', community_mobility_report.content)
            #with open(os.path.join(OUTPUT_DIR, '2020-04-05_CO_Mobility_Report_en.pdf'), 'wb') as f:
            #    f.write(community_mobility_report.content)


# %%
# Add Mobility Changes
#from pdfminer.high_level import extract_pages
# Get mobility changes
def get_mobility_changes(URL):
    # Target changes
    targets = ['Retail & recreation', 'Grocery & pharmacy', 'Parks', 'Transit stations', 'Workplaces', 'Residential']
    # Mobility Changes
    mobility_changes = []
    # Get Mobility Report
    with requests.get(URL) as mobility_report:
        #print(mobility_report.status_code)
        if mobility_report.status_code == 200:
            temp = tempfile.NamedTemporaryFile()
            temp.write(mobility_report.content)
            #print('temp.name:', temp.name)
            with open(temp.name, 'rb') as file:
                # By pages
                pdf_text = []
                page = 0
                while page != -1:
                    text = extract_text(file, maxpages=1, page_numbers=[page])
                    if text:
                        #print('text', text)
                        pdf_text.append(text.split('\n'))
                        page += 1
                    else:
                        page = -1
                # Pages
                #print('Pages:', len(pdf_text))
                # Page 1
                page1 = pdf_text[0]
                page1 = filter(lambda value: value != '', page1)
                page1 = filter(lambda value: value in targets or value[-1] == '%', list(page1))
                page1 = list(page1)[:6]
                # Page 2
                page2 = pdf_text[1]
                page2 = filter(lambda value: value != '', page2)
                page2 = filter(lambda value: value in targets or value[-1] == '%', list(page2))
                page2 = list(page2)[:6]
                # Merge
                mobility_changes = page1 + page2
    return mobility_changes
# Add Mobility Changes
google_community_mobility_reports['mobility_changes'] = google_community_mobility_reports['url'].transform(lambda value: get_mobility_changes(value))
# By case
google_community_mobility_reports['Retail & recreation'] = google_community_mobility_reports['mobility_changes'].transform(lambda value: value[1])
google_community_mobility_reports['Grocery & pharmacy'] = google_community_mobility_reports['mobility_changes'].transform(lambda value: value[3])
google_community_mobility_reports['Parks'] = google_community_mobility_reports['mobility_changes'].transform(lambda value: value[5])
google_community_mobility_reports['Transit stations'] = google_community_mobility_reports['mobility_changes'].transform(lambda value: value[7])
google_community_mobility_reports['Workplaces'] = google_community_mobility_reports['mobility_changes'].transform(lambda value: value[9])
google_community_mobility_reports['Residential'] = google_community_mobility_reports['mobility_changes'].transform(lambda value: value[11])
# Drop column
google_community_mobility_reports.drop(columns=['mobility_changes'], inplace=True)
# Sort columns
google_community_mobility_reports = google_community_mobility_reports[['date', 'country', 'Retail & recreation', 'Grocery & pharmacy', 'Parks', 'Transit stations', 'Workplaces', 'Residential', 'file', 'url']]
# Setup date format
google_community_mobility_reports['date'] = [value.strftime('%d/%m/%Y') for value in pd.to_datetime(google_community_mobility_reports['date'], format='%Y-%m-%d')]
# Show dataframe
google_community_mobility_reports.head()

# %% [markdown]
# ## Google COVID-19 Community Mobility Reports - Colombia
# > ***Output file***: google_community_mobility_reports.csv

# %%
# Save dataframe
google_community_mobility_reports.to_csv(os.path.join(OUTPUT_DIR, 'google_community_mobility_reports.csv'), index=False)

# %% [markdown]
# ---

# %%
# Insights Colombia
# Reading the json as a dict
with requests.get('https://infogram.com/api/live/flex/4524241a-91a7-4bbd-a58e-63c12fb2952f/90df9eae-e3e5-4982-b71c-3e28e3c4273f?') as original_dataset:
    data = original_dataset.json()
#print(data['data'][0])
#print(data['data'][0][1][0])

total_cases = data['data'][0][0][0]
#print(total_cases)
total_cases = total_cases.split('<b>')[1].split('</b>')[0].replace('.', '')

total_recovered = data['data'][0][1][0]
#print(total_recovered)
total_recovered = total_recovered.split('<b>')[1].split('</b>')[0].replace('.', '')

total_deaths = data['data'][0][2][0]
#print(total_deaths)
total_deaths = total_deaths.split('<b>')[1].split('</b>')[0].replace('.', '')

#print('Total Cases:', total_cases)
#print('Total Recovered:', total_recovered)
#print('Total Deaths:', total_deaths)


# %%
# Type of Case
# Reading the json as a dict
with requests.get('https://infogram.com/api/live/flex/4524241a-91a7-4bbd-a58e-63c12fb2952f/a991990b-3b23-4ab2-8452-0ed1162d4896?') as original_dataset:
    data = original_dataset.json()
#print(data['data'][0])
#print(data['data'][0][0])

type_imported = data['data'][0][0][0]

type_related = data['data'][0][1][0]

type_study = data['data'][0][2][0]


#print('Total Importado:', type_imported)
#print('Total Relacionado:', type_related)
#print('Total Estudio:', type_study)

# %% [markdown]
# ## Resume

# %%
# Resume
data = []
# cases_by_care_by_date[N] = ['Hospital', 'Hospital UCI', 'Casa', 'Fallecido', 'Recuperado', 'Recuperado (Hospital)']
# Resume Attributes
data.append(['Confirmados', total_cases])
data.append(['Recuperados', total_recovered])
data.append(['Fallecidos', total_deaths])
data.append(['Muestras descartadas', samples_descarted])
data.append(['Importado', type_imported])
data.append(['Relacionado', type_related])
data.append(['En estudio', type_study])
data.append(['Muestras procesadas', samples_processed])

# Resume Dataframe
covid_df_resume = pd.DataFrame(data=data, columns=['title', 'total'])
# Show dataframe
covid_df_resume.head(10)

# %% [markdown]
# ## Resume
# > ***Output file***: covid19_resume.csv

# %%
# Save dataframe
covid_df_resume.to_csv(os.path.join(OUTPUT_DIR, 'covid19_resume.csv'), index=False)
print('\nColombia Covid19 Resumen:')
print(covid_df_resume)

# %% [markdown]
# ---

# %%


