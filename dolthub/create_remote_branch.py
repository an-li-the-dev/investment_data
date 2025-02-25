import requests

response = requests.post(
    "https://www.dolthub.com/api/v1alpha1/{owner}/{database}/branches",
    headers={"authorization":"YOUR_API_KEY","Content-Type":"application/json"},
    data={"revisionType":"branch","revisionName":"main","newBranchName":"feature-branch"}
)

data = response.json()

def create_remote_branch(owner: str, database: str, branch: str, new_branch: str):
    response = requests.post(
        f"https://www.dolthub.com/api/v1alpha1/{owner}/{database}/branches",
        headers={"authorization":"YOUR_API_KEY","Content-Type":"application/json"},
        data={"revisionType":"branch","revisionName":branch,"newBranchName":new_branch}
    )
    response.raise_for_status()
    data = response.json()
    return data