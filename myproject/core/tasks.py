from __future__ import absolute_import
import time
from celery import shared_task


@shared_task(queue='fila1')
def calculate_sla(email):
    time.sleep(10)
    send_email_.delay(email)
    return "Processo finalizado com sucesso."


@shared_task(queue='fila2')
def send_email_(email):
    # filename = '%s/%s.txt' % (settings.BASE_DIR, email)
    filename = '/tmp/%s.txt' % email
    with open(filename, 'w') as f:
        f.write("!")
    return "E-mail enviado com sucesso para %s" % email


@shared_task(queue='fila3')
def print_numbers(max_number):
    print('Aguardar 10 seg')
    time.sleep(10)
    for i in range(max_number):
        print(i)
    return 'Fim'


@shared_task(queue='fila4')
def parse_cv(filename):
    return True
