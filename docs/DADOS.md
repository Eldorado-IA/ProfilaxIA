# Dados e rastreabilidade

## Origem

O HealthVer foi apresentado por Sarrouti et al. em 2021. Alegações foram extraídas de snippets de buscas sobre COVID-19; artigos científicos vieram do CORD-19, versão de 16 de julho de 2020, composto majoritariamente por publicações do PubMed Central. Anotadores humanos selecionaram evidências de resumos e títulos e rotularam os pares como suporta, refuta ou neutro.

Referência: [Evidence-based Fact-Checking of Health-related Claims](https://aclanthology.org/2021.findings-emnlp.297/), seções 3 e 4. A base original é descrita com 14.330 pares. Consulte o [repositório dos autores](https://github.com/sarrouti/healthver) quanto aos arquivos e termos originais.

O arquivo deste projeto é uma **versão preparada**: `data/raw/healthver_preparado_completo_3classes.xlsx`. A palavra `raw` no caminho é uma convenção do projeto, não indicação de cópia bruta e inalterada do HealthVer.

## Unidade de análise

Cada linha é um par de alegação e evidência. A relação entre os textos é de muitos para muitos. Repetir somente a alegação ou somente a evidência não caracteriza duplicação do par.

Colunas: `id`, `evidence`, `claim`, `label`, `topic_ip` e `label_multiclasse`. O treino usa `claim`, `evidence` e `label_multiclasse`.

| Código | Classe na API | Significado |
|---|---|---|
| 0 | SUPPORTED | A evidência apoia a alegação |
| 1 | REFUTED | A evidência contradiz a alegação |
| 2 | NEUTRAL | O trecho não permite concluir a favor nem contra; pode ser irrelevante |

## Contagens por versão

| Registro | Pares | Alegações distintas |
|---|---:|---:|
| Apresentação, slide 5 | 13.309 | 1.855, conforme o slide |
| Planilha preservada na branch de entrega | 13.303 | 1.854 antes da normalização |
| Mesma planilha após normalizar espaços | 13.303 | 1.851 |

A inspeção da planilha não encontrou pares duplicados literais nem após normalizar espaços. A diferença no número de alegações distintas decorre de variantes de espaços, agrupadas na preparação.

As quantidades de linhas dos artefatos são compatíveis com o total da planilha: 9.428 de treino, 1.797 de validação e 2.078 de teste, totalizando 13.303. Essa compatibilidade não prova correspondência linha a linha, pois os índices das partições não foram persistidos na entrega original.

Os 13.309 pares dos slides não são a contagem da planilha atual. Não se deve inferir o número de duplicatas removidas apenas pela subtração entre etapas sem o registro de preparação.

## Verificação dos arquivos

`data_manifest.json` registra contagens e hashes SHA-256. Para repetir a inspeção, com pandas, openpyxl e numpy instalados:

```bash
python scripts/inspect_dataset.py --output docs/data_manifest.json
```

O script não gera embeddings nem treina. A matriz `data/processed/X_train_emb.npy` é versionada por Git LFS: após clonar, execute `git lfs install` e `git lfs pull`.

O treinamento usa o HealthVer. Em uso, a aplicação recupera conclusões de outros artigos com procedimentos e recortes diferentes. Essa mudança de distribuição precisa ser considerada ao interpretar o desempenho.
