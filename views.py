from django.shortcuts import render
import requests
import re
import execjs
import sys
import json
import os 
import ddddocr
import time
import random
import datetime
from datetime import date, timedelta
from PIL import Image 
from django.http import JsonResponse,HttpResponse
from django.core import serializers
from .models import *
from django.contrib.auth.hashers import make_password, check_password

def login(sess, uname, pwd):
    login_url = 'https://authserver6.zjweu.edu.cn/authserver/login?service=https://oa.zjweu.edu.cn/wui/cas-entrance.jsp?path=/wui/index.html#/main/portal/portal-1-1?menuIds=0,1&menuPathIds=0,1&_key=5uwsuw&ssoType=CAS'
    get_login = sess.get(login_url)
    get_login.encoding = 'utf-8'
    lt = re.search('name="lt" value="(.*?)"', get_login.text).group(1)
    salt = re.search('id="pwdDefaultEncryptSalt" value="(.*?)"', get_login.text).group(1)
    execution = re.search('name="execution" value="(.*?)"', get_login.text).group(1)
    
    pic = sess.get('https://authserver6.zjweu.edu.cn/authserver/captcha.html?ts='+str(time.time())).content
    pngname = 'yzm/'+str(time.time())+'.png'
    with open(pngname, 'wb') as fs:
        fs.write(pic)
    ocr = ddddocr.DdddOcr()
    with open(pngname, 'rb') as fss:
        img_bytes = fss.read()
    respng = ocr.classification(img_bytes)
    
    f = open("encrypt.js", 'r', encoding='UTF-8')
    line = f.readline()
    js = ''
    while line:
        js = js + line
        line = f.readline()
    ctx = execjs.compile(js)
    password = ctx.call('_ep', pwd, salt)

    login_post_url = 'https://authserver6.zjweu.edu.cn/authserver/login?service=https://oa.zjweu.edu.cn/wui/cas-entrance.jsp?path=/wui/index.html#/main/portal/portal-1-1?menuIds=0,1&menuPathIds=0,1&_key=5uwsuw&ssoType=CAS'
    personal_info = {'username': uname,
                     'password': password,
                     'lt': lt,
                     'dllt': 'userNamePasswordLogin',
                     'execution': execution,
                     'captchaResponse':respng,
                     '_eventId': 'submit',
                     'rmShown': '1'}
    post_login = sess.post(login_post_url, personal_info)
    post_login.encoding = 'utf-8'
    userurl = 'https://oa.zjweu.edu.cn/api/ecode/sync'
    getUser = json.loads(sess.get(userurl).text)
    
    try:
        getUser["_data"]["_user"]
    except KeyError:
        json_dict = {'errcode':404,'errmsg':'登录失败，请重试'}
        return (json_dict)
    else:
        userData = getUser["_data"]
        print(userData)
        json_dict = {'errcode':200,'errmsg':'获取成功','userId':uname,'userName':getUser["_data"]["_user"]["resourceName"],'deptName':getUser["_data"]["_user"]["departmentName"]}
        return (json_dict)
      
def loginMain(request):
    if request.method == 'POST':
        username = request.POST.get('stuid','')
        password = request.POST.get('stupwd','')
        if username=='' or password=='':
            loginText = {'errcode':403}
        else:
            sess = requests.session()
            loginText = login(sess, username, password)
            if loginText['errcode']==200:
                request.session['uid']=username #登录成功
            sess.close()
    else:
        loginText = {'errcode':403}
    return JsonResponse(loginText, safe=False)
