from django.urls import path
from myproject.core import views as c

app_name = 'core'


urlpatterns = [
    path('', c.home, name='home'),
    path('person/', c.PersonList.as_view(), name='person_list'),
    path('person/add/', c.PersonCreate.as_view(), name='person_add'),
    path('person/<int:pk>/', c.person_detail, name='person_detail'),
    path('person/<int:pk>/edit/', c.person_update, name='person_edit'),
    path('person/<int:pk>/delete/', c.person_delete, name='person_delete'),
    path('last_taskresult/', c.get_last_taskresult, name='last_taskresult')
]
