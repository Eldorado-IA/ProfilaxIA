# Testes da API do ProfilaxIA

Suíte de seis testes de integração e contrato para a API do MVP do First Challenge.

## Versão de referência

- Repositório: https://github.com/Eldorado-IA/ProfilaxIA
- Implementação da API utilizada como referência: commit [`c3e3b63`](https://github.com/Eldorado-IA/ProfilaxIA/commit/c3e3b63fdc61a2934da6729cfe7730eb375ed97a).

Os testes exercitam essa implementação do backend. O histórico e a procedência do código estão em [Créditos e referências](CREDITOS.md).

## Escopo

O `TestClient` executa a aplicação FastAPI em memória. São exercitados o endpoint,
validação da entrada, orquestração, busca com respostas controladas, extração de XML,
agrupamento de evidências, esquema de resposta e tratamento de erros.

O NLP, a tradução, o classificador e as chamadas HTTP do NCBI são substituídos por
objetos e respostas de teste. Os artigos e os rótulos são sintéticos. Nenhuma
consulta médica real é feita. Esta suíte não mede F1, não valida tradução ou
inferência real e não testa a interface web no navegador.

## Casos

| ID | Cenário | HTTP esperado |
|---|---|---|
| CT01 | Consulta com três evidências sintéticas e rastreabilidade | 200 |
| CT02 | Entrada vazia | 422 |
| CT03 | Entrada apenas numérica | 422 |
| CT04 | Conversor simulado não gera uma claim | 422 |
| CT05 | Busca simulada sem evidências | 404 |
| CT06 | Timeout simulado do PubMed | 502 |

## Como executar no Windows

1. Clone o repositório, que inclui a suíte e suas dependências.
2. Abra o terminal na raiz. Utilize Python 3.12.

```powershell
python -m venv .venv-qa
.\.venv-qa\Scripts\python.exe -m pip install -r requirements-test-lock.txt
.\.venv-qa\Scripts\python.exe -m pytest -v --junitxml=qa/resultados.xml
```

Não é necessário ativar o ambiente virtual. As dependências de QA permitem rodar
esses seis casos sem baixar os modelos de linguagem ou iniciar o Docker.

No Linux/macOS, use `.venv-qa/bin/python` nas duas últimas linhas.

## Evidências

- `qa/resultados.xml`: resultado JUnit emitido pelo pytest.
- `qa/evidencias/CT01.json` a `CT06.json`: requisição, resposta e chamadas simuladas.
- `qa/relatorio.md`: resumo da execução registrada.
- `qa/ambiente.json`: data, versão do código e versões das dependências usadas.

Uma nova execução regrava o XML e os JSONs por caso. O resumo e o registro de
ambiente anexos referem-se à execução documentada; atualize-os ao publicar uma
execução diferente. O resultado da suíte deve ser citado com o escopo acima.

Os registros atuais de `qa/` correspondem à execução local de 7 de novembro de
2026: seis testes aprovados. Os registros recebidos do pacote de outubro foram
preservados em `docs/registros/api_2026-10-13/`. Consulte também
[Verificação técnica](docs/VERIFICACAO.md). A suíte também foi aprovada no
[GitHub Actions](https://github.com/Eldorado-IA/ProfilaxIA/actions/runs/42431631345).
