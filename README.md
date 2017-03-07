# dva-flask-blog
一个新手向博客模板，前端使用dva框架（封装了react，redux，redux-saga，react-redux，react-router等，个人感觉这框架是react最佳实践，让你的前端代码写起来更轻松，更易维护），后端使用python的轻量级web框架flask（连接数据库，为前端提供RESTful的api接口）。
##后端
后端有两个作用：
连接数据库，从数据库中拿出前端需要展现的数据。
提供API，便于前端调用。说白了，就是提供数据。

###连接数据库：
1.构造一个最简单的flask后端。
先谈谈怎样构造一个flask的后端。首先建立一个flask的web应用：
```python
from flask import Flask
app = Flask(__name__)
```
ok,现在我们已经有了一个web应用了，但这个应用怎么用呢？我们知道，当我们调用RESTful api的时候，请求一个url，类似https://api.example.com/users ，然后就会获得一些数据，最常见的是json数据：
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
这段代码的意思是以根路径'/'为路由，定义一个路由函数:index,这个路由函数返回一串数据。在本例里，这个数据是一段html。于是当我们启动这个web应用的时候，就能在本机的5000端口看到一个"Hello World!"的页面，也就是你在浏览器输入localhost:5000就能看到这个页面。启动web应用的代码：
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
此时我们输入localhost:5000/users,就能看到浏览器返回了刚刚的json数据. **注意：路由改成了/users所以要访问localhost:5000/users了，而不是根路由localhost:5000了**  

![img_users](http://oh8c4fk40.bkt.clouddn.com/0A9BE314-523D-452A-97C6-55E93E236439.png)  

2.数据库与SQLAlchemy  

通过上面的步骤，我们知道了后端怎么把json数据给出来。
可是这个json数据是哪里来的呢？喂，这个json数据不就是你自己写的吗，这都要问，智障。
对的，这个json数据是我们自己写的，而且是直接在代码里敲出来的，这样太low了啊，你写博客的时候直接在代码里敲文字吗？所以我们需要一个数据来源，那就是数据库。那数据库里的数据哪里来的呀？你自己输入的。

。。。。。。
那我们为什么要用数据库呢？

- 第一，数据库里可以存很多数据，几个G都是小意思。可是代码里面就不可能写这么多数据吧。试想一下，你的后端代码里有一万行是你写的文章，但是只有几百行是你的代码。那样看上去该多恶心啊！

- 第二，数据库里的数据可以分类，而且使用数据库查询语言（例如SQL）可以筛选出我们想要的各种各样的数据。比如，你突然想做一个自己的短篇博客合集，那么就可以用SQL筛选出自己博客文章里小于1000字的博客，是不是方便多了呢？  


可能你有个疑问，既然我们的数据都是从数据库里来的，为什么我们不直接把数据库里的数据展示到前端呢？为啥还要后端。  
设想一下，你特别喜欢吃鸡腿，那么别人不可能直接给你一只鸡吧，总需要厨师进行加工吧。  
后端就是那个厨师，它把数据进行加工、处理、分类后放到你的桌子上。所以，暂时可以这样理解：**后端就是数据的中转站。**
说了这么多，赶快用上数据库吧！  
问题来了，有很多种数据库，我们用哪种？有关系型数据库（即SQL数据库），还有非关系型数据库（即NoSQL数据库）。  
关系型数据库里又有MySQL,Oracle，SQLServer等等。  
非关系型数据库里又有Redis等。  
可是我只想要一个能存取数据的玩意儿而已啊，这些里面随便用一个不就好了吗，简单方便就好，我又不是想做DB工程师。  
既然你是这种需求的话，那么一定要推荐你这个数据库:SQLite.这个数据库python自带，简单方便，新手需要的数据库增删改查的功能它都有。  
选好了数据库，是不是迫不及待想要开始了！  
别急，还有最后一个准备工作：SQLAlchemy.这是个什么玩意儿呢，看它名字，它叫SQL炼金术，它对数据库做了什么呢？  
它把数据库变成我们更容易理解的样子。假设我们数据库里有个表叫users： 
 
| id  | name     | age |
| --- | -------- | --- |
| 1   | xiaoming |  18 |
| 2   | xiaohua  |  19 |


按照关系型数据库的理解，这个表里有两条数据，一条数据是[1,"xiaoming",18]，一条数据是[2,"xiaohua",19]。通过每条数据里的子数据对应的位置，知道每个子数据表示的是什么意义。  
但是，数据是足够好理解了，可是用来增删改查的SQL语言却有些不那么直观。比如创建这个表的SQL语句：  
```sql
create table users(
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(40) NOT NULL,
age INT);
```  

比如查询这个表里的年龄为18的那条数据：
```sql
select * from users where age=18;
```  


不是太贴近人类语言的感觉，更像是给机器发布的一条命令。
SQLAlchemy就闪亮登场。它把数据库里的表变成一个对象，也可以说变成了一个模型,把SQL查询语言用更高级的操作对象的方法来封装。  
把users这个表变成对象User:  


```python
class User(db.Model):  
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	age = db.Column(db.Interger)
	def __repr__(self):	//这个方法就是当你调用User的实例（比如xiaoming）的时候，它会返回<Role "xiaoming">
		return '<Role %r>' % self.name 
   
```  

为表里添加数据也很优雅：

```python
xiaoming = User(id=1, name="xiaoming", age=18)
xiaohua = User(id=1, name="xiaohua", age=19)
```

小明和小华都是User类的一个实例。是的，这很面向对象。  
查询也同样优雅：

```python
User.query.filter_by(age=18).all()
```  

调用User这个类的query方法，来查询。以age=18为过滤器，来筛选出来年龄等于18的人，all()这个方法获得满足条件的所有User.

3.连接数据库  

好的，啰嗦了半天，终于能够连接数据库了。  
首先配置一下数据库：  
```python
from flask.ext.sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))  
app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] =\  
'sqlite:///' + os.path.join(basedir, 'data.sqlite')   app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  
db = SQLAlchemy(app)  
```  

解释一下，```basedir```是这个项目的根路径，app为实例化的Flask项目，就像我们之前做的那样。下面的两个```app.config```分别是配置数据库的地址，配置每次请求结束后都自动提交数据库中的变动。最后一句是实例化SQLAlchemy，并且连上这个项目。也就是说，db就是这个项目的数据库（被SQLAlchemy转变成的对象）


