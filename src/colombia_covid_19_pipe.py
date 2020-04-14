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
from datetime import date
from calendar import day_name, month_name

import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
# Short ID
#try:
#    from shortid import ShortId
#except Exception:
#    install('shortid')
#    from shortid import ShortId
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
# [INS - Official Report](https://e.infogram.com/api/live/flex/bc384047-e71c-47d9-b606-1eb6a29962e3/664bc407-2569-4ab8-b7fb-9deb668ddb7a)
# 
# The number of new cases are increasing day by day around the world.
# This dataset has information about reported cases from 32 Colombia departments.
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
# URL original dataset
URL_DATASET = 'https://e.infogram.com/api/live/flex/bc384047-e71c-47d9-b606-1eb6a29962e3/664bc407-2569-4ab8-b7fb-9deb668ddb7a'


# %%
# Reading the json as a dict
with requests.get(URL_DATASET) as original_dataset:
    data = original_dataset.json()
#print(data)

# Get attributes and data
attrs = data['data'][0][0]
del data['data'][0][0]
data = data['data'][0]

# Build dataframe
covid_df = pd.DataFrame(data=data, columns=attrs)

# Size dataframe
covid_df.shape


# %%
# Show dataframe
covid_df.tail()


# %%
# Rename columns
covid_df.rename(columns={
    "ID de caso": "id_case",
    "Fecha de diagnóstico": "date",
    "Ciudad de ubicación": "city",
    "Departamento o Distrito": "dept_dist",
    "Atención**": "care",
    "Edad": "age",
    "Sexo": "sex",
    "Tipo*": "kind",
    "País de procedencia": "country_origin"}, inplace=True)
# Show dataframe
covid_df.head()


# %%
# Clean empty rows
covid_df = covid_df[(covid_df['id_case'] != '') | (covid_df['date'] != '')]
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
covid_df['date'] = [value.strftime('%d/%m/%Y') for value in pd.to_datetime(covid_df['date'], format='%d/%m/%Y')]
covid_df.head()


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
#covid_df['id_case'] = covid_df['id_case'].transform(lambda value: ShortId().generate())
#covid_df['id_case'] = covid_df['sex'] + covid_df['id_case'] + covid_df['age']
#covid_df.head()
covid_df['id_case'] = covid_df.index
covid_df.tail()


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
covid_df.head()

# %% [markdown]
# ## Covid 19 Dataset
# > ***Output file***: covid19.csv

# %%
# Save dataframe
covid_df.to_csv(os.path.join(OUTPUT_DIR, 'covid19.csv'), index=False)

# %% [markdown]
# ---

# %%
# Cases by Date
covid_df_by_date = covid_df.groupby('date')['date'].count()
covid_df_by_date = pd.DataFrame(data={'date': covid_df_by_date.index, 'total': covid_df_by_date.values}, columns=['date', 'total'])
covid_df_by_date['date_iso'] = pd.to_datetime(covid_df_by_date['date'], format='%d/%m/%Y')
covid_df_by_date = covid_df_by_date.sort_values(by=['date_iso'], ascending=True)
covid_df_by_date['cumsum'] = covid_df_by_date['total'].cumsum()
covid_df_by_date = covid_df_by_date.drop(columns=['date_iso'])
covid_df_by_date.reset_index(inplace=True, drop=True)
# Show dataframe
covid_df_by_date.tail()

# %% [markdown]
# ## Cases by Date
# > ***Output file***: covid19_by_date.csv

# %%
# Save dataframe
covid_df_by_date.to_csv(os.path.join(OUTPUT_DIR, 'covid19_by_date.csv'), index=False)

# %% [markdown]
# ---

# %%
# Cases by Care
covid_df_by_care = covid_df.groupby('care')['care'].count().sort_values(ascending=False)
covid_df_by_care = pd.DataFrame(data={'care': covid_df_by_care.index, 'total': covid_df_by_care.values}, columns=['care', 'total'])
# Show dataframe
covid_df_by_care.head()

# %% [markdown]
# ## Cases by Care
# > ***Output file***: covid19_by_care.csv

# %%
# Save dataframe
covid_df_by_care.to_csv(os.path.join(OUTPUT_DIR, 'covid19_by_care.csv'), index=False)

# %% [markdown]
# ---

# %%
# Cases by Sex
covid_df_by_sex = covid_df.groupby('sex')['sex'].count().sort_values(ascending=False)
covid_df_by_sex = pd.DataFrame(data={'sex': covid_df_by_sex.index, 'total': covid_df_by_sex.values}, columns=['sex', 'total'])
# Show dataframe
covid_df_by_sex.head()

# %% [markdown]
# ## Cases by Sex
# > ***Output file***: covid19_by_sex.csv

# %%
# Save dataframe
covid_df_by_sex.to_csv(os.path.join(OUTPUT_DIR, 'covid19_by_sex.csv'), index=False)

# %% [markdown]
# ---

# %%
# Cases by Age
covid_df_by_age = covid_df.groupby('age')['age'].count().sort_values(ascending=False)
covid_df_by_age = pd.DataFrame(data={'age': covid_df_by_age.index, 'total': covid_df_by_age.values}, columns=['age', 'total'])
# Show dataframe
covid_df_by_age.head()

# %% [markdown]
# ## Cases by Age
# > ***Output file***: covid19_by_age.csv

# %%
# Save dataframe
covid_df_by_age.to_csv(os.path.join(OUTPUT_DIR, 'covid19_by_age.csv'), index=False)

# %% [markdown]
# ---

# %%
# Cases by Age and Sex
covid_df_by_age_sex = covid_df.groupby(['age', 'sex'])['id_case'].count().sort_values(ascending=False)
covid_df_by_age_sex = pd.DataFrame(data={'age': covid_df_by_age_sex.index.get_level_values('age'), 'sex': covid_df_by_age_sex.index.get_level_values('sex'), 'total': covid_df_by_age_sex.values}, columns=['age', 'sex', 'total'])
# Show dataframe
covid_df_by_age_sex.head()

# %% [markdown]
# ## Cases by Age and Sex
# > ***Output file***: covid19_by_age_sex.csv

# %%
# Save dataframe
covid_df_by_age_sex.to_csv(os.path.join(OUTPUT_DIR, 'covid19_by_age_sex.csv'), index=False)

# %% [markdown]
# ---

# %%
# Build dataframe by Age and Sex using intervals
def age_sex_intervals(dataframe):
    intervals = []
    i = 0
    while i < 100:
        interval_i = dataframe[(dataframe['age'] >= i) & (dataframe['age'] < i+10)]
        interval_i = interval_i.groupby('sex')['total'].sum().sort_values(ascending=False)
        if len(interval_i.values) > 0:
            interval_i = pd.DataFrame(data={'age': [ str(i) + '-' + str(i+9), str(i) + '-' + str(i+9)], 'sex': interval_i.index, 'total': interval_i.values}, columns=['age', 'sex', 'total'])
            intervals.append(interval_i)
        i = i + 10
    return pd.concat(intervals).reset_index(drop=True)
# Cases by Age and Sex using intervals
covid_df_by_age_sex_interval = covid_df_by_age_sex
covid_df_by_age_sex_interval['age'] = pd.to_numeric(covid_df_by_age_sex_interval['age'])
covid_df_by_age_sex_interval = age_sex_intervals(covid_df_by_age_sex_interval)
covid_df_by_age_sex_interval.sort_values(ascending=False, inplace=True, by=['total'])
# Show dataframe
covid_df_by_age_sex_interval.head()

# %% [markdown]
# ## Cases by Age and Sex Interval
# > ***Output file***: covid19_by_age_sex_interval.csv

# %%
# Save dataframe
covid_df_by_age_sex_interval.to_csv(os.path.join(OUTPUT_DIR, 'covid19_by_age_sex_interval.csv'), index=False)

# %% [markdown]
# ---

# %%
# Cases by City
covid_df_by_city = covid_df.groupby('city')['city'].count().sort_values(ascending=False)
covid_df_by_city = pd.DataFrame(data={'city': covid_df_by_city.index, 'total': covid_df_by_city.values}, columns=['city', 'total'])
# Show dataframe
covid_df_by_city.head()


# %%
# Find city geolocation
def findgeopoint(city):
    geo = geolocator.geocode(city + ', Colombia')
    if geo:
        return geo.point
    else:
        return geolocator.geocode('Colombia').point


# %%
# Add city geolocation
covid_df_by_city['geo'] = covid_df_by_city['city'].transform(lambda value: findgeopoint(value))
# Add city latitude and longitude
covid_df_by_city['lat'] = covid_df_by_city['geo'].transform(lambda value: value.latitude)
covid_df_by_city['lng'] = covid_df_by_city['geo'].transform(lambda value: value.longitude)
covid_df_by_city = covid_df_by_city.drop(columns=['geo'])
# Show dataframe
covid_df_by_city

# %% [markdown]
# ## Cases by City
# > ***Output file***: covid19_by_city.csv

# %%
# Save dataframe
covid_df_by_city.to_csv(os.path.join(OUTPUT_DIR, 'covid19_by_city.csv'), index=False)

# %% [markdown]
# ---

# %%
# Cases by Department or District
covid_df_by_dept_dist = covid_df.groupby('dept_dist')['dept_dist'].count().sort_values(ascending=False)
covid_df_by_dept_dist = pd.DataFrame(data={'dept_dist': covid_df_by_dept_dist.index, 'total': covid_df_by_dept_dist.values}, columns=['dept_dist', 'total'])
# Show dataframe
covid_df_by_dept_dist.head()


# %%
# Add dept_dist geolocation
covid_df_by_dept_dist['geo'] = covid_df_by_dept_dist['dept_dist'].transform(lambda value: findgeopoint(value))
# Add city latitude and longitude
covid_df_by_dept_dist['lat'] = covid_df_by_dept_dist['geo'].transform(lambda value: value.latitude)
covid_df_by_dept_dist['lng'] = covid_df_by_dept_dist['geo'].transform(lambda value: value.longitude)
covid_df_by_dept_dist = covid_df_by_dept_dist.drop(columns=['geo'])
# Show dataframe
covid_df_by_dept_dist.head()

# %% [markdown]
# ## Cases by Department or District
# > ***Output file***: covid19_by_dept_dist.csv

# %%
# Save dataframe
covid_df_by_dept_dist.to_csv(os.path.join(OUTPUT_DIR, 'covid19_by_dept_dist.csv'), index=False)

# %% [markdown]
# ---

# %%
# Cases by Care by Date
#list_care = list(set(covid_df['care'].values))
list_care = ['Hospital', 'Hospital UCI', 'Casa', 'Fallecido', 'Recuperado']
#print('list_care', list_care)
cases_by_care_by_date = []
# Each Care
for care in list_care:
    covid_df_care_by_date = covid_df[covid_df['care'] == care]
    covid_df_care_by_date = covid_df_care_by_date.groupby('date')['date'].count()
    covid_df_care_by_date = pd.DataFrame(data={'date': covid_df_care_by_date.index, 'care': ([care] * len(covid_df_care_by_date.index)), 'total': covid_df_care_by_date.values}, columns=['date', 'care', 'total'])
    covid_df_care_by_date['date_iso'] = pd.to_datetime(covid_df_care_by_date['date'], format='%d/%m/%Y')
    covid_df_care_by_date = covid_df_care_by_date.sort_values(by=['date_iso'], ascending=True)
    covid_df_care_by_date['cumsum'] = covid_df_care_by_date['total'].cumsum()
    covid_df_care_by_date = covid_df_care_by_date.drop(columns=['date_iso'])
    covid_df_care_by_date.reset_index(inplace=True, drop=True)
    cases_by_care_by_date.append(covid_df_care_by_date)
# Show dataframe
#for i, care in enumerate(list_care):
#    print(care, '\n', cases_by_care_by_date[i].tail())

# %% [markdown]
# ## Cases by Care by Date
# > ***Output files***: covid19_cases_by_care_by_date_(int).csv

# %%
# Save dataframe
list_care_file = ['hospital', 'uci', 'casa', 'fallecido', 'recuperado']
for i, care in enumerate(list_care):
    cases_by_care_by_date[i].to_csv(os.path.join(OUTPUT_DIR, 'covid19_cases_by_' + list_care_file[i] + '_by_date.csv'), index=False)

# %% [markdown]
# ---

# %%
# Cases by Country Origin
covid_df_by_country_origin = covid_df.groupby('country_origin')['country_origin'].count().sort_values(ascending=False)
covid_df_by_country_origin = pd.DataFrame(data={'country_origin': covid_df_by_country_origin.index, 'total': covid_df_by_country_origin.values}, columns=['country_origin', 'total'])
# Show dataframe
covid_df_by_country_origin.head()

# %% [markdown]
# ## Cases by Country Origin
# > ***Output file***: covid19_by_country_origin.csv

# %%
# Save dataframe
covid_df_by_country_origin.to_csv(os.path.join(OUTPUT_DIR, 'covid19_by_country_origin.csv'), index=False)

# %% [markdown]
# ---

# %%
# Cases by Kind
covid_df_by_kind = covid_df.groupby('kind')['kind'].count().sort_values(ascending=False)
covid_df_by_kind = pd.DataFrame(data={'kind': covid_df_by_kind.index, 'total': covid_df_by_kind.values}, columns=['kind', 'total'])
# Show dataframe
covid_df_by_kind.head()

# %% [markdown]
# ## Cases by Kind
# > ***Output file***: covid19_by_kind.csv

# %%
# Save dataframe
covid_df_by_kind.to_csv(os.path.join(OUTPUT_DIR, 'covid19_by_kind.csv'), index=False)

# %% [markdown]
# ---

# %%
# Descarted Cases
# Reading the json as a dict
with requests.get('https://infogram.com/api/live/flex/5eb73bf0-6714-4bac-87cc-9ef0613bf697/c9a25571-e7c5-43c6-a7ac-d834a3b5e872?') as original_dataset:
    data = original_dataset.json()
#print(data['data'][0][4][0])

# Get attributes and data
attrs = data['data'][0][4][0]
del data
#print(attrs)
descarted_cases = attrs.split('<b>')[1].split('</b>')[0].replace('.', '')
#print('Descarted Cases:', descarted_cases)

# %% [markdown]
# ---

# %%
# Samples Processed
# Reading the json as a dict
with requests.get('https://infogram.com/api/live/flex/bc384047-e71c-47d9-b606-1eb6a29962e3/523ca417-2781-47f0-87e8-1ccc2d5c2839?') as original_dataset:
    data = original_dataset.json()
#print(data['data'])
#print(data['data'][2])

# Get attributes and data
attrs = data['data'][2][0]
attrs[0] = 'Periodo'
del data['data'][2][0]
#print(attrs)
data = data['data'][2]
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
# ## Samples Processed
# > ***Output file***: covid19_samples_processed.csv

# %%
# Save dataframe
covid_df_samples_processed.to_csv(os.path.join(OUTPUT_DIR, 'covid19_samples_processed.csv'), index=False)

# %% [markdown]
# ---

# %%
# Resume
data = []
# cases_by_care_by_date[N] = ['Hospital', 'Hospital UCI', 'Casa', 'Fallecido', 'Recuperado']
# Resume Attributes
data.append(['Confirmados', covid_df_by_date.values[-1][-1]])
data.append(['Recuperados', cases_by_care_by_date[4].values[-1][-1]])
data.append(['Muertes', cases_by_care_by_date[3].values[-1][-1]])
data.append(['Casos descartados', descarted_cases])
data.append(['Importado', covid_df_by_kind[covid_df_by_kind['kind'] == 'Importado'].values[0][-1]])
data.append(['Relacionado', covid_df_by_kind[covid_df_by_kind['kind'] == 'Relacionado'].values[0][-1]])
data.append(['En estudio', covid_df_by_kind[covid_df_by_kind['kind'] == 'En estudio'].values[0][-1]])
data.append(['Muestras procesadas', covid_df_samples_processed.values[-1][-1]])

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
print('\nColombia Covid 19 Resumen:')
print(covid_df_resume)

# %% [markdown]
# ---

# %%
# Get time line by care [cases, recovered, deaths]
def get_time_line_by_care(care):
    # covid_df_report
    covid_df_report = pd.DataFrame()
    # Check care
    if care == '*':
        covid_df_report = covid_df.groupby('date')['date'].count()
    else:
        covid_df_report = covid_df[covid_df['care'] == care].groupby('date')['date'].count()
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
# > ***Output file***: covid_19_time_line_city.csv

# %%
# Save dataframe
for city in covid_19_time_line_by_care_city:
    #print('city:', city)
    # Save dataframe
    covid_19_time_line_by_care_city[city].to_csv(os.path.join(OUTPUT_DIR, 'covid_19_time_line_city_' + city + '.csv'), index=False)

# %% [markdown]
# ---

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
# > ***Output file***: covid_19_time_line_dept_dist.csv

# %%
# Save dataframe
for dept_dist in covid_19_time_line_by_care_dept_dist:
    #print('dept_dist:', dept_dist)
    # Save dataframe
    covid_19_time_line_by_care_dept_dist[dept_dist].to_csv(os.path.join(OUTPUT_DIR, 'covid_19_time_line_dept_dist_' + dept_dist + '.csv'), index=False)

# %% [markdown]
# ---

# %%
# Time line Google Community Mobility Reports - Colombia
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


