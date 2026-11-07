# Registro de mudanças

## Organização da entrega coletiva em novembro de 2026

- Preservação do histórico e identificação do commit original de entrega.
- README com objetivo, arquitetura, dados, métricas, limitações e reprodução.
- Índice dos documentos originais, slides, testes e procedência dos arquivos.
- Incorporação dos seis testes de contrato e integração da API e de suas evidências históricas.
- Preparação de workflow de testes e build para GitHub Actions.
- Lockfile do frontend e arquivos de dependências para repetir as verificações locais.
- Correção do build TypeScript: tipos do Node usados na configuração do Vite.
- Inclusão de `imbalanced-learn` e `seaborn`, importados no treino, nos requisitos.
- Padronização do codificador em `src/prep.py` para `all-mpnet-base-v2`, utilizado pelo backend.
- Remoção de bytecode Python versionado.
- Substituição da chave de API embutida no script de terminal por leitura de `NCBI_API_KEY` do ambiente. A mudança atual não remove valores de commits históricos nem revoga credenciais.
- Registro das contagens da planilha efetivamente presente no código e da diferença em relação aos slides.
- Reprodução das métricas do modelo salvo na matriz de validação, sem novo treino.

As correções de configuração e documentação não representam novos resultados de treinamento. Os registros de verificação identificam seus próprios ambientes e arquivos.
