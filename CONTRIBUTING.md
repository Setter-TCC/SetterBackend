# Guia de Contribuição

## Como contribuir?

Para contribuir com o projeto é muito fácil e cada pouquinho conta! Basta seguir os seguintes passos:

* *Fork* do repositório (apenas para usuários externos)
* Criar [*issues*](CONTRIBUTING.md#política-de-issues)
* Criar [*branchs*](CONTRIBUTING.md#política-de-branches)
* Seguir a política de [*commits*](CONTRIBUTING.md#política-de-commits)
* Submeter [*Pull Request*](CONTRIBUTING.md#política-de-merges-e-pull-requests)


### Política de Issues

As *issues* devem possuir título, descrição, no mínimo um assinante responsável, *labels*.

Caso seja uma nova funcionalidade, que engloba o Frontend e Backend, ela pode ser criada no [Repositório de Documentação](https://github.com/Setter-TCC/SetterDocs). Caso seja um *bug*, a *issue* pode ser criada no repositório onde o problema foi identificado.

As Labels usadas no projeto estão descritas no tópico [Labels](https://github.com/Setter-TCC/SetterDocs/labels) no Github.


### Política de Branches

#### *main*

A branch *main* é a branch de produção, onde ficará a versão estável do projeto. Ela estará bloqueada para commits e para pushs.

#### *devel*

A branch *devel* é a branch de desenvolvimento, onde o trabalho das outras branchs será unificado e onde será criada uma versão estável para mesclar com a *main*.
Assim como a *main* ela está bloqueada para commits e pushs.

#### Nome das Branches

As branchs de desenvolvimento de features serão criadas a partir da branch *devel* com a nomenclatura padrão ```x-<nome da branch>```, onde o `x` representa o número da issue.

### Política de Commits

A issue em questão deve ser citada no commit, para isso, basta adicionar o número no início da mensagem da seguinte forma: ```[nº issue] mensagem```.

```
 [05] Fazendo guia de contribuição
```

Para que ambos envolvidos no commit sejam incluidos como contribuintes no gráfico de commits do GitHub, basta incluir a instrução `Co-authored-by:` na mensagem:

```
[5] Fazendo guia de contribuição

Co-authored-by: Fulano <fulano@outlook.com>
Co-authored-by: Beltrano <beltrano@gmail.com>

```

### Política de Merges e Pull Requests

#### Pull Requests

Pull requests devem ser feitos para a branch *main* seguindo as regras e os passos do tópico [*Merges para main*](CONTRIBUTING.md#merges-para-main). No conteúdo do pull request deve haver uma descrição clara do que foi feito.

Deve ser seguido de uma descrição, os PRs relacionados, e as tarefas gerais realizadas.

#### Merges para *main*
Os merges para *main* deverão ser feitos quando a funcionalidade ou refatoração estiverem de acordo com os seguintes aspectos:
- Funcionalidade ou refatoração concluída;
- Funcionalidade revisada por algum outro membro.

Para fazer um merge para *main* os passos a serem seguidos são:
- `git checkout branch_de_trabalho`;
- `git pull --rebase origin main`;
- `git push origin branch_de_trabalho`;
- Abrir pull request via interface GitHub;
- Aguardar Code Review


##### Code Review
O code review deve ser feito por um ou mais membros da equipe que não participaram das modificações.
Após pelo menos uma aprovação de Code Review, Status Check (Travis, CodeClimate) o PullRequest poderá ser aceito;

Para aceitar o PullRequest, deve-se usar a opção *merge* no Github.
