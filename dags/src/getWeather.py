import json
import os
from datetime import datetime
from pathlib import Path

import requests
from dotenv import (
    dotenv_values,
    load_dotenv,
)


def get_weather():
    """
    Query Taiwan CWB API and to get the weather for
    嘉義縣 and then dump the json to the /src/data/ directory
    with the file name "{todays_date}.json"
    """

    # My API key is defined in .env or .env.secret file(s)
    load_dotenv()
    config = os.environ
    #config = {
    #    **dotenv_values(".env.shared"),
    #    **dotenv_values(".env.secret"),
    #}
    paramaters = {
        "Authorization": config["CWB_API_KEY"],
        "format": "json",
    }

    general_url = (
        f'{config["CWB_RESTFUL_API_URL"]}/'
        f'{config["GENERAL_WEATHER_36_HOUR_DATAID"]}?'
        #f'{config["CHANGHUA_WEATHER_2_DAY_DATAID"]}?'
    )
    result = requests.get(general_url, paramaters)

    if result.status_code == 200 :
        json_data = result.json()
        file_name  = str(datetime.now().date()) + '.json'
        tot_name   = Path(__file__).parent/f'data/{file_name}'

        with open(tot_name, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False)
    else :
        print(result.text)


if __name__ == "__main__":
    get_weather()
