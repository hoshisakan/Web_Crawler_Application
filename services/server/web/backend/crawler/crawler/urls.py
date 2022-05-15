"""crawler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from django.conf.urls.static import static
# from django.conf import settings
from google_search.views import GoogleSearchNewsViewset, GoogleSearchVideoViewset, \
                            GoogleSearchViewset
from stock.views import StockInfoViewset
from ptt.views import PttBoardInfoViewset, PttArticlesInfoViewset
from tasks.views import TasksResultViewset, ExtraTaskInfoViewset
from users.views import UserViewset


router = DefaultRouter(trailing_slash=False)
router.register(prefix=r'google-search/news', viewset=GoogleSearchNewsViewset, basename='access google search news info')
router.register(prefix=r'google-search/video', viewset=GoogleSearchVideoViewset, basename='access google search video info')
router.register(prefix=r'stock', viewset=StockInfoViewset, basename='access obtain stock info')
router.register(prefix=r'ptt/board', viewset=PttBoardInfoViewset, basename='access ptt board info')
router.register(prefix=r'ptt/article', viewset=PttArticlesInfoViewset, basename='access ptt article info')
router.register(prefix=r'tasks/base', viewset=TasksResultViewset, basename='access celery task result info')
router.register(prefix=r'tasks/extra', viewset=ExtraTaskInfoViewset, basename='access celery task extra info')
router.register(prefix=r'users', viewset=UserViewset)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/google-search/obtain-info', GoogleSearchViewset.obtain_info_by_crawler , name='obtain google search info'),
]
