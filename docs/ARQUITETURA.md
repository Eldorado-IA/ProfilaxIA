# Arquitetura e contrato da API

## Fluxo da aplicação web

1. O frontend recebe a pergunta e chama a API.
2. O backend normaliza e valida a entrada.
3. MarianMT traduz para inglês; spaCy reorganiza a pergunta em uma alegação.
4. YAKE extrai palavras-chave. A busca consulta o PubMed com AND e remove termos por fallback quando necessário.
5. O ESummary fornece metadados e PMCIDs. O EFetch do PMC retorna XML JATS.
6. O buscador procura o primeiro parágrafo de uma conclusão no corpo ou no resumo estruturado, limitado a 900 caracteres.
7. O filtro lexical exige pelo menos uma palavra-chave na evidência.
8. O classificador codifica a alegação e os primeiros 350 caracteres da evidência, combina os vetores e aplica o MLP salvo.
9. A API devolve evidências agrupadas, metadados e links dos artigos.

`src/app.py` e `src/buscador.py` preservam o caminho de terminal anterior à separação do backend web. A API utiliza `backend/app/services`.

## Endpoints

| Método | Caminho | Finalidade |
|---|---|---|
| GET | `/api/v1/health` | Estado básico da API |
| GET | `/api/v1/exemplos` | Perguntas de exemplo |
| POST | `/api/v1/verificacoes` | Verificação de uma pergunta |

Entrada do POST:

```json
{"pergunta": "As máscaras reduzem a transmissão de COVID-19?"}
```

A resposta inclui `pergunta`, `pergunta_traduzida`, `claim`, `total` e `evidencias`. O último campo contém `refutam`, `suportam` e `neutras`. Cada item inclui `pmid`, `pmcid`, `titulo`, `autores`, `ano`, `fonte`, `link` e `trecho`.

## Erros

| HTTP | Tipo exemplificado | Situação |
|---|---|---|
| 422 | `vazia`, `sem_letras`, `pergunta_invalida` | Entrada inválida ou impossibilidade de gerar claim |
| 404 | `sem_evidencias` | Nenhuma evidência utilizável |
| 502 | `pubmed_indisponivel` | Falha de comunicação ou indisponibilidade externa |
| 500 | `erro_interno` | Erro não previsto pelo fluxo específico |

O formato é `{"erro":{"tipo":"...","mensagem":"..."}}`. O frontend exibe a mensagem e os estados de carregamento previstos. Os seis testes recuperados não cobrem todas as regras de entrada ou todos os estados da interface.

## Dependências externas

O backend carrega MarianMT e Sentence Transformers na inicialização e utiliza o MLP em `data/processed`. Consultas dependem do NCBI. O `.env` configura o ambiente; credenciais não devem ser adicionadas ao controle de versão.
