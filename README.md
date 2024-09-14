# ZJWEU_SSO_Proxy

浙江水利水电学院 统一身份认证系统 代理用户登录

本程序仅供在非官方服务平台集成学校统一身份认证登录获取信息，以浙江水利水电学院统一身份认证系统为例，集成验证码识别，仅供学习使用，切勿用于非法途径。

## views.py

以下URL中service后面的xxxxxxxx处替换需要登录的系统

> login_url = 'https://authserver6.zjweu.edu.cn/authserver/login?service=xxxxxxxx'

> login_post_url = 'https://authserver6.zjweu.edu.cn/authserver/login?service=xxxxxxxx'


此处URL是统一身份认证系统的验证码地址，后面带参数是为了防止出现用了相同的验证码，所以用了一个时间戳加以区别，保证每次请求的验证码都是不一样的

> pic = sess.get('https://authserver6.zjweu.edu.cn/authserver/captcha.html?ts=' + str(time.time())).content

这里是保存获取到的验证码的路径，可以自行修改

> pngname = 'yzm/'+str(time.time())+'.png'
> 
登录成功后，通过已登录系统的api获取当前用户信息

> userurl = 'https://oa.zjweu.edu.cn/api/ecode/sync'


## encrypt.js

此为加密用户的post数据而加的crypt加密方法

## 声明

程序根据其他版本增加了验证码识别，仅供学习参考，切勿用于违法
