# Organização do repositório

## Versão publicada

O repositório [Eldorado-IA/ProfilaxIA](https://github.com/Eldorado-IA/ProfilaxIA) reúne o código, os dados, o modelo e a documentação do First Challenge. A branch principal é `main`.

A consolidação dos arquivos e do histórico de implementação está registrada no commit [`6a8a0ab`](https://github.com/Eldorado-IA/ProfilaxIA/commit/6a8a0ab4b3b2d7187d8e9fe817e046c4f4a7655f). A procedência da implementação está descrita em [Créditos e referências](../CREDITOS.md).

## Estrutura

| Diretório | Conteúdo |
|---|---|
| `backend/` | API FastAPI e serviços de recuperação e classificação |
| `frontend/` | Interface web React e TypeScript |
| `src/` | Implementação de terminal e scripts de preparação e treinamento |
| `data/` | Planilha preparada, matrizes, rótulos e modelo salvo |
| `tests/` e `qa/` | Suíte da API e evidências de execução |
| `docs/` | Documentação técnica e documentos da entrega |
| `scripts/` e `results/` | Verificação dos artefatos e registros de resultados |

## Obtenção dos arquivos

Com Git e Git LFS instalados:

```bash
git clone https://github.com/Eldorado-IA/ProfilaxIA.git
cd ProfilaxIA
git lfs install
git lfs pull
```

A matriz `data/processed/X_train_emb.npy` utiliza Git LFS. Os hashes da planilha, do modelo e das matrizes estão em [`data_manifest.json`](data_manifest.json). As instruções da aplicação e dos experimentos estão em [Reprodução](REPRODUCAO.md).

## Documentação e verificações

O [índice de documentação](README.md) reúne as referências técnicas e os documentos de outubro de 2026. Os testes da API, a compilação do frontend e a avaliação do modelo salvo estão descritos em [Verificação técnica](VERIFICACAO.md).
