# django-celery-estudo

Estudo de Django e Celery

**Material:** [Tarefas demoradas de forma assíncrona com Django e Celery](https://fernandofreitasalves.com/tarefas-assincronas-com-django-e-celery/)

```
celery --app=myproject worker --loglevel=INFO --queue=fila1,fila2,fila3
```

## Como rodar o projeto?

* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.
* Rode as migrações.

```
git clone https://github.com/rg3915/django-celery-estudo.git
cd django-celery-estudo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python contrib/env_gen.py
python manage.py migrate
python manage.py createsuperuser --username='admin' --email=''
python manage.py shell_plus < shell/shell_person.py
```