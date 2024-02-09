import requests

# Substitua 'SUA_CHAVE_DE_API' pela sua chave de API
API_KEY = 'RGAPI-f996c09d-3987-4e3b-aaed-0fa0469d0c3b'

# Região do servidor (por exemplo, 'br1' para o servidor brasileiro)
REGION = 'br1'

# Nome de invocador (seu nome de jogador)
SUMMONER_NAME = 'teteco25'

# URL base da API da Riot Games
BASE_URL = f'https://{REGION}.api.riotgames.com/lol'

# Função para obter o ID do invocador
def obter_id_invocador():
    summoner_url = f'https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{SUMMONER_NAME}'
    headers = {'X-Riot-Token': API_KEY}

    response = requests.get(summoner_url, headers=headers)

    if response.status_code == 200:
        match_history_data = response.json()
        return match_history_data
    else:
        print(f'Erro ao obter ID do invocador. Código de status: {response.status_code}')
        return None

# Função para obter o histórico de partidas
def obter_historico_partidas():
    account_id = obter_id_invocador()
    if account_id:
        match_history_url = f'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{account_id['puuid']}/ids?start=0&count=20'
        headers = {'X-Riot-Token': API_KEY}

        response = requests.get(match_history_url, headers=headers)

        if response.status_code == 200:
            match_history_data = response.json()
            return match_history_data
        else:
            print(f'Erro ao obter histórico de partidas. Código de status: {response.status_code}')
            return None


# Função para obter o histórico de partidas
def get_partidaById(idPartida):
    if idPartida:
        match_history_url = f'https://americas.api.riotgames.com/lol/match/v5/matches/{idPartida}'
        headers = {'X-Riot-Token': API_KEY}

        response = requests.get(match_history_url, headers=headers)

        if response.status_code == 200:
            match_history_data = response.json()
            return match_history_data['info']
        else:
            print(f'Erro ao obter histórico de partidas. Código de status: {response.status_code}')
            return None


if __name__ == '__main__':
    historico_partidas = obter_historico_partidas()
    if historico_partidas:
        print("Histórico de Partidas:")
        for partida in historico_partidas:
            dataPartida = get_partidaById(partida)
            print(f"ID da Partida: {dataPartida['gameId']}")
            print(f"Tipo de Jogo: {dataPartida['gameMode']} - {dataPartida['gameType']}")
            for times in dataPartida['teams']:
                corTime = "Azul" if times['teamId'] == 100 else "Vermelho"
                resultado = "Venceu" if times['win'] else "Perdeu"
                contadorObjetivos = times['objectives']
                print(f"Time {corTime} - Resultado: {resultado} - Totais de Obaajetivos: Dragão:{contadorObjetivos['dragon']['kills']} Campeões:{contadorObjetivos['champion']['kills']} Barão:{contadorObjetivos['baron']['kills']} Torres:{contadorObjetivos['tower']['kills']} Arauto:{contadorObjetivos['riftHerald']['kills']}")
                #print(f"ID do Campeão: {dataPartida['champion']}")
                #print(f"Data da Partida: {dataPartida['timestamp']}")
            print("---")
    else:
        print("Nenhum histórico de partidas encontrado.")

