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
"id":1,
"name":"xiaoming",
"age":18
},
{
"id":2,
"name":"xiaohua",
"age":19
}
]}
```
所以我们要做的就是搞出一个这样的url来。
在flask里，使用的是一个装饰器：app.route来定义路由(url).
```python
@app.route('/')
def index():
    return '<h1>Hello World!</h1>'
```
这段代码的意思是以根路径'/'为路由，定义一个路由函数:index,这个路由函数返回一串数据。在本例里，这个数据是一段html。于是当我们启动这个web应用的时候，就能看到一个"Hello World!"的页面。启动web应用的代码：
```python
if __name__ == '__main__':
   app.run()
```
等等，刚刚不是说好的要返回json数据吗，怎么返回了一个"Hello World!"的页面？？？
因为作为一个码农，写个demo必定要"Hello World!"一下才爽啊！
言归正传，怎样返回json数据呢？想必同学们都应该看懂了，路由函数里return什么值，我们访问这个路由就会得到什么值。所以我们就把```<h1>Hello World!</h1>```改成那段json数据就行了。对了，那么路由就不应该是根路由'/'了，而是我们刚刚举的例子里的'/users'。flask里有一个包叫json，负责把python的dict数据与json格式的数据互相转换。于是整个代码是这个样子:
```python
from flask import Flask, json
app = Flask(__name__)

@app.route('/users')
def index():
    respJson = json.dumps({"users": [
    {
        "id": 1,
        "name": "xiaoming",
        "age": 18
    },
    {
        "id": 2,
        "name": "xiaohua",
        "age": 19
    }
]})
    return respJson
    
if __name__ == '__main__':
    app.run()
```
