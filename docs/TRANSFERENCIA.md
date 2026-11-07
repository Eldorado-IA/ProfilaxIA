# Preparação da transferência para a equipe

## Destino

A proposta é criar um repositório **privado e vazio**, chamado `ProfilaxIA`, na organização `Eldorado-IA`. O nome proposto não indica que o destino já exista ou esteja publicado. Os repositórios `dataset` e `TesteProjetoIA` não serão substituídos.

## Histórico e acesso

A base é a branch `modelo-producao` de `19loren/project-null`, commit `c3e3b63fdc61a2934da6729cfe7730eb375ed97a`. O histórico original foi preservado na cópia preparada. A nova organização não deve ser apresentada como criação exclusiva de quem a publica.

A conta pessoal no navegador e a conexão utilizada para editar podem ter acessos diferentes. A conexão precisa conseguir consultar e escrever no destino privado. O administrador pode liberar apenas o repositório do ProfilaxIA.

## Publicação

Criar o destino privado vazio, configurar seu endereço como um novo remoto e conferir a permissão de escrita. Enviar inicialmente a branch de organização para revisão. Não enviar essas mudanças ao repositório pessoal de origem por engano.

O objeto Git LFS da matriz de treino também deve ser enviado ao destino. Um push Git sem o objeto não entrega o arquivo completo.

## Cópia para revisão

O arquivo ZIP da versão preparada contém os arquivos atuais, incluindo os dados e o modelo. Ele permite revisar e executar a cópia local, mas não transporta o histórico Git. A publicação com preservação de autoria e histórico deve partir da cópia Git preparada, ou de um clone da origem com as mudanças aplicadas, e incluir os objetos Git LFS.

## Conferência da entrega do link

- Código, documentos, dados e modelo acessíveis aos membros autorizados.
- Matriz Git LFS recuperável no novo destino.
- Histórico e procedência preservados.
- README e links internos válidos.
- Verificações locais identificadas como locais; GitHub Actions identificado conforme a execução efetiva no novo destino.
- Autoria e condições de divulgação alinhadas com a equipe e a residência.

O script legado teve uma chave embutida removida da versão atual. Isso não elimina o valor do histórico original nem substitui sua eventual revogação pelo responsável. O histórico deve ser considerado ao definir a divulgação.

Não adicionar licença unilateralmente, atribuir DOI inexistente ou apresentar esta preparação como artigo publicado. O `CITATION.cff` registra a equipe e o software.
