import requests
import json
import time
import os

def fetch_lotofacil_history():
    output_filename = 'lotofacil.json'
    complete_history = []
    start_draw = 1
    base_url = "https://loteriascaixa-api.herokuapp.com/api/lotofacil/"

    if os.path.exists(output_filename):
        try:
            with open(output_filename, 'r', encoding='utf-8') as f:
                complete_history = json.load(f)
                if complete_history:
                    last_saved = max(item.get('draw_number', 0) for item in complete_history)
                    start_draw = last_saved + 1
                    print(f"Arquivo existente encontrado. Último concurso: {last_saved}. Iniciando em: {start_draw}")
        except Exception as e:
            print(f"Erro ao ler arquivo existente: {e}")

    try:
        latest_response = requests.get(base_url, timeout=15)
        if latest_response.status_code == 200:
            data_list = latest_response.json()
            latest_draw = data_list[0].get("concurso")
            end_draw = latest_draw
        else:
            print("Não foi possível determinar o último concurso.")
            return
    except Exception as e:
        print(f"Erro de conexão: {e}")
        return

    if start_draw > end_draw:
        print("O histórico da Lotofácil já está atualizado.")
        return

    print(f"Atualizando do concurso {start_draw} ao {end_draw}")
    print("-" * 75)

    for draw_number in range(start_draw, end_draw + 1):
        try:
            response = requests.get(f"{base_url}{draw_number}", timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                awards = data.get("premiacoes", [])

                prizes = {p.get("faixa"): p for p in awards}
            
                item = {
                    "draw_number": data.get("concurso"),
                    "draw_date": data.get("data"),
                    "numbers": data.get("dezenas"),
                    "winners_15_numbers": prizes.get(1, {}).get("ganhadores", 0),
                    "winners_14_numbers": prizes.get(2, {}).get("ganhadores", 0),
                    "winners_13_numbers": prizes.get(3, {}).get("ganhadores", 0),
                    "winners_12_numbers": prizes.get(4, {}).get("ganhadores", 0),
                    "winners_11_numbers": prizes.get(5, {}).get("ganhadores", 0),
                    "prize_value_15_numbers": prizes.get(1, {}).get("valorPremio", 0.0),
                    "prize_value_14_numbers": prizes.get(2, {}).get("valorPremio", 0.0),
                    "prize_value_13_numbers": prizes.get(3, {}).get("valorPremio", 0.0),
                    "prize_value_12_numbers": prizes.get(4, {}).get("valorPremio", 0.0),
                    "prize_value_11_numbers": prizes.get(5, {}).get("valorPremio", 0.0),
                    "is_accumulated": data.get("acumulou", False),
                    "accumulated_prize": data.get("valorAcumuladoProximoConcurso", 0.0),
                    "estimated_next_prize": data.get("valorEstimadoProximoConcurso", 0.0)
                }
                
                complete_history.append(item)
                
                with open(output_filename, 'w', encoding='utf-8') as f:
                    json.dump(complete_history, f, ensure_ascii=False, indent=4)
                
                print(f"Concurso [{item['draw_number']}] salvo.")

            elif response.status_code == 429:
                print("Limite de requisições atingido. Aguardando 30 segundos...")
                time.sleep(30)
            
            time.sleep(0.1)

        except Exception as e:
            print(f"Falha no concurso {draw_number}: {e}")
            continue

    print("-" * 75)
    print(f"Atualização completa! Total de registros: {len(complete_history)}")

if __name__ == "__main__":
    fetch_lotofacil_history()