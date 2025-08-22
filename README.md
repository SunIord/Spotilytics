# Spotilytics
**Spotilytics** é uma aplicação web interativa feita com Streamlit que consome dados da API do Spotify para apresentar visualizações e insights sobre músicas, artistas ou playlists.

## Como rodar o projeto
Siga os passos abaixo para rodar a aplicação localmente:

### 1. Clone o repositório
```bash
git clone https://github.com/SunIord/Spotilytics
cd Spotilytics
```

### 2. Crie um ambiente virtual
```bash
python -m venv .venv
```

### 3. Ative o ambiente
#### Windows (cmd):
```bash
.venv\Scripts\activate
```
#### PowerShell:
```bash
.\.venv\Scripts\Activate.ps1
```
#### Linux/macOS:
```bash
source .venv/bin/activate
```

### 4. Instale as dependências
```bash
pip install -r requirements.txt
```

### 5. Configure as variáveis de ambiente
#### Crie um arquivo `.env` na pasta do projeto e adicione suas credenciais da API do Spotify:
```ini
spotipyId=SEU_CLIENT_ID
spotipySecret=SEU_CLIENT_SECRET
``` 
#### Você pode obter essas credenciais em: https://developer.spotify.com

### 6. Execução
```bash
streamlit run app.py
```
