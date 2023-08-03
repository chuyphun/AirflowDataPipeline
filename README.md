# Origin
This repo is an adaptation from
[this blog post](http://michael-harmon.com/blog/AirflowETL.html).

The major changes are
1. Instead of OpenWeatherMap API, we have chosen Taiwan's Central Weather
   Bureau's (abbr. CWB) API because in this case we do not need to register
   credit card information in order to use the API.
   For more info on CWB, cf.
    - <https://opendata.cwb.gov.tw/devManual/insrtuction>
    - <https://opendata.cwb.gov.tw/dist/opendata-swagger.html>
1. Python3 and `airflow==2.6.3`


## How to Use This Repo?
### Installation
1. Create a new virtual environment (or use an existing one). Activate it.
    - If you use Miniconda, you can create and activate
      one such virtual env by
      ```shell
      $ conda create --name airflow_practice python=3.10
      $ conda activate airflow_practice
      ```
      The Python version could be anything from 3.7 to 3.11
1. Install Airflow by copying and pasting the commands below into a terminal
   ```shell
   AIRFLOW_VERSION=2.6.3
   PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
   CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
   pip install "apache-airflow[postgres]==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
   ```
1. Install the remaining packages by
   ```shell
   (airflow_practice) $ pip install -r requirements.txt
   ```


