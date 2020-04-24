# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

# Dependencies
import numpy as np
import pandas as pd
import requests
import unidecode
import datetime
import dateutil
import subprocess
import sys
import json
import tempfile
import os

# Install missing dependencies
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
# PDFMiner pdfminer.six
try:
    from pdfminer.high_level import extract_text
except Exception:
    install('pdfminer.six')
    from pdfminer.high_level import extract_text

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

#for dirname, _, filenames in os.walk('/kaggle/input'):
#    for filename in filenames:
#        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.

# %% [markdown]
# ---
# %% [markdown]
# # Colombia Covid19 Pipeline
# Dataset obtained from [Instituto Nacional de Salud](https://www.ins.gov.co/Noticias/Paginas/Coronavirus.aspx) daily report Covid19 from Colombia.
# 
# You can get the official dataset here: 
# [INS - Official Report](https://www.datos.gov.co/Salud-y-Protecci-n-Social/Casos-positivos-de-COVID-19-en-Colombia/gt2j-8ykr)
# 
# The number of new cases are increasing day by day around the world.
# This dataset has information about reported cases from 32 Colombia departments.
# 
# Also you can get the dataset Google COVID-19 Community Mobility Reports - Colombia.
# 
# You can view and collaborate to the analysis here:
# [colombia_covid_19_analysis](https://www.kaggle.com/sebaxtian/colombia-covid-19-analysis) Kaggle Notebook Kernel.
# %% [markdown]
# ---
# %% [markdown]
# ## Data Sources

# %%
# Input data files are available in the "../input/" directory.
INPUT_DIR = './'
if os.path.split(os.path.abspath('.'))[-1] == 'src':
    INPUT_DIR = '../input'
# Output data files are available in the "../output/" directory.
OUTPUT_DIR = './'
if os.path.split(os.path.abspath('.'))[-1] == 'src':
    OUTPUT_DIR = '../output'
# Official Daily Report Until Now
URL_OFFICIAL_DATASET = 'https://www.datos.gov.co/api/views/gt2j-8ykr/rows.csv?accessType=DOWNLOAD'
# Official Daily Samples Processed
URL_SAMPLES_PROCESSED = 'https://infogram.com/api/live/flex/4524241a-91a7-4bbd-a58e-63c12fb2952f/96848e74-6055-4aa8-9944-502bf69ef6fc?'

# %% [markdown]
# ---
# %% [markdown]
# ## Official Covid19 Colombia Daily Report

# %%
# Official Daily Report Until Now
with requests.get(URL_OFFICIAL_DATASET) as official_dataset:
    with open(os.path.join(INPUT_DIR, 'covid19co_official.csv'), 'wb') as dataset_file:
        dataset_file.write(official_dataset.content)


# %%
# Open Official Daily Report
covid19co = pd.read_csv(os.path.join(INPUT_DIR, 'covid19co_official.csv'))
# Total Daily Report
covid19co.shape


# %%
# Show dataframe
covid19co.tail()


# %%
# Show attributes
list(covid19co.columns.values)


# %%
# Update Name Columns
# Remove Accents and Uppercase
covid19co.columns = [unidecode.unidecode(value).upper() for value in covid19co.columns]
# Show dataframe
covid19co.head()


# %%
# Update texto to title text format
for attr in covid19co.columns:
    if covid19co[attr].dtypes == 'object':
        covid19co[attr] = covid19co[attr].transform(lambda value: str(value).title())
# Show dataframe
covid19co.head()


# %%
# Fill NaN Values
if covid19co.isna().sum().sum() > 0:
    covid19co.fillna(value='-', inplace=True)
# Show dataframe
covid19co.head()


# %%
# Setup Date Format
def setup_date(value):
    try:
        value = value.split('T')[0].split('-')
        if len(value) == 3:
            value = value[2] + '/' + value[1] + '/' + value[0]
        else:
            value = '-'
    except IndexError:
        value = '-'
    if len(value) != 10 and len(value) != 1:
        value = '-'
    return value
# Date Columns
date_columns = list(filter(lambda value: value.find('FECHA') != -1 or value.find('FIS') != -1, covid19co.columns))
# For each date column
for date_column in date_columns:
    covid19co[date_column] = covid19co[date_column].transform(lambda value: setup_date(value))
# Show dataframe
covid19co.head()


# %%
# Add Day, Month, Year, Month Name and Day Name for each Date

# Spanish
nombre_mes = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
nombre_dia = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

# Get day
def get_day(value):
    if value not in '-':
        return value.split('/')[0]
    return value
# Get month
def get_month(value):
    if value not in '-':
        return value.split('/')[1]
    return value
# Get year
def get_year(value):
    if value not in '-':
        return value.split('/')[2]
    return value
# Get month name
def get_month_name(value):
    if value not in '-':
        return nombre_mes[int(value.split('/')[1]) - 1]
    return value
# Get weekday
def get_weekday(value):
    if value not in '-':
        return nombre_dia[datetime.date(int(value.split('/')[2]), int(value.split('/')[1]), int(value.split('/')[0])).weekday()]
    return value

# For each date column
for date_column in date_columns:
    covid19co[date_column + ' DIA'] = covid19co[date_column].transform(lambda value: get_day(value))
    covid19co[date_column + ' MES'] = covid19co[date_column].transform(lambda value: get_month(value))
    covid19co[date_column + ' ANIO'] = covid19co[date_column].transform(lambda value: get_year(value))
    covid19co[date_column + ' NOMBRE MES'] = covid19co[date_column].transform(lambda value: get_month_name(value))
    covid19co[date_column + ' DIA SEMANA'] = covid19co[date_column].transform(lambda value: get_weekday(value))
# Show dataframe
covid19co.head()

# %% [markdown]
# ## Covid19 Colombia Dataset
# > ***Output file***: covid19co.csv

# %%
# Save dataframe
covid19co.to_csv(os.path.join(OUTPUT_DIR, 'covid19co.csv'), index=False)

# %% [markdown]
# ---
# %% [markdown]
# ## Official Covid19 Colombia Samples Processed

# %%
# Official Samples Processed Until Now
with requests.get(URL_SAMPLES_PROCESSED) as official_dataset:
    with open(os.path.join(INPUT_DIR, 'covid19co_samples_processed_official.json'), 'w') as json_file:
        json_data = official_dataset.json()
        del json_data['refreshed']
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)


# %%
# Open Official Samples Processed
with open(os.path.join(INPUT_DIR, 'covid19co_samples_processed_official.json')) as official_dataset:
    official_dataset = json.load(official_dataset)
# Official Samples Processed
official_dataset = official_dataset['data'][0]
covid19co_samples_processed = pd.DataFrame(columns=official_dataset[0], data=official_dataset[1:])
# Total Daily Report
covid19co_samples_processed.shape


# %%
# Show dataframe
covid19co_samples_processed.head()


# %%
# Update Name Columns
# Remove Accents and Uppercase
covid19co_samples_processed.columns = [unidecode.unidecode(value).upper() for value in covid19co_samples_processed.columns]
# Show dataframe
covid19co_samples_processed.head()


# %%
# Setup Date Format
def setup_date_samples(value):
    #print('date:', value)
    try:
        value = value.split('/')
        #print(len(value))
        if len(value) == 3:
            # Month
            if len(value[0]) == 1:
                value[0] = '0' + value[0]
            # Day
            if len(value[1]) == 1:
                value[1] = '0' + value[1]
            # Year
            if len(value[2]) == 2:
                value[2] = value[2] + '20'
            # Date
            value = value[1] + '/' + value[0] + '/' + value[2]
        else:
            value = '-'
    except IndexError:
        value = '-'
    #print('VALUE:', value)
    if len(value) != 10 and len(value) != 1:
        value = '-'
    return value
# Setup Date Format
covid19co_samples_processed['FECHA'] = covid19co_samples_processed['FECHA'].transform(lambda value: setup_date_samples(value))
# Show dataframe
covid19co_samples_processed.head()

# %% [markdown]
# ## Covid19 Colombia Samples Processed Dataset
# > ***Output file***: covid19co_samples_processed.csv

# %%
# Save dataframe
covid19co_samples_processed.to_csv(os.path.join(OUTPUT_DIR, 'covid19co_samples_processed.csv'), index=False)

# %% [markdown]
# ---
# %% [markdown]
# ## Google Community Mobility Reports - Colombia

# %%
# Google Community Mobility Reports - Colombia
google_community_mobility_reports = pd.DataFrame(columns=['date', 'country', 'file', 'url'])
google_community_mobility_reports['date'] = [dti.strftime('%Y-%m-%d') for dti in pd.date_range(start='2020-03-29', end=datetime.date.today().isoformat(), freq='D')]
google_community_mobility_reports['country'] = 'Colombia'
google_community_mobility_reports['file'] = [date + '_CO_Mobility_Report_en.pdf' for date in google_community_mobility_reports['date'].values]
# Get URL report
def get_report_url(file):
    with requests.get('https://www.gstatic.com/covid19/mobility/' + file) as community_mobility_report:
        if community_mobility_report.status_code == 200:
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


# %%
# Get/Add Mobility Changes
def get_mobility_changes(URL):
    # Target changes
    targets = ['Retail & recreation', 'Grocery & pharmacy', 'Parks', 'Transit stations', 'Workplaces', 'Residential']
    # Mobility Changes
    mobility_changes = []
    # Get Mobility Report
    with requests.get(URL) as mobility_report:
        if mobility_report.status_code == 200:
            temp = tempfile.NamedTemporaryFile()
            temp.write(mobility_report.content)
            with open(temp.name, 'rb') as file:
                # By pages
                pdf_text = []
                page = 0
                while page != -1:
                    text = extract_text(file, maxpages=1, page_numbers=[page])
                    if text:
                        pdf_text.append(text.split('\n'))
                        page += 1
                    else:
                        page = -1
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
# ## Google Community Mobility Reports - Colombia
# > ***Output file***: google_community_mobility_reports.csv

# %%
# Save dataframe
google_community_mobility_reports.to_csv(os.path.join(OUTPUT_DIR, 'google_community_mobility_reports.csv'), index=False)

# %% [markdown]
# ---

# %%


