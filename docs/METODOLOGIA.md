# Metodologia e resultados

## Tarefa e preparação

O modelo classifica a relação entre uma alegação e uma evidência em três classes, em uma tarefa de inferência entre textos no domínio de saúde. O rótulo não avalia isoladamente o rigor de um estudo ou o consenso científico.

`src/prep.py` substitui ausências por texto vazio, converte as colunas para string, apara espaços e reduz sequências de espaços. Pontuação e capitalização são preservadas.

O `GroupShuffleSplit`, com `random_state=42`, cria treino e um conjunto temporário, depois dividido em validação e teste. Os grupos são as alegações normalizadas. As proporções pretendidas são aproximadamente 70%, 15% e 15%; o agrupamento não garante proporções exatas em linhas.

## Representação e treino

O codificador pré-treinado `all-mpnet-base-v2` gera vetores de 768 dimensões. A entrada concatena o vetor da alegação, o da evidência, sua diferença absoluta e seu produto elemento a elemento. O resultado tem 3.072 dimensões. Não há fine-tuning do SBERT nesse pipeline.

O preparo codifica o texto da base. A aplicação limita a evidência aos primeiros 350 caracteres. A correspondência entre os recortes de treino e inferência merece avaliação adicional.

SMOTE é aplicado ao treino; a divisão fixa de validação e a de teste mantêm sua distribuição original. O projeto compara Regressão Logística, SVM Linear, Random Forest, MLP e XGBoost.

O modelo entregue é um MLPClassifier com camadas ocultas de 256 e 128 neurônios, ReLU, Adam, `alpha=0.01`, taxa inicial `0.001`, até 500 iterações, parada antecipada e `random_state=42`.

## Avaliação da divisão fixa

O modelo salvo e a matriz de validação reproduzem:

| Métrica | Valor arredondado |
|---|---:|
| Acurácia | 69,23% |
| F1 macro | 66,71% |
| Recall macro | 66,39% |
| Recall de refuta | 50,97% |

`results/validation_metrics.json` registra valores sem arredondamento, relatório por classe, matriz de confusão, ambiente e hashes dos artefatos. Os resultados correspondem à validação apresentada. Esta revisão não usa o conjunto de teste para produzir uma nova estimativa final.

O F1 macro dá o mesmo peso às classes. A proximidade entre métricas globais não demonstra desempenho igual por classe.

## Curva de aprendizado

O script original utiliza `learning_curve` com `cv=3`, F1 macro e quatro tamanhos de treino. A apresentação mostra aproximadamente 0,98 no treino e 0,78 na curva de validação.

Esse cálculo não corresponde à divisão fixa da tabela. O `cv=3` também não recebe os grupos de alegações do `GroupShuffleSplit`; uma mesma alegação pode aparecer em partições diferentes da curva. Portanto, a curva não oferece a mesma garantia de separação de alegações da divisão fixa e exige esse cuidado na interpretação.

## Alcance

Não há avaliação documentada por tema médico, de utilidade clínica, de tradução ou de recuperação ponta a ponta. Os índices que vinculam cada linha da planilha às matrizes salvas não foram preservados. Os hashes e as inspeções desta organização identificam os artefatos disponíveis.

Os testes da API usam dependências simuladas e verificam fluxo e contrato. A avaliação offline do MLP salvo é uma verificação distinta, com as matrizes numéricas da entrega. Nenhuma delas representa uma avaliação completa de consultas web com os serviços reais.
