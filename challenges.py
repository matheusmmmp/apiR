import requests
import pandas as pd

# Substitua 'SUA_CHAVE_DE_API' pela sua chave de API
API_KEY = 'RGAPI-f996c09d-3987-4e3b-aaed-0fa0469d0c3b'

# Região do servidor (por exemplo, 'br1' para o servidor brasileiro)
REGION = 'br1'

# Nome de invocador (seu nome de jogador)
SUMMONER_NAME = 'teteco25'

# URL base da API da Riot Games
BASE_URL = f'https://{REGION}.api.riotgames.com/lol'

def filter_data(data):
    filtered_data = []
    for item in data:
        localized_names = item["localizedNames"].get("pt_BR")
        if localized_names:
            item["localizedNames"] = localized_names
            filtered_data.append(item)
    return filtered_data

def getConfigChallenge():
    summoner_url = f'https://{REGION}.api.riotgames.com/lol/challenges/v1/challenges/config'
    headers = {'X-Riot-Token': API_KEY}

    response = requests.get(summoner_url, headers=headers)

    if response.status_code == 200:
        filtered_data = filter_data(response.json())
        return filtered_data
    else:
        print(f'Erro ao obter ID do invocador. Código de status: {response.status_code}')
        return None

def obter_id_invocador():
    summoner_url = f'https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{SUMMONER_NAME}'
    headers = {'X-Riot-Token': API_KEY}

    response = requests.get(summoner_url, headers=headers)

    if response.status_code == 200:
        match_history_data = response.json()
        return match_history_data['puuid']  # Retorna o ID do invocador
    else:
        print(f'Erro ao obter ID do invocador. Código de status: {response.status_code}')
        return None

def getChallengeById(idPartida):
    match_history_url = f'https://{REGION}.api.riotgames.com/lol/challenges/v1/player-data/{idPartida}'
    headers = {'X-Riot-Token': API_KEY}

    response = requests.get(match_history_url, headers=headers)

    if response.status_code == 200:
        player_challenges_data = response.json()
        return player_challenges_data
    else:
        print(f'Erro ao obter histórico de partidas. Código de stasstus: {response.status_code}')
        return None


if __name__ == '__main__':
    # Obter o ID do invocador
    account_id = obter_id_invocador()

    if account_id:
        # Obter os dados dos desafios de configuração
        dfConfig = pd.DataFrame(getConfigChallenge())

        # Obter os dados do desafio do usuário
        dfUserChallenge = getChallengeById(account_id)
        print(dfUserChallenge)
        df = pd.DataFrame(dfUserChallenge['challenges'])

        # Adicionar uma nova coluna com o nome do desafio ao DataFrame do usuário
        #df['challengeName'] = dfConfig.loc[dfConfig['id'] == df['challengeId'], 'localizedNames']['name'].values[0]

        # Iterar sobre os desafios do usuário e imprimir o nome do desafio
        for index, row in df.iterrows():
            print(f"ID: {row['challengeId']}")
            print(f"ID: {row['level']}")
            print("=" * 50)
    else:
        print("Nenhum histórico de partidas encontrado.")
