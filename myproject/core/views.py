import timeit
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy as r
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic import UpdateView, DeleteView
from django_celery_results.models import TaskResult
from .mixins import NameSearchMixin
from .models import Person
from .forms import PersonForm
from .tasks import send_email_, print_numbers, running_django_command


def home(request):
    print('request.session:', request.session.get('res_celery_id'))
    return render(request, 'index.html')


class PersonList(NameSearchMixin, ListView):
    model = Person
    paginate_by = 5


person_detail = DetailView.as_view(model=Person)


class PersonCreate(CreateView):
    model = Person
    form_class = PersonForm

    def form_valid(self, *args, **kwargs):
        response = super(PersonCreate, self).form_valid(*args, **kwargs)
        first_name = self.object.first_name
        last_name = self.object.last_name
        email = self.object.email

        send_email_.delay('{} {} <{}>'.format(first_name, last_name, email))

        # Iniciando contagem do cronometro
        tic = timeit.default_timer()

        # Chamando task para teste do django_celery_results
        res = print_numbers.delay(10)

        # Chamando task que executa um custom Django command
        running_django_command.delay()

        print('res print_numbers id', res.id)
        # print('res print_numbers get', res.get())  # demora
        # if res.get():  # demora
        #     print('Demorou, mas chegou', res.result)
        #     print('aqui', get_last_taskresult(self.request, res.id))
        #     if self.request.session['res_celery_id'] != res.id:
        #         pass

        self.request.session['res_celery_id'] = res.id
        # Fim do cronometro
        toc = timeit.default_timer()
        end = toc - tic
        print('time', end)
        if end > 60:
            print(end / 60, 'min')

        return response

    # def post():
    #     files = request.GET.getlist(files)
    #     for file in files:
    #         parse_cv.delay(file)


person_update = UpdateView.as_view(model=Person, form_class=PersonForm)

person_delete = DeleteView.as_view(
    model=Person,
    success_url=r('core:person_list')
)


def get_last_taskresult(request, task_id=None):
    '''
    Pega o id do último TaskResult
    '''
    # print('request.session:', request.session['res_celery_id'])
    res_celery_id = request.session.get('res_celery_id')
    # task_result = TaskResult.objects.get(task_id=task_id)
    task_result = TaskResult.objects.filter(task_id=res_celery_id).first()
    res = {'res_celery_id': res_celery_id}
    if task_result:
        res['task_result'] = task_result.result
    return JsonResponse(res)
