# Resultado dos testes da API do ProfilaxIA

Execução: 13/10/2026 às 23:33:46 (America/Sao_Paulo).

Commit: `c3e3b63fdc61a2934da6729cfe7730eb375ed97a`.

**6 aprovados, 0 falhas, 0 erros e 0 não executados.**

Duração registrada pelo pytest: 0.047 s.

| Caso | Cenário | HTTP observado | Resultado |
|---|---|---|---|
| CT01 | Consulta com fontes e três grupos | 200 | PASS |
| CT02 | Entrada vazia | 422 | PASS |
| CT03 | Entrada numérica | 422 | PASS |
| CT04 | Conversor sem claim | 422 | PASS |
| CT05 | Nenhuma evidência | 404 | PASS |
| CT06 | PubMed indisponível | 502 | PASS |

A execução utiliza o código real da API, da validação, da orquestração e do parser XML. As respostas HTTP externas, o NLP, a tradução e o classificador são simulados. Os rótulos não são previsões do MLP real.

O resultado caracteriza apenas os seis cenários executados; não representa cobertura completa, teste do navegador ou nova avaliação médica do modelo.

Aviso de execução: houve uma depreciação de dependência do Starlette TestClient relacionada ao anyio. A execução terminou com código de saída 0.
