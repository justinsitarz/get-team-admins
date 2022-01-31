import requests
import json
import pandas as pd

api_key = '' # retrieve key with global access and read permissions from API Key Management
url = "https://api.opsgenie.com/v2/teams/" # set as https://api.eu.opsgenie.com/v2/users/ if account is in the EU region
csv = "./admins.csv"


def get_teams(url, headers):
    teams = []
    res = requests.get(url=url, headers=headers)
    response = json.loads(res.text)
    for r in response['data']:
        if r.get('id') and r.get('name'):
            teams.append([r['name'], r['id']])
    return teams

def get_admins(url, team_id, headers):
    url += team_id
    admins = []
    res = requests.get(url, headers=headers)
    response = json.loads(res.text)
    if response['data'].get('members'):
        for r in response['data'].get('members'):
            if r['role'] == 'admin':
                admins.append(r['user']['username'])
    return ', '.join(admins)


def generate_csv(data):
    df = pd.DataFrame(data)
    df.to_csv(csv, sep=',', encoding='utf-8')

def main():
    global api_key
    global url
    global csv

    if api_key == '':
        api_key = input("API key: ")

    api_headers = {'content-type': 'application/json','Authorization':'GenieKey ' + api_key}
    team_admins = []
    teams = get_teams(url, api_headers)

    for t in teams:
        team_dict = {"Team": t[0], "Admins": get_admins(url, t[1], api_headers)}
        team_admins.append(team_dict)
    print(team_admins)

    generate_csv(team_admins)

if __name__ == '__main__':
    main()