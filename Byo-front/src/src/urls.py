from django.urls import path
from app import views

urlpatterns = [   
     path('', views.home,name='home'), 
     path('modelagem', views.modelagem, name='modelagem'),
     path('proteina', views.proteina, name='proteina'),
     path('executar_pipeline/', views.executar_pipeline, name='executar_pipeline'),
]
