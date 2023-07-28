import requests
import datetime

from pandas import DataFrame
from click import command
from click import option
from time import sleep
from github import Github
from github.GithubException import RateLimitExceededException
from tqdm import tqdm

def seach_gh_code(token: str, keyword: str) -> list:
    print('Searching GitHub using keyword: {}'.format(keyword))

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": "Token " + token
    }

    # Set up the query
    base_url = "https://api.github.com"
    search_endpoint = "/search/code?q=" + keyword + "+in:file"

    response = requests.request("GET", base_url + search_endpoint, headers=headers)
    if response.status_code == 200:
        results = response.json()
    else:
        print(f"Error occurred. Status Code: {response.status_code}")
        return None

    # Print results
    results_count = len(results["items"])
    print(f'Found {results_count} of available code(s)')
    results_list = []
    for item in tqdm(results["items"]):
        try:
            owner = item["repository"]["owner"]["login"]
            repo = item["repository"]["name"]
            repo_endpoint = f"/repos/{owner}/{repo}"
            resp = requests.get(base_url + repo_endpoint, headers=headers)
            if resp.status_code == 200:
                repo_info = resp.json()
                creation_date = repo_info["created_at"]
                push_date = repo_info["pushed_at"]
            else:
                print(f"Error occurred. Status Code: {response.status_code}")
                return None
            
            results_list.append([item["name"], creation_date, push_date, item["html_url"], item["repository"]["description"]])
            sleep(2)
        except requests.exceptions.RetryError:
            sleep(60)
            results_list.append([item["name"], creation_date, push_date, item["html_url"], item["repository"]["description"]])

    return results_list


def search_gh_descp(auth: Github, keyword: list) -> list:
    print('Searching GitHub using keyword: {}'.format(keyword))

    query = keyword + '+in:readme+in:description'
    results = auth.search_repositories(query, 'stars', 'desc')

    # print results
    print(f'Found {results.totalCount} repo(s)')

    results_list = []
    for repo in tqdm(range(0, results.totalCount)):
        try:
            results_list.append([results[repo].name, results[repo].created_at, results[repo].pushed_at, results[repo].clone_url, results[repo].description])
            sleep(1)
        except RateLimitExceededException:
            sleep(60)
            results_list.append([results[repo].name, results[repo].created_at, results[repo].pushed_at, results[repo].clone_url, results[repo].description])

    return results_list


@command()
@option('--token', prompt='Please enter your GitHub Access Token')
@option('--keywords', prompt='Please enter the keywords separated by a comma')
@option('--filename', prompt='Please provide the file path')

def main(token: str, keywords: str, filename: str) -> None:

    # initialize and authenticate GitHub API
    auth = Github(token)

    # search a list of keywords
    search_list = [keyword.strip() for keyword in keywords.split(',')]

    # search repositories on GitHub
    github_results = dict()
    for key in search_list:
        github_results[key] = []
        github_results[key] += search_gh_descp(auth, key)
        github_results[key] += seach_gh_code(token, key)
        print("\n\n\n")
        if len(search_list) > 1: sleep(5)

    # write out results
    timestamp = datetime.datetime.now()
    formatted_date = timestamp.strftime('%d') + timestamp.strftime('%b') + timestamp.strftime('%Y')
    full_filename = filename.strip() + 'GitHub_Search_Results_' + formatted_date + '.csv'

    i = 1
    sno = []
    names = []
    c_date = []
    p_date = []
    url = []
    description = []

    print('Writing search results to: {}'.format(full_filename))
    for key in tqdm(github_results.keys()):
        for res in github_results[key]:
            sno.append(i)
            i += 1
            names.append(res[0])
            c_date.append(res[1])
            p_date.append(res[2])
            url.append(res[3])
            description.append(res[4])
    
    tem = list(zip(sno,names,c_date,p_date,url,description))
    df = DataFrame(data=tem, columns=["S.No","Name","Date Created","Date of last push", "URL","Description"])
    df.to_csv(full_filename, index=False)
    sleep(5)


if __name__ == '__main__':
    main()
