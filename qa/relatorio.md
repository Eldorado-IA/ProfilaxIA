# Verificação local da API

Execução em 07/11/2026 às 19:32:28 (America/Sao_Paulo).

Seis testes aprovados, zero falhas, zero erros e zero casos não executados.

| Caso | Cenário | HTTP | Resultado |
|---|---|---|---|
| CT01 | Consulta e fontes | 200 | PASS |
| CT02 | Entrada vazia | 422 | PASS |
| CT03 | Entrada numérica | 422 | PASS |
| CT04 | Conversor sem claim | 422 | PASS |
| CT05 | Sem evidências | 404 | PASS |
| CT06 | PubMed indisponível | 502 | PASS |

As chamadas externas, o NLP, a tradução e o classificador foram simulados. A API, a validação, a orquestração e o parser XML utilizam o código do projeto. O ambiente e os hashes estão em ambiente.json. Um aviso de depreciação de dependência do Starlette/anyio não interrompeu a execução.
