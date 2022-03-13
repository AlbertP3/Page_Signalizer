from django.contrib import admin
from django.urls import path, include
from core import views as core_views
from django.contrib.auth.decorators import login_required

app_name = 'core'

urlpatterns = [
    path('', core_views.home_page, name='home'),
    path('add/', login_required(core_views.Render_add.as_view()), name='add'),
    path('scrape/<int:id>/', core_views.render_scrape, name='scrape'),
    path('modify/<int:id>/', core_views.update_template, name='update'),
    path('delete/<int:id>/', core_views.delete_template, name='delete'),
]
