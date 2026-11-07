# Como executar e reproduzir

## Aplicação web

Requer Git, Git LFS e Docker com Compose. Os Dockerfiles usam Python 3.12 no backend e Node 22 no frontend. A primeira inicialização pode baixar modelos do Hugging Face.

Na raiz:

```bash
git lfs install
git lfs pull
```

Copie `.env.example` para `.env`: no PowerShell, `Copy-Item .env.example .env`; no Linux/macOS, `cp .env.example .env`. Ajuste a configuração do NCBI. A chave é opcional no backend; o intervalo entre chamadas depende de sua presença. Não versione credenciais.

### Desenvolvimento

```bash
docker compose up --build backend frontend
```

Interface em `http://localhost:5173`, API em `http://localhost:8000` e OpenAPI em `http://localhost:8000/docs`.

### Perfil de produção

```bash
docker compose --profile prod up --build backend-prod frontend-prod
```

Interface em `http://localhost:8080`, com Nginx como servidor e proxy. Os comandos vêm da configuração do projeto. Consulte `VERIFICACAO.md` para o alcance das execuções locais.

## Testes da API

Os seis testes leves dispensam modelos reais, Docker e NCBI. Use Python 3.12 e um ambiente separado:

```powershell
python -m venv .venv-qa
.\.venv-qa\Scripts\python.exe -m pip install -r requirements-test-lock.txt
.\.venv-qa\Scripts\python.exe -m pytest -v --junitxml=qa/resultados.xml
```

No Linux/macOS, use `.venv-qa/bin/python`. `requirements-test.txt` contém dependências diretas; `requirements-test-lock.txt` registra também as transitivas da verificação local. Veja `README_TESTES.md`.

## Build do frontend

Com Node 22 ou versão compatível e npm:

```bash
cd frontend
npm ci
npm run build
```

O lockfile registra as dependências. O build verifica TypeScript e gera `dist/`.

## Métricas salvas

Em um ambiente Python 3.12 separado:

```bash
python -m pip install -r requirements-evaluation-lock.txt
python scripts/evaluate_saved_model.py --output results/validation_metrics.json
```

O script utiliza o MLP salvo, `X_val_emb.npy` e `y_val.npy`. Não baixa embeddings, não retreina e não avalia o teste. Carregue `.pkl` apenas de origem confiável.

## Regeração e treino

```bash
python -m pip install -r requirements.txt
python -m spacy download en_core_web_sm
python src/prep.py
python src/teste_sup.py
python src/sup.py
```

`teste_sup.py` é opcional para comparar classificadores. `prep.py` precede o treino, pois gera as matrizes e os rótulos. Essa sequência exige baixar modelos e mais recursos do que os testes leves.

O relatório desta organização não representa uma nova execução completa do treino ou do conjunto de teste.
