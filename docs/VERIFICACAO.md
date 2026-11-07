# Verificação da versão organizada

Esta página distingue o que foi verificado localmente da execução integral do produto. O histórico original da entrega é preservado; os registros atuais não substituem os documentos e resultados de outubro.

## Verificações executadas em 7 de novembro de 2026

| Verificação | Resultado | Registro |
|---|---|---|
| Integração e contrato da API | 6 aprovados, 0 falhas, 0 erros e 0 não executados | `qa/resultados.xml`, `qa/evidencias/` e `qa/ambiente.json` |
| Frontend | TypeScript e build Vite concluídos | `results/preparation_checks.json` e `frontend/package-lock.json` |
| Modelo salvo e validação | Acurácia 69,23%, F1 macro 66,71% e recall macro 66,39% | `results/validation_metrics.json` |
| Planilha e matrizes | 13.303 pares; contagens e hashes registrados | `docs/data_manifest.json` |

## API

O TestClient executa a aplicação FastAPI em memória. Endpoint, validação, orquestração, parser XML, agrupamento e respostas de erro utilizam o código do backend. Chamadas HTTP externas, NLP, tradução e classificador são substituídos por dados e objetos de teste.

Os seis casos cobrem consulta com três grupos e fontes, entrada vazia, entrada numérica, conversor sem claim, busca sem evidências e timeout do PubMed. O último caso verifica a conversão de uma falha externa em HTTP 502.

O teste do conversor sem claim verifica a reação da API a esse retorno simulado, não a capacidade linguística do modelo real. Os rótulos dos artigos sintéticos não são previsões do MLP.

O executor emitiu um aviso de depreciação de dependência do Starlette/anyio. Os seis casos terminaram aprovados. Não houve falha de aplicação nesse escopo.

## Frontend

A primeira compilação identificou a ausência dos tipos do Node usados por `process.env` na configuração do Vite. Foram incluídos `@types/node` e o tipo `node` no TypeScript. A compilação e o build passaram depois do ajuste.

O ambiente local utilizou Node 24.22.1. O Dockerfile e o workflow estão configurados para Node 22. O build verifica compilação e geração dos arquivos; não representa teste de navegação ou uso ponta a ponta.

## Modelo

Foi carregado o arquivo MLP entregue, com scikit-learn 1.9.1, e realizada a previsão dos 1.797 exemplos da matriz de validação salva. Os valores arredondados coincidem com os slides da entrega. O registro JSON contém os hashes e as versões efetivas das bibliotecas.

Não houve novo treino, geração de embeddings, nova seleção de modelo ou avaliação do conjunto de teste. Os números não medem a qualidade da busca ou da tradução em uso real.

## Execuções fora do escopo

Nesta organização não foram executados Docker Compose completo, consulta ao NCBI com todos os modelos reais, avaliação de carga, avaliação por tema médico ou teste de interface no navegador.

O workflow do GitHub Actions foi preparado e sua estrutura foi conferida localmente. Sua execução remota dependerá do envio ao repositório da equipe; não há declaração de CI remota aprovada nesta preparação.
