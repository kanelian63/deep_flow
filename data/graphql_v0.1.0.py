import os
import json
import pathlib
from datetime import datetime
import numpy as np
import requests

def get_certified(token_dir: str) -> str:

    try:
        os.chdir("./data")
    except:
        pass

    with open(token_dir, "r") as file:
        token = file.readlines()[0]

    return token



datetimes = []

repo = "MariaDB/server"
owner, name = repo.split("/")
progress_task=(None, None)
selection = "last: 100"
starred = []
while True:
    query = f"""
    {{
      repository(owner:"{owner}", name:"{name}") {{
        stargazers({selection}) {{
          pageInfo {{
            hasPreviousPage
            startCursor
          }}
          edges {{
            starredAt
          }}
          totalCount
        }}
      }}
    }}
    """

    res = requests.post(
        "https://api.github.com/graphql",
        json={"query": query},
        headers={"Authorization": f"token {token}"},
    )
    data = res.json()["data"]["repository"]["stargazers"]
    print(data)
    part_starred = data['edges']
    starred.extend(part_starred)
    total_starred = data['totalCount']
    cursor = data["pageInfo"]["startCursor"]
    selection = f'last: 100, before: "{cursor}"'
    if not data["pageInfo"]["hasPreviousPage"]:
        print('total star :', total_starred)
        print('part_starred :', len(starred))
        break


if __name__=="__main__":
    token = get_certified("./github_authentication.txt")

    print(__name__)