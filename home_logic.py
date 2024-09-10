# home_logic.py

# Variável para contar o número de links gerados


def get_home_data():
    message = "Bem-vindo à sua página inicial!"
    tasks = ["Tarefa 1", "Tarefa 2", "Tarefa 3"]
    restaurants = ["Restaurante A", "Restaurante B", "Restaurante C"]

    # Verifica se o link ainda pode ser gerado
    link_available = link_counter < MAX_LINKS

    return {
        'message': message,
        'tasks': tasks,
        'restaurants': restaurants,
        'link_available': link_available
    }


