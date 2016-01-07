from django.conf.urls import url
import app.views as views

urlpatterns = [
    url(r'^$', views.HomeView.as_view())
]
