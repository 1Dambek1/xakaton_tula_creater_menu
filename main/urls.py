
from django.contrib import admin
from django.urls import path,include
from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static

from mainapp.views import LoginsView, RegisterView, logouts
urlpatterns = [
    path("admin/", admin.site.urls),
    path('login',LoginsView.as_view(), name='login'),
    path('registraion', RegisterView.as_view(), name='register'),
    path('', include('mainapp.urls', namespace='main')),
    path('logout', logouts, name = 'logout')

]
if settings.DEBUG:


    urlpatterns += static(settings.MEDIA_URL,document_root =  settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,document_root =  settings.STATIC_ROOT)