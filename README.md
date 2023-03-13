# ZJWEU-Authserver-Proxy
浙江水利水电学院 统一身份认证系统 代理用户登录

由于要在非官方的服务平台集成高校的统一身份认证，故使用Python实现了统一身份认证系统登录的模块，本代码以浙江水利水电学院统一身份认证系统为例，集成了验证码识别，仅供学习使用，切勿用于非法途径。

本代码是在Django里面开发的，所以可以直接套用进Django里，但是记得安装代码里需要的几个库，

## views.py

以下URL中service后面的xxxxxxxx处替换需要登录的系统

> login_url = 'https://authserver6.zjweu.edu.cn/authserver/login?service=xxxxxxxx'

> login_post_url = 'https://authserver6.zjweu.edu.cn/authserver/login?service=xxxxxxxx'


此处URL是统一身份认证系统的验证码地址，后面带参数是为了防止出现用了相同的验证码，所以用了一个时间戳加以区别，保证每次请求的验证码都是不一样的

> pic = sess.get('https://authserver6.zjweu.edu.cn/authserver/captcha.html?ts=' + str(time.time())).content

这里是保存获取到的验证码的路径，可以自行修改，建议自行添加一个删除已使用过的验证码的地方，这里就不再补充了

> pngname = 'yzm/'+str(time.time())+'.png'
> 
登录成功后，通过已登录系统的api获取当前用户信息

> userurl = 'https://oa.zjweu.edu.cn/api/ecode/sync'


## encrypt.js

这个是统一身份认证为了加密用户的post数据而加的crypt加密方法，同样的系统加密方式是一样的，如有不同仅供参考

## 声明

本代码也是由别人的一个代码修改而来的，增加了验证码识别，修改并完善了一些，仅供学习参考，切勿用于违法！
