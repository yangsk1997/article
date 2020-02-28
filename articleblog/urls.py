from django.shortcuts import render_to_response,render
from django.urls import path,re_path
from .views import *
urlpatterns = [
    # path('index/',index),
    path('about/',about),
    path('listpic/',listpic),
    re_path('newslistpic/(?P<page>\d+)',newslistpic),
    re_path('articleinfo/(?P<id>\d*)',articleinfo),
    re_path('fy_test/(?P<page>\d+)',fy_test),
    path('add_article/',add_article),
    # path('register/',register),
    path('register/',register),
    path('search_article/',search_article),
    # path('ajax_get_req/',ajax_get_req),
    # path('ajax_post_req/',ajax_post_req),



]