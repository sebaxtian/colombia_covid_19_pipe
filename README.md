# Colombia Covid 19 Pipeline
Pipeline to get dataset from [Instituto Nacional de Salud](https://www.ins.gov.co/Noticias/Paginas/Coronavirus.aspx) daily report Coronavirus Covid 19 of Colombia.

You can get the official dataset here: [INS - Official Report](https://e.infogram.com/api/live/flex/bc384047-e71c-47d9-b606-1eb6a29962e3/664bc407-2569-4ab8-b7fb-9deb668ddb7a)

The number of new cases are increasing day by day around the world. This dataset has information about reported cases from 32 Colombia departments.

You can get the datasets from [colombia_covid_19_pipe](https://www.kaggle.com/sebaxtian/colombia-covid-19-pipe) Kaggle Notebook Kernel.

---

## Requirements

See [requirements.txt](./requirements.txt) file.

## Source Code

See [./src](./src) directory.

## Datasets

See [./output](./output) directory.

## Documentation

| Directory | Readme    |
|-----------|-----------|
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

***That's all for now ...***

---

#### Would you like contribute?

> Getting in touch with [@sebaxtianbach](https://twitter.com/sebaxtianbach)

---

#### License

[MIT License](./LICENSE)

#### About me

[https://about.me/sebaxtian](https://about.me/sebaxtian)
