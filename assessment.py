import requests
import os

# Configurações iniciais
GITLAB_API_URL = "https://gitlab.com/api/v4"
PRIVATE_TOKEN = os.getenv("GITLAB_TOKEN")
if not PRIVATE_TOKEN:
    raise ValueError("A variável de ambiente GITLAB_TOKEN não está definida.")
HEADERS = {"Private-Token": PRIVATE_TOKEN}

# Função para listar projetos privados
def get_private_projects():
    projects = []
    page = 1
    while True:
        url = f"{GITLAB_API_URL}/projects?membership=true&visibility=private&page={page}&per_page=100"
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            if not data:  # Se não houver mais projetos, encerrar a busca.
                break
            projects.extend(data)
            page += 1
        else:
            print(f"Erro ao listar projetos: {response.status_code}")
            break
    return projects

# Função para verificar variáveis do projeto
def check_project_variables(project_id):
    url = f"{GITLAB_API_URL}/projects/{project_id}/variables"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        variables = response.json()
        unprotected = [var for var in variables if not var.get("protected", False)]
        return unprotected
    else:
        print(f"Erro ao verificar variáveis no projeto {project_id}: {response.status_code}")
        return []

# Função para listar runners do projeto
def check_runners(project_id):
    url = f"{GITLAB_API_URL}/projects/{project_id}/runners"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        runners = response.json()
        shared_runners = [runner for runner in runners if runner.get("is_shared", False)]
        return shared_runners
    else:
        print(f"Erro ao verificar runners no projeto {project_id}: {response.status_code}")
        return []

# Função principal de assessment
def perform_assessment(project_id=None):
    if project_id:
        # Analisar apenas o projeto especificado
        projects = [project for project in get_private_projects() if str(project["id"]) == project_id]
    else:
        # Analisar todos os projetos privados
        projects = get_private_projects()
    
    if not projects:
        print("Nenhum projeto privado encontrado ou ID inválido.")
        return
    
    for project in projects:
        project_id = project["id"]
        project_name = project["name"]
        print(f"\nAnalisando projeto: {project_name}")
        
        # Verificar variáveis
        unprotected_variables = check_project_variables(project_id)
        if unprotected_variables:
            print(f"  ⚠️ Variáveis não protegidas encontradas: {len(unprotected_variables)}")
            for var in unprotected_variables:
                print(f"    - Nome: {var['key']}")
        else:
            print("  ✅ Todas as variáveis estão protegidas.")
        
        # Verificar runners
        shared_runners = check_runners(project_id)
        if shared_runners:
            print(f"  ⚠️ Runners compartilhados encontrados: {len(shared_runners)}")
        else:
            print("  ✅ Não há runners compartilhados.")

# Execução do script com parâmetros opcionais
if __name__ == "__main__":
    print("Bem-vindo ao script de análise de segurança de pipelines!")
    user_input = input("Digite o ID do repositório que deseja analisar ou pressione Enter para todos os projetos privados: ").strip()
    perform_assessment(project_id=user_input if user_input else None)
