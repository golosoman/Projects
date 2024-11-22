from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from prefect.blocks.system import Secret
from prefect.variables import Variable

import httpx
import sys

def upload(developer):
    upload_token = Secret.load("upload-basic-token")

    print("Upload started")
    start = datetime.now()

    response = httpx.post(
        Variable.get("parsing_upload_url"),
        headers={ 'Authorization': 'Basic ' + upload_token.get() },
        json={ 'developer': developer },
        timeout=60 * 15
    )

    print(f"Upload completed in {datetime.now() - start}")

    if not response.is_success:
        print(f"Fail response status code: {response.status_code}", file=sys.stderr)
        print(response.json(), file=sys.stderr)
        response.raise_for_status()

def create_date_from_quarter(year, quarter):
    if not isinstance(year, int):
        raise ValueError(f"Year type {type(year)} must be an integer")

    if not isinstance(quarter, int):
        raise ValueError(f"Quarter type '{type(quarter)}' must be an integer")

    if quarter < 1 or quarter > 4:
        raise ValueError(f"Invalid quarter {quarter}")

    if year < 1950 or year > 2100:
        raise ValueError(f"Invalid year {year}")

    return date(year, quarter * 3, 1) + relativedelta(months=1)

def transform_roman_to_arabic(roman):
    if roman == 'I':
        return 1

    if roman == 'II':
        return 2

    if roman == 'III':
        return 3

    if roman == 'IV':
        return 4

    raise ValueError(f"Invalid roman: {roman}")
