
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth


urlpatterns = [
    path('login/', views.Login, name ='login'),
    # path('logout/', auth.LogoutView.as_view(template_name ='analyzer_app/index.html'), name ='logout'),
    path('register/', views.register, name ='register'),
    path('logout/', views.custom_logout, name='logout'),
    path('', views.index, name ='index'),

    path('addnew/',views.addnew, name='addnew'),  
    path('edit/<int:id>', views.edit, name='edit'),  
    # path('update/<int:id>', views.update, name='update'),  
    path('delete/<int:id>', views.destroy, name='destroy'),
]
