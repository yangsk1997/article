from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from django.core.paginator import Paginator
from django.http import JsonResponse


# Create your views here.

def loginValid(func):
    def inner(request,*args,**kwargs):
        cookie_username = request.COOKIES.get('username')
        session_username = request.session.get('username')
        if cookie_username and session_username and cookie_username==session_username:
            return func(request,*args,**kwargs)
        else:
            return HttpResponseRedirect('/login/')
    return inner

@loginValid
def index(request):
    # 1、返回6条文章数据 排序  按照时间逆序
    article = Article.objects.order_by('-date')[:6]
    # 2、返回图文推荐内容 7 条
    # 图文推荐：获取到推荐的文章 数据库中应该有推荐的字段 标识
    recommend_article = Article.objects.filter(recommend=1).order_by('-date')[:7]
    # 3、点击排行12条内容
    click_article = Article.objects.order_by('-click')[:12]

    return render_to_response('index.html',locals())

def about(request):
    return render_to_response('about.html')

def listpic(request):
    return render_to_response('listpic.html')

def newslistpic(request,page):
    # article  = Article.objects.all().order_by('id')
    article_type = request.GET.get('type')
    A_type = Type.objects.filter(name=article_type).first()
    article = A_type.article_set.all()
    pagniator_obj = Paginator(article,6)
    page_obj = pagniator_obj.page(page)
    page_num = page_obj.number
    start = page_num - 2
    if start <= 2:
       start = 1
       end = start + 5
    else:
        end = page_num + 3
        if end >= pagniator_obj.num_pages:
            end = pagniator_obj.num_pages+1
            start = end-5
    page_range = range(start,end)




    return render_to_response('newslistpic.html',locals())

def articleinfo(request,id):

    article = Article.objects.get(id = id)
    article1 = Article.objects.filter(id=id).first()
    article1.click += 1
    article1.save()

    return render_to_response('articleinfo.html',locals())

def fy_test(request,page):
    #查询文章的方法
    article = Article.objects.all().order_by('id')
    paginator_obj = Paginator(article,6)
    page_obj = paginator_obj.page(page)


    return HttpResponse('fy_test')

# 增加多条数据
def add_article(request):
    for i in range(100):
        article = Article()
        article.title = 'title_%s'%i
        article.content = 'content_%s'%i
        article.description = 'description_%s'%i
        article.author = Author.objects.get(id = 1)
        article.save()
        article.type.add(Type.objects.get(id=1))
        article.save()

    return HttpResponse('增加多条数据')

import hashlib
def setPassword(password):
#     实例化md5对象
    md5 = hashlib.md5()
# 对password进行加密
    md5.update(password.encode())
    result = md5.hexdigest()
    return result

from .forms import UserForm
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username and password:
        user = User.objects.filter(username=username).first()
        if user.username == username and user.password == setPassword(password):
            response = HttpResponseRedirect('/')
            response.set_cookie('username',username)
            request.session['username'] = username
            return response
        else:
            message = '用户名或密码错误'
    else:
        message = '账号密码不能为空'
    return render(request, 'login.html', locals())

# 返回ajax页面
def register(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username and password:
        flag = User.objects.filter(username=username).exists()
        if flag:
            message = '用户已经存在'
        else:
            User.objects.create(username=username,password=setPassword(password))
            return HttpResponseRedirect('/login/')
    else:
        message = '账号密码不能为空'
    return render(request, 'register.html',locals())

# 处理ajax get 请求
# def ajax_get_req(request):
#     '''
#     处理ajax的get请求
#         获取到ajax的值，进行查询数据库，判断用户是否存在
#     :param request:
#         username 用户账号
#     :return:
#         返回是否存在的结果
#     '''
#     username = request.GET.get('username')  #GET获取的是get方法请求的参数
#     result = {'code':10000,'msg':''}
#     if username:
#         if 'admin' not in username:
#             if 4 <= len(username) <= 8:
#                 flag = User.objects.filter(username=username).exists()
#                 if flag:
#                     #账号存在
#                     result = {'code':10001,'msg':'账号已经存在，请换个账号'}
#                 else:
#             #         账号不存在，可以在数据库中创建
#                     result = {'code':10000,'msg':'账号不存在，可以用'}
#             else:
#                 result = {'code':10004,'msg':'用户名必须在4到8位之间'}
#         else:
#             result = {'code':10003,'msg':'不能包含admin'}
#     else:
#     #     账号不能为空
#         result = {'code':10002,'msg':'账号不能为空'}
#     return JsonResponse(result)
#
# def ajax_post_req(request):
#     result = {'code':10000,'msg':""}
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     if password and username:
#         User.objects.create(username=username,password=setPassword(password))
#         result = {'code':10001,'msg':'注册成功'}
#         # return HttpResponseRedirect('/login/')
#     else:
#         result = {'code':10002,'msg':'注册失败'}
#
#     return JsonResponse(result)
def search_article(request):
    search_key = request.GET.get('search_key')
    page = request.GET.get('page',1)
    if search_key:
        article = Article.objects.filter(title__contains=search_key).all()
        pagniator_obj = Paginator(article, 6)
        page_obj = pagniator_obj.page(page)
        page_num = page_obj.number
        start = page_num - 2
        if start <= 2:
            start = 1
            end = start + 5
        else:
            end = page_num + 3
            if end >= pagniator_obj.num_pages:
                end = pagniator_obj.num_pages + 1
                start = end - 5
        page_range = range(start, end)
    return render(request,'newslistpic.html',locals())

