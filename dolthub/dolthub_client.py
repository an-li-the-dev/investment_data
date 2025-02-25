import os

import fire

import requests

session = requests.Session()
session.headers["Authorization"] = f'token {os.environ["DOLTHUB_TOKEN"]}'
token = os.environ["DOLTHUB_TOKEN"]


def get_index_last_update_date(user="kidylee", database="investment_data", branch="master") -> {str: str}:
    query = 'SELECT index_code, MAX(trade_date) AS last_update_date FROM ts_index_weight GROUP BY index_code;'
    url = f'https://www.dolthub.com/api/v1alpha1/{user}/{database}/{branch}'

    resp = session.get(url, params={"q": query})
    resp.raise_for_status()
    result = resp.json()
    return {row["index_code"]: row["last_update_date"] for row in result["rows"]}

def create_remote_branch(owner: str, database: str, branch: str, new_branch: str):
    response = session.post(
        f"https://www.dolthub.com/api/v1alpha1/{owner}/{database}/branches",
        json={"revisionType":"branch","revisionName":branch,"newBranchName":new_branch}
    )
    data = response.json()
    if response.status_code == 200:
        return data
    if response.status_code == 400 and data["message"] == 'already exists':
        return data

    print(data)
    response.raise_for_status()

    return data

if __name__ == '__main__':
    fire.Fire()