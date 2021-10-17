import os
import json
import pathlib
from datetime import datetime
import numpy as np
import requests

try:
    os.chdir("./data")
except:
    pass

def get_github_token(token_dir: str) -> str:

    with open(token_dir, "r") as file:
        github_token = file.readlines()[0]

    return github_token


def get_repo_groups(repos_txt_dir):

    with open(repos_txt_dir, 'r') as file:
        repos_groups = json.load(file)

    return repos_groups


def get_starred(owner, name):

    selection = "last: 100"
    datetimes = []
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
            print(owner, name)
            print('total star :', total_starred)
            print('part_starred :', len(starred))
            break

    return starred


if __name__=="__main__":

    print(__name__)
    # get github token
    token_txt_dir = './github_authentication.txt'
    token = get_github_token(token_txt_dir)
    # get repo groups
    repos_txt_dir = './repo_groups.json'
    repo_groups = get_repo_groups(repos_txt_dir)
    len(repo_groups)

    for repos_idx, repos_group in enumerate(repo_groups):
        print(repos_idx, repo_groups[repos_group])

        for repo_idx, repo_info in enumerate(repo_groups[repos_group]):
            owner, repo = repo_info.split("/")
            print(repo_idx, owner, repo)
            starred = get_starred(owner, repo)

