# ProfilaxIA

Protótipo acadêmico para recuperar evidências científicas e classificar sua relação com alegações de saúde, desenvolvido pela **Equipe Project NULL** no **First Challenge da Residência em Inteligência Artificial do Instituto ELDORADO em parceria com a PUC Campinas**, em 2026.

O usuário apresenta uma pergunta de sim ou não. A aplicação gera uma alegação, recupera artigos no PubMed/PMC e organiza os trechos encontrados em três classes: **suporta**, **refuta** e **neutro**. Cada evidência mantém a identificação e o link do artigo de origem.

## Equipe Project NULL

- [Gabriella Andrade Silva](https://github.com/moonienng)
- [Loren Tavolaro](https://github.com/19loren)
- [Luís Augusto Ferreira](https://github.com/blackbarth)
- [Prisciele Vitória de Souza](https://github.com/PriscieleSouza)
- [Marcia Regina Stankiwich](https://github.com/MarciaStank)
- [Natalia Silva](https://github.com/Nannnnnnn)

## Documentação

- [Índice e documentos da entrega](docs/README.md)
- [Arquitetura e contrato da API](docs/ARQUITETURA.md)
- [Dados e rastreabilidade](docs/DADOS.md)
- [Metodologia e resultados](docs/METODOLOGIA.md)
- [Como executar e reproduzir](docs/REPRODUCAO.md)
- [Testes da API](README_TESTES.md)
- [Créditos e referências](CREDITOS.md)
- [Registro de mudanças](CHANGELOG.md)

## Problema e objetivo

A circulação de alegações médicas fora de contexto dificulta a consulta às evidências. O ProfilaxIA explora recuperação de artigos e classificação supervisionada para aproximar uma pergunta das fontes científicas relacionadas. O recorte de treinamento é o HealthVer, construído a partir de alegações sobre COVID-19.

A saída corresponde à relação entre **uma alegação e um trecho**. Ela não constitui, por si só, uma avaliação do consenso científico, do rigor metodológico do artigo ou da situação clínica de uma pessoa.

## Componentes

| Componente | Tecnologia | Localização |
|---|---|---|
| Interface web | React, TypeScript e Vite | `frontend/` |
| API | Python e FastAPI | `backend/` |
| Tradução e análise linguística | MarianMT, spaCy e YAKE | `backend/app/services/nlp.py` |
| Recuperação de artigos | PubMed/PMC e XML JATS | `backend/app/services/pubmed.py` |
| Classificação | Embeddings fixos MPNet e MLPClassifier | `backend/app/services/classificador.py` |
| Preparação, comparação e treino | Sentence Transformers, scikit-learn e SMOTE | `src/` |
| Testes de integração da API | pytest e TestClient | `tests/` |

## Resultados do modelo

Resultados da avaliação do modelo `.pkl` salvo sobre os **1.797 pares da matriz de validação** da entrega.

| Métrica | Resultado |
|---|---:|
| Acurácia | 69,23% |
| F1 macro | 66,71% |
| Recall macro | 66,39% |
| Recall da classe refuta | 50,97% |

O [registro da avaliação](results/validation_metrics.json) identifica os arquivos e o ambiente utilizados. Esses números correspondem à **validação**, como no slide 10 da apresentação, e não a uma nova avaliação do conjunto de teste.

**Versão dos dados:** a planilha presente no código contém **13.303 pares**. A apresentação histórica informa 13.309 pares. Essa divergência, as contagens verificadas e a normalização das alegações estão documentadas em [Dados](docs/DADOS.md).

## Execução da aplicação

Pré-requisitos: Docker com Compose, Git e Git LFS. A inicialização dos modelos requer acesso à internet.

1. Clone este repositório e execute `git lfs install` e `git lfs pull`.
2. Copie `.env.example` para `.env` e ajuste a configuração do NCBI.
3. Na raiz, execute:

```bash
docker compose up --build backend frontend
```

A interface é configurada em `http://localhost:5173` e a documentação da API em `http://localhost:8000/docs`. O perfil de produção e as instruções para Windows estão em [Reprodução](docs/REPRODUCAO.md).

## Verificações da entrega

- Testes de contrato e integração da API com dependências externas simuladas, com evidências em `qa/`.
- Compilação TypeScript e build do frontend.
- Reprodução offline das métricas do classificador sobre a matriz de validação salva.

Os seis testes da API verificam entradas, agrupamento, fontes e respostas de erro. PubMed, tradução, conversor linguístico e classificador são simulados nesses testes. A execução não equivale a um teste completo da interface com os serviços reais. A reprodução das métricas acima é uma verificação distinta e utiliza o **MLP real salvo**.

```bash
python -m pip install -r requirements-test-lock.txt
python -m pytest -v --junitxml=qa/resultados.xml
```

O workflow em `.github/workflows/verificacoes.yml` executa os testes da API e a compilação do frontend no GitHub Actions. As duas verificações foram aprovadas na [execução do commit `6a8a0ab`](https://github.com/Eldorado-IA/ProfilaxIA/actions/runs/42431631345). Os registros locais e o alcance das verificações estão em [Verificação técnica](docs/VERIFICACAO.md).

## Limitações

- O treino utiliza pares do HealthVer; as consultas recuperam trechos de conclusões de outros artigos.
- A busca lexical e o fallback podem recuperar textos pouco pertinentes.
- O buscador limita a conclusão a 900 caracteres; a inferência utiliza os primeiros 350.
- A tradução e a conversão em alegação podem alterar o sentido ou produzir construções inadequadas.
- O recall de refuta é o menor entre as classes na validação apresentada.
- A curva de aprendizado histórica utiliza outro protocolo e não equivale à divisão fixa de validação.
- A revisão não inclui avaliação por tema médico, teste de carga ou execução completa da consulta web com NCBI e todos os modelos reais.

## Créditos e citação

Os créditos do projeto e as referências dos recursos utilizados estão em [CREDITOS.md](CREDITOS.md). Os metadados de citação do software estão em [CITATION.cff](CITATION.cff).

Artigo de origem da base:

Sarrouti, M.; Ben Abacha, A.; Mrabet, Y.; Demner-Fushman, D. **Evidence-based Fact-Checking of Health-related Claims**. Findings of EMNLP 2021, p. 3499–3512. DOI: [10.18653/v1/2021.findings-emnlp.297](https://doi.org/10.18653/v1/2021.findings-emnlp.297).
