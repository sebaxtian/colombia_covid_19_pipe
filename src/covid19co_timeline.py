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
import re

# Install missing dependencies
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

#for dirname, _, filenames in os.walk('/kaggle/input'):
#    for filename in filenames:
#        print(os.path.join(dirname, filename))

# Any results you write to the current directory are saved as output.

# %% [markdown]
# ---
# %% [markdown]
# # Colombia Covid19 Time Line
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


# %%
# Covid19 Colombia Dataset
covid19co = pd.read_csv(os.path.join(OUTPUT_DIR, 'covid19co.csv'))
# Total Covid19 Colombia
covid19co.shape


# %%
# Covid19 Colombia Samples Processed Dataset
covid19co_samples_processed = pd.read_csv(os.path.join(OUTPUT_DIR, 'covid19co_samples_processed.csv'))
# Total Covid19 Colombia Samples Processed
covid19co_samples_processed.shape

# %% [markdown]
# ---
# %% [markdown]
# ## Time Line Reported, Recupered and Deceased

# %%
# Show dataframe
covid19co.head()


# %%
# Get Time Line
def get_time_line(dfreport):
    # Time Line [date, total, accum]
    dfreport_time_line = pd.DataFrame(columns=['date', 'total', 'accum'])
    dfreport_time_line['date'] = [dti.strftime('%d/%m/%Y') for dti in pd.date_range(start='2020-03-01', end=datetime.date.today().isoformat(), freq='D')]
    # Total by Date
    total_by_date = {}
    # Group by 'FECHA REPORTE WEB'
    group_by_date = dfreport.groupby(['FECHA REPORTE WEB'], sort=False)
    # For each date
    for date_report in group_by_date.groups.keys():
        total_by_date[date_report] = group_by_date.get_group(date_report)['ID DE CASO'].count()
    # Update Total by Date
    dfreport_time_line['total'] = dfreport_time_line['date'].transform(lambda date: total_by_date[date] if date in total_by_date else 0)
    # Update Accumulative Sum Cases Reported by Date
    dfreport_time_line['accum'] = dfreport_time_line['total'].cumsum()
    # Drop the last one if doesn't have total
    #index_empty = dfreport_time_line[dfreport_time_line['date'] == datetime.date.today().strftime('%d/%m/%Y')]
    #index_empty = index_empty[index_empty['total'] == 0].index
    #dfreport_time_line.drop(index_empty, inplace=True)
    # Return
    return dfreport_time_line


# %%
# Get Reported Time Line
reported_time_line = get_time_line(covid19co)
# Rename columns
reported_time_line.columns = ['date', 'total_reported', 'accum_reported']
# Show dataframe
reported_time_line.tail()


# %%
# Get Recupered Time Line
dfrecupered = covid19co[covid19co['ATENCION'] == 'Recuperado']
# Get Recupered Time Line
recupered_time_line = get_time_line(dfrecupered)
# Rename columns
recupered_time_line.columns = ['date_recupered', 'total_recupered', 'accum_recupered']
# Show dataframe
recupered_time_line.tail()


# %%
# Get Deceased Time Line
dfdeceased = covid19co[covid19co['ATENCION'] == 'Fallecido']
# Get Deceased Time Line
deceased_time_line = get_time_line(dfdeceased)
# Rename columns
deceased_time_line.columns = ['date_deceased', 'total_deceased', 'accum_deceased']
# Show dataframe
deceased_time_line.tail()


# %%
# Merge Time Lines
covid19co_time_line = pd.concat([reported_time_line, recupered_time_line, deceased_time_line], axis=1, sort=False)
# Delete Columns
covid19co_time_line.drop(columns=['date_recupered', 'date_deceased'], inplace=True)
# Show dataframe
covid19co_time_line.tail()

# %% [markdown]
# ## Time Line Reported, Recupered and Deceased
# > ***Output file***: covid19co_time_line.csv

# %%
# Save dataframe
covid19co_time_line.to_csv(os.path.join(OUTPUT_DIR, 'covid19co_time_line.csv'), index=False)

# %% [markdown]
# ---
# %% [markdown]
# ## Time Line Reported, Recupered and Deceased by City

# %%
# List of Cities
cities = list(set(covid19co['CIUDAD DE UBICACION'].values))
# Show total cities
len(cities)


# %%
# Time Line by City
time_line_by_city = {}
# For each city
for city in cities:
    # Filter by City
    covid19co_city = covid19co[covid19co['CIUDAD DE UBICACION'] == city]
    # Get Reported Time Line
    reported_time_line = get_time_line(covid19co_city)
    # Rename columns
    reported_time_line.columns = ['date', 'total_reported', 'accum_reported']
    # Get Recupered Time Line
    dfrecupered = covid19co_city[covid19co_city['ATENCION'] == 'Recuperado']
    # Get Recupered Time Line
    recupered_time_line = get_time_line(dfrecupered)
    # Rename columns
    recupered_time_line.columns = ['date_recupered', 'total_recupered', 'accum_recupered']
    # Get Deceased Time Line
    dfdeceased = covid19co_city[covid19co_city['ATENCION'] == 'Fallecido']
    # Get Deceased Time Line
    deceased_time_line = get_time_line(dfdeceased)
    # Rename columns
    deceased_time_line.columns = ['date_deceased', 'total_deceased', 'accum_deceased']
    # Merge Time Lines
    covid19co_time_line = pd.concat([reported_time_line, recupered_time_line, deceased_time_line], axis=1, sort=False)
    # Delete Columns
    covid19co_time_line.drop(columns=['date_recupered', 'date_deceased'], inplace=True)
    # Create key city
    key_city = ''.join(x for x in re.sub('[^A-Za-z0-9 ]+', '', unidecode.unidecode(city)).title() if not x.isspace())
    # Add to dict
    time_line_by_city[key_city] = covid19co_time_line


# %%
# Show time line by city keys
#list(time_line_by_city.keys())


# %%
# Show dataframe
time_line_by_city['Cali'].tail()

# %% [markdown]
# ## Time Line Reported, Recupered and Deceased by City
# > ***Output file***: covid19co_time_line_{key_city}.csv

# %%
for key_city in time_line_by_city:
    # Save dataframe
    time_line_by_city[key_city].to_csv(os.path.join(OUTPUT_DIR, 'covid19co_time_line_' + key_city + '.csv'), index=False)

# %% [markdown]
# ---
# %% [markdown]
# ## Time Line Reported, Recupered and Deceased by Department

# %%
# List of Departments
departs = list(set(covid19co['DEPARTAMENTO O DISTRITO '].values))
# Show total departments
len(departs)


# %%
# Time Line by Department
time_line_by_depto = {}
# For each deparment
for deparment in departs:
    # Filter by Department
    covid19co_depto = covid19co[covid19co['DEPARTAMENTO O DISTRITO '] == deparment]
    # Get Reported Time Line
    reported_time_line = get_time_line(covid19co_depto)
    # Rename columns
    reported_time_line.columns = ['date', 'total_reported', 'accum_reported']
    # Get Recupered Time Line
    dfrecupered = covid19co_depto[covid19co_depto['ATENCION'] == 'Recuperado']
    # Get Recupered Time Line
    recupered_time_line = get_time_line(dfrecupered)
    # Rename columns
    recupered_time_line.columns = ['date_recupered', 'total_recupered', 'accum_recupered']
    # Get Deceased Time Line
    dfdeceased = covid19co_depto[covid19co_depto['ATENCION'] == 'Fallecido']
    # Get Deceased Time Line
    deceased_time_line = get_time_line(dfdeceased)
    # Rename columns
    deceased_time_line.columns = ['date_deceased', 'total_deceased', 'accum_deceased']
    # Merge Time Lines
    covid19co_time_line = pd.concat([reported_time_line, recupered_time_line, deceased_time_line], axis=1, sort=False)
    # Delete Columns
    covid19co_time_line.drop(columns=['date_recupered', 'date_deceased'], inplace=True)
    # Create key depto
    key_depto = ''.join(x for x in re.sub('[^A-Za-z0-9 ]+', '', unidecode.unidecode(deparment)).title() if not x.isspace())
    # Add to dict
    time_line_by_depto[key_depto] = covid19co_time_line


# %%
# Show time line by deparment keys
#list(time_line_by_depto.keys())


# %%
# Show dataframe
time_line_by_depto['ValleDelCauca'].tail()

# %% [markdown]
# ## Time Line Reported, Recupered and Deceased by Department
# > ***Output file***: covid19co_time_line_{key_depto}.csv

# %%
for key_depto in time_line_by_depto:
    # Save dataframe
    time_line_by_depto[key_depto].to_csv(os.path.join(OUTPUT_DIR, 'covid19co_time_line_' + key_depto + '.csv'), index=False)

# %% [markdown]
# ---
# %% [markdown]
# ## Time Line Samples Processed

# %%
# Show dataframe
covid19co_samples_processed.head()


# %%
# Rename columns
covid19co_samples_processed.columns = ['date', 'accum_samples']
# Fill NaN
covid19co_samples_processed['accum_samples'].fillna(0, inplace=True)
# Update column type
covid19co_samples_processed['accum_samples'] = covid19co_samples_processed['accum_samples'].astype('int64')
# Show dataframe
covid19co_samples_processed.head()


# %%
# Time Line [date, accum]
covid19co_samples_time_line = pd.DataFrame(columns=['date', 'accum'])
covid19co_samples_time_line['date'] = [dti.strftime('%d/%m/%Y') for dti in pd.date_range(start='2020-03-01', end=datetime.date.today().isoformat(), freq='D')]
# Get Accumulative Samples
def get_accum(date_sample):
    accum = covid19co_samples_processed[covid19co_samples_processed['date'] == date_sample]['accum_samples'].values
    return accum[0] if len(accum) > 0 else 0
# Update accum
covid19co_samples_time_line['accum'] = covid19co_samples_time_line['date'].transform(lambda value: get_accum(value))
# Add samples without date
#covid19co_samples_time_line.iloc[2] = list(covid19co_samples_processed.iloc[0])
# Show dataframe
covid19co_samples_time_line.head()

# %% [markdown]
# ## Time Line Samples Processed
# > ***Output file***: covid19co_samples_time_line.csv

# %%
# Save dataframe
covid19co_samples_time_line.to_csv(os.path.join(OUTPUT_DIR, 'covid19co_samples_time_line.csv'), index=False)

# %% [markdown]
# ---

# %%


