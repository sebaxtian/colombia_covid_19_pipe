![Schedule master](https://github.com/sebaxtian/colombia_covid_19_pipe/workflows/Schedule%20master/badge.svg?branch=master&event=schedule)
![Build and merge dev into master](https://github.com/sebaxtian/colombia_covid_19_pipe/workflows/Build%20and%20merge%20dev%20into%20master/badge.svg?branch=dev&event=push)
![GitHub](https://img.shields.io/github/license/sebaxtian/colombia_covid_19_pipe?style=plastic)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/sebaxtian/colombia_covid_19_pipe?style=plastic)
![GitHub contributors](https://img.shields.io/github/contributors/sebaxtian/colombia_covid_19_pipe?style=plastic)
![GitHub last commit](https://img.shields.io/github/last-commit/sebaxtian/colombia_covid_19_pipe?color=09ca8c&style=plastic)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/sebaxtian/colombia_covid_19_pipe?style=plastic)

# Colombia Covid 19 Pipeline

Dataset is obtained from [Instituto Nacional de Salud](https://www.ins.gov.co/Noticias/Paginas/Coronavirus.aspx) daily report Coronavirus 2019 from Colombia.

You can get the official dataset here: [INS - Official Report](https://www.datos.gov.co/Salud-y-Protecci-n-Social/Casos-positivos-de-COVID-19-en-Colombia/gt2j-8ykr)

The number of new cases are increasing day by day around the world.
This dataset has information about reported cases from 32 Colombia departments.

You can get the Google COVID-19 Community Mobility Reports - Colombia.

You can view and collaborate to the analysis here:
[colombia_covid_19_analysis](https://www.kaggle.com/sebaxtian/colombia-covid-19-analysis) Kaggle Notebook Kernel.

---

[![Colombia Covid19 Time Line](./chart/covid19_time_line.png "Colombia Covid19 Time Line")](https://www.datawrapper.de/_/b9YVt/)

---

## Requirements

- **Python 3**:
  - See [requirements.txt](./requirements.txt) file.

## Source Code

See [./src](./src) directory.

## Datasets

See [./output](./output) directory.

## Documentation

| Directory | Readme    |
|-----------|-----------|
| ./chart   | [README.md](./chart/README.md) |
| ./doc     | [README.md](./doc/README.md) |
| ./input   | [README.md](./input/README.md) |
| ./output  | [README.md](./output/README.md) |
| ./src     | [README.md](./src/README.md) |

### How to use

Please read and execute each step below:

#### Step 1

Create and use Python virtual environment:

```bash
$promt> python3 -m venv .venv
$promt> source .venv/bin/activate
```

#### Step 2

Install all Python requirements:

```bash
$promt> pip3 install -r requirements.txt
```

#### Step 3

Run Pipeline script:

```bash
$promt> ./run.sh
```

The Pipeline output is generated within [./output](./output) directory.

#### Step N

> Work in progress ...

---

#### Jupyter Nootebook to Python Script

```bash
$promt> jupyter nbconvert --to script ./src/colombia-covid-19-pi
pe.ipynb --output colombia_covid_19_pipe
```

---

***That's all for now ...***

---

#### Would you like contribute?

> Getting in touch with [@sebaxtianbach](https://twitter.com/sebaxtianbach)

---

#### License

[MIT License](./LICENSE)

#### About me

[https://about.me/sebaxtian](https://about.me/sebaxtian)
