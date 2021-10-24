import os
import json
import pathlib
from datetime import datetime
import numpy as np
import requests
import pandas as pd


pd.options.display.max_rows = 500
pd.options.display.max_columns = 500

try:
    os.chdir("./data")
except:
    pass

def get_github_token(token_dir: str) -> str:
    """aasdfasdfasdf"""
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
            print('sum_starred :', len(starred))
            break

    return starred


def get_starredAt(repo_groups):
    for repos_idx, repos_group in enumerate(repo_groups):
        print(repos_idx, repo_groups[repos_group])

        for repo_idx, repo_info in enumerate(repo_groups[repos_group]):
            owner, repo = repo_info.split("/")
            print(repo_idx, owner, repo)
            starred = get_starred(owner, repo)

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
    # get starredAt
    starred = get_starredAt(repo_groups)


# pandas dataframe resample 함수를 이용하여 월별 혹은 주별 데이터 수 적립
df2 = pd.DataFrame(index=range(0, len(starred)), columns=['starredAt', 'starredSeq'])

for starred_idx, at in enumerate(starred):
    df2.loc[starred_idx, 'starredAt'] = datetime.fromisoformat(at['starredAt'].replace("Z", ""))
    df2.loc[starred_idx, 'starredSeq'] = 1

df_resample = df2.sort_values('starredAt').reset_index(drop=True)
df_resample = df_resample.set_index('starredAt')
df_resample_1W = df_resample.resample(rule='1W').sum()

# 1W 단위로 resmapling한 df에 stacked 컬럼 추가

