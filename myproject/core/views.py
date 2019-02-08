from django.shortcuts import render
from django.urls import reverse_lazy as r
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic import UpdateView, DeleteView
from .mixins import NameSearchMixin
from .models import Person
from .forms import PersonForm
from .tasks import send_email_


def home(request):
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
