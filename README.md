# dva-flask-blog
一个博客模板，前端使用dva框架（封装了react，redux，redux-saga，react-redux，react-router等，个人感觉这框架是react最佳实践，让你的前端代码写起来更轻松，更易维护），后端使用python的轻量级web框架flask（连接数据库，为前端提供RESTful的api接口）。
##后端
后端有两个作用：
连接数据库，从数据库中拿出前端需要展现的数据。
提供API，便于前端调用。说白了，就是提供数据。

1.连接数据库：
先谈谈怎样构造一个flask的后端。首先建立一个flask的web应用：
```python
from flask import Flask
app = Flask(__name__)
```
ok,现在我们已经有了一个web应用了，但这个应用有啥用呢？我们知道，当我们调用RESTful api的时候，请求一个url，类似https://api.example.com/users ，然后就会获得一些数据，最常见的是json数据：
```json
{"users":[
{
"name":"xiaoming",
"age":18
},
{
"name":"xiaohua",
"age":19
}
]}
```所以我们要做的就是搞出一个这样的url来。
在flask里，使用的是一个装饰器：app.route来定义路由.
```python
@app.route('/')
      def index():
          return '<h1>Hello World!</h1>'
```
