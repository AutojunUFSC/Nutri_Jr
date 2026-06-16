O sistema tem duas configurações, uma pra desenvolvimento (no nosso computador) e uma pra produção (rodando no servidor com cliente usando). O sistema tem duas configurações, uma pra dev e outra pra prod que mudam por exemplo o banco de dados que em dev é Sqlite e em prod é PostgreSQL entre outras várias coisas

Atualizar produção:

**Se for critico, faça backup dos dados pelo** https://www.heroku.com/ 

**Esteja com o codigo certo**

1. Vai pra branch master do projeto no seu computador usando

`git checkout master`

2. Esteja com a versão mais atualizada dela com o origin (gitlab) usando 

`git pull`

**Ative as configuarações de prod**

1. No arquivo manage.py mudar `'nutri.settings.dev'` para `'nutri.settings.prod'`
2. Registre isso no seu repositorio local com

`git add manage.py`

`git commit -m "Alterada para settings em prod"`

**Atualize os repositorios**
1. Que ta no gitlab com

`git push`

2. Que ta no server heroku com 

`git push heroku master`

>Talvez precise do --force pra sobrepor o repositorio que ta no heroku com o que ta no seu repositorio local

3. Se precisar fazer migrações use

`heroku run python manage.py makemigrations`

`heroku run python manage.py migrate`

ouuuu essa outra sequência

`heroku run bash`

`python manage.py makemigrations`

`python manage.py migrate`

4. Se ainda vai ter trabalho em dev refaz o item 2 mas dessa vez voltando pra nutri.settings.dev pra quando alguém for mexer em dev não dar uns erros doidos

**Mais informações:** https://docs.google.com/document/d/1sgpPSoQyQIjGlzX_VJcubjk9jbbLdR_rlsTHCqW-rK8/edit
* Como acessar o banco e fazer querys
* Credenciais de acesso ao sistema
* Ajuda com bugs
* Detalhes do servidor
* etc . . .
