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
言归正传，怎样返回json数据呢？想必同学们都应该看懂了，路由函数里return什么值，我们访问这个路由就会得到什么值。所以我们就把```<h1>Hello World!</h1>```改成那段json数据就行了。对了，那么路由就不应该是根路由'/'了，而是我们刚刚举的例子里的'/users'。flask里有一个包叫json，负责把python的dict，list数据与json格式的数据互相转换。于是整个代码是这个样子:
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
把users这个表变成对象User：  

```python
class User(db.Model):  
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	age = db.Column(db.Integer)
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
from flask import Flask
import os
from flask.ext.sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))  
app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  
db = SQLAlchemy(app)  
```  

解释一下，```basedir```是这个项目的根路径，app为实例化的Flask项目，就像我们之前做的那样。下面的两个```app.config```分别是配置数据库的地址，配置每次请求结束后都自动提交数据库中的变动。最后一句是实例化SQLAlchemy，并且连上这个项目。也就是说，db就是这个项目的数据库被SQLAlchemy转变成的对象.
再加上前面的路由函数，我们的程序是这样：
```python
//下面这段程序写在app.py这个文件里
from flask import Flask,json
import os
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
manager = Manager(app)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    age = db.Column(db.Integer)
    def __repr__(self):
        return '<User %r>' % self.name
@app.route('/users')
def users():  
    respJson=json.dumps(User.query.all())
    return respJson

if __name__=='__main__':
    manager.run()
```
我们这个程序里面好像多了一个刚刚没有提到的东西：manager。这玩意是在我们的app外面套了层套子，让我们的app变得更方便调试，并且多了一个用shell调试的功能。你没有看错，不需要用网页来调试，我们可以直接用shell来调试。  
如果你直接开始运行这段程序，那么恭喜你，会报错。为啥呢？因为我们的数据库还没有成功创建users这个表。估计你要问了，我们不是已经有了User这个类了吗，他不就是users这个表的高级封装吗（即将表变为对象）？是的，没错，它只是个高级抽象，你还需要让他真正变成数据库里的表啊。

于是我们要打开shell,把这个表创建了。  

```shell
python app.py shell  
>>> from app import db  
>>> db.create_all()  
```  

好的，这次终于大功告成了。

现在按control+C退出shell,然后运行app.py。

现在你访问localhost:5000/users，你会惊奇的发现，有个中括号。纳尼，怎么只有一个中括号，数据呢？？？User里不是应该有xiaoming和xiaohua的吗？别急，你还没添加呢。

还是打开shell,(你可以先把正在跑着的app.py程序control+c退出掉，也可以刚刚就把app.py用下面这个命令在后台运行```python app.py runserver &```)

```shell
python app.py shell
>>> from app import db
>>> from app import User
>>> xiaoming = User(id=1, name="xiaoming", age=18)
>>> xiaohua = User(id=2, name="xiaohua", age=19)
>>> db.session.add(xiaoming)
>>> db.session.add(xiaohua)
>>> db.session.commit()
```

好的，在上面的代码里面，我们创建了xiaoming和xiaohua这两个数据，然后把这两个数据通过会话(session)添加到db里，别忘了，最后一定要commit()，因为这样表示你确认要提交这两个add操作。如果你用过git的话，这个和git add 后一定要git commit 是一个道理。

这个时候你再运行app.py这个程序，再去访问localhost:5000/users，你满心欢喜的以为小明和小华会跑出来见你的时候，你发现报了个错，囧：

```python
TypeError: <User u'xiaoming'> is not JSON serializable
```

错误说：<Role u'xiaoming'>这玩意儿不能变成json格式。对哦，json这个库只能把dict或者list变成json，<Role u'xiaoming'>是个实例，咦，话说为什么会返回这个实例呢？我们看User.query.all()返回了什么东西.同样的，我们在shell里这么干。现在知道Manager的好处了吧，测试起来很方便。

```shell
python app.py shell
>>> from app import User
>>> User.query.all()
[<User u'xiaoming'>, <User u'xiaohua'>]
```
返回了一个list，里面装着两个实例。我们需要的是这两个实例的属性：id,name,age。所以呢，就在这个类里写个方法，返回它的这些属性。


```python
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    age = db.Column(db.Integer)
    def __repr__(self):
        return '<User %r>'%self.name
    def to_json(self):
        return {"id": self.id,
                    "name": self.name,
                    "age": self.age}
```    

然后改一下路由函数返回的值：

```python
@app.route('/users')
def users():  
    users = User.query.all()
    return json.dumps([user.to_json() for user in users])
```    

注意一下return的东西，由于users里的元素都是User实例，所以对每一个实例调用to_json()的方法，返回一串dict,然后把这两个dict组成的list通过json.dumps变成了json。

此时你在浏览器中输入localhost:5000/users，你会发现，小明小华终于回来了！

现在我们和小明小华这两兄弟说拜拜了，我们需要的是博客文章，所以要一个新的表，对于SQLAlchemy来说也就是一个新的模型：Post。

类似User，我们搞一个Post出来：
```python
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    text = db.Column(db.Text)
    def __repr__(self):
        return '<Post %r>'%self.title
    def to_json(self):
        return {"id": self.id,
                    "title": self.title,
                    "text": self.text}
```  

同样的，先要通过shell,创建posts这个表，具体方法回头参考一下users是怎么创建的。  

可是，怎样给posts里添加数据呢？兄弟，一样类似users不就好了嘛。可是，这样是不是太不优雅了，而且我是要用户在浏览器那里输入博客文章，自动传到数据库里去呀，而不是总是拿着shell往数据库里添加数据呀！！！

好的好的，这样就需要前端啦！那么我们来进入React的前端世界吧！  
后端完整代码看这个[commit](https://github.com/zhangdistephen/dva-flask-blog/commit/9b2390c9c13346da4cc2b03cf576ce42b424cf38#diff-3f41e546893dc64b71aaacad12cad815)

##前端

###博客数据展示

说起前端，就是三剑客html,css,js。那么直接用这三个东西写前端不就好了嘛，为什么要搞个react呢。

不提性能这些东西，因为react能让你的代码更加清晰，它规定了一些条条框框，你按照这个条条框框写就能让你的代码更容易维护。而且，我们说的react并不是简简单单的react框架，而是一整个react生态圈，包括react-router,redux,react-redux,redux-saga。看起来东西很多，但其实只需要了解他们的思想，然后把它们都当成工具来用就好了。除了这些，还要知道npm,一个下载我们需要的包的东西，还要知道webpack，一个帮我们打包代码的东西，还要知道babel，一个帮我们翻译我们超前的js代码的东西。

我的天，前端这么多东西，什么时候才可以编程啊。

不要害怕，这些东西目前我们都当成工具来用就行。甚至直接有一个把这些工具全部封装起来的一个更方便的工具：dva。没错，就是守望先锋里的那个dva，就冲这个名字就要star一下这个项目了。

好的，废话不多说，我们直接开始吧。

首先，把npm下下来，怎么下？看[廖雪峰老师的教程](http://www.liaoxuefeng.com/wiki/001434446689867b27157e896e74d51a89c25cc8b43bdb3000/00143450141843488beddae2a1044cab5acb5125baf0882000)

有了npm，再把dva下下来，只需要在shell里输入  

```SHELL
npm install dva-cli -g
```
有了dva，就能自动构建一个我们需要的环境啦，在shell里输入  

```shell
dva new dva-flask-blog
```

等他创建好，你应该就有了一大堆文件夹和文件，解释一下各个文件夹是干嘛的，mock不用管，是用来做虚拟数据的，我们不需要。node_modules就是我们存放npm下载下来的依赖的地方。public里面放的是index.html，这个不需要解释了吧。最关键的是src文件夹，里面很多层东西，这个我们等会细讲。下面这些点开头的文件，就不细讲。注意一下package.json这个文件，里面是npm的配置信息。比如你安装了哪些库呀，

好的，重点来看看src里的文件。

为什么要划分这么多文件夹？？？为了让项目的层次分明，每一个文件夹里的文件都有着类似的功能。
  
* assets：存放静态资源。比如图片。
* components：存放react的UI组件。（啥叫组件？等会说）
* models：存放数据模型。（怎么感觉好像数据库？等会说）
* routes：存放路由组件。（路由我知道，后端里刚刚讲了这个概念！聪明，但react的路由稍微有一点区别哦，而且它也是个react组件哦）
* services：用来存放和后端进行数据交互的函数的文件。
* utils：一些工具函数咯。
* router.js：吧routes里的路由组件拿进来，并且给每个路由组件分配一个路由。（就是你进入某个路由，你就能看到对应的那个路由组件啦。）
* index.js:引入models和routes。

好的，看完了这些东西，是不是一头雾水，怎么这么一大堆文件夹，这么堆概念。其实，重要的概念就两个：**组件**，**模型**。

先来看看什么是**组件**：


你肯定见过```<p>我很酷</p>```这个东西,这个不就是个文本标签嘛，html里的东西。可是，你有没有想过，我们可不可以自己创造一个html标签？开玩笑的吧，这应该是研究html的协会做的事吧。不过实际上，你的确可以创造一个html标签，只不过是把原有的html标签组合一下，形成一个新的标签。这个标签，在react里，我们就称他为组件。比如你定义一个组件```<Ku></Ku>```这个组件等同于```<p>我很酷</p>```ok，那么在你需要显示```<p>我很酷</p>```的地方，你只需要放一个```<Ku></Ku>```就行了。

react里的组件还有生命周期，状态，属性这些东西。不过暂时先不用了解，代码写到那里的时候我们再说。

说完了组件，我们说说**模型**。其实完全可以把模型理解为一个全局对象。模型有自己的名字(namespace),有自己的状态(state),有自己的方法，同步的方法（reducers），异步的方法(effects)。

为了更好的理解组件和模型，我们来设想一个情况。

我写了三篇博客文章，但在首页我只想展示一篇文章。那么文章（posts)就是我们的**模型**。它有两个状态，一个状态是```data:[{id:1,text:"post1"},{id:2,text:"post2"},{id:3,text:"post3"}]```,另一个状态是```currentDisplay:{id:1,text:"post1"}```所以如果我们想把首页的展示文章换一篇，那么只需要修改```currentDisplay```这个状态就行。

假如我们在首页放一个div容器，这个div里装的是文章，文章背景要黑色，字要白色，鼠标点击这个div，就要换一篇文章。那么，我们就可以把这个div容器做成一个**UI组件**。伪代码是

```html
<Post />  
等于 
<div beiDianJile={changeDisplay}  background='black'>
	<p>{posts.currentDisplay.text}</p>
</div>
```

假如你还希望在首页看到```欢迎您，Master```这几个字，你甚至可以把这几个字也做成一个**UI组件**（如果你很闲的话）

```html
<Welcome />  
等于 
<p>欢迎您，Master</p>
```

你在某个路由看到的所有东西的集合，就是**路由组件**。假如首页(即根路由'/')只出现一篇文章和一个欢迎您的话，那么你的**路由组件**就可以这么写

```html
<Index />  
等于 
<div>
	<Welcome />
	<Post />
</div>	
```  
**注意：这里必须在```<Welcome />和<Post />```外面套一层div，因为react规定了一个组件只能等于一个标签。如果不加div，就是让```<Index /> ```等于两个标签了。**

现在对于这些东西不是那么迷糊了吧？那么我们开始写代码吧。

代码最好从models里写起，比如我们的博客需要展示我们的文章，那么先搞一个名为posts的model出来。

我个人认为models主要有4个要点:

1.状态（state)

2.异步请求（effects)

3.同步请求（reducers）

4.监测用户和浏览器行为（subscriptions）

状态比较好理解，在这个角度可以把模型理解为存储状态的东西。

异步请求主要是与服务器进行交互，从服务器这里拿数据。

同步请求主要是把服务器的数据经过筛选、判断后，存到状态里。

监测用户的行为主要是监测用户按了哪些键之类的行为。监测浏览器行为主要是监测目前的路由是什么，针对不同的路由，执行不同的行为。

```JavaScript
import * as postsService from '../services/posts'
export default{
  namespace:'posts',
  state:{
    data:[],
    currentDisplay:{}
  },
  effects: {
    *fetch({},{call,put}){
      const {data}=yield call(postsService.fetchPosts)
      yield put({
        type: 'save', payload: {
          data,
          currentDisplay:data[0]
        }
      })
    }
  },
  reducers:{
    save(state,{payload}){
      return{...state,...payload}
    }
  },
  subscriptions:{
    setup({dispatch}){
      dispatch({type:'fetch'})
    }
  }
}
```

我们这里的第一句就让人有些搞不明白了，services是什么东西？前面我们讲过，services是用来存放和后端进行数据交互的函数的文件，而models里需要进行异步请求，所以就从services里引入这些函数。你可能要问，为什么不把这些函数直接放在models里呢？这样的话，models看起来就会很杂，有很多和服务器交互的函数，有很多维护自己状态的函数。所以不如把和服务器交互的函数放在services里，这样结构更清晰。

后面定义了posts的命名空间（也就是给这个模型里的effects和reducers加了个前缀，确保不会和其他模型的同名函数重复），定义了两个状态,一个是所有的文章```data```，另一个是首页显示的文章```currentDisplay```。

effects里装的是一些异步请求，目前只有一个，也就是```*fetch```, 前面的星号是什么意思呢？这表示这个函数是generator，generator的定义请看阮一峰老师的[es6教程：Generator函数](http://es6.ruanyifeng.com/#docs/generator)。简单来说，就是在函数执行的过程中，遇到yield，就停下来，等到yield的东西执行完了，把返回的值拿到手，然后继续执行。我们这里的```fetch```很简单，```call```了一个services里请求服务器数据的函数，将它返回的对象里的```data```装入我们的常量```data```里。注意，这里用了解构赋值，具体请看阮一峰老师的[es6教程：变量的解构赋值](http://es6.ruanyifeng.com/#docs/destructuring)。简单来说就是假如有这么一个对象```post={data:"haha",title:"xixi"}```,执行```const {data}=post```，得到的```data```就是```haha```，相当于执行了```const data=post.data```。

然后执行了```yield put```,相当于发起一个行为（action），这个action就是下面reducers里的save，作用是把数据存到posts这个模型的状态里。

最后的subscriptions里的setup表示当用户进入我们的前端页面的时候，就执行。我们的这个函数发起了一个名叫fetch的action，也就是我们effects里的fetch。这里的这个dispatch和刚刚的put是一个意思，都是发起行为。

先写models，是为了对数据有了一个完整的印象，通过写models，我们了解了数据是通过调用services里的和服务器交互的异步函数拿到的，然后通过同步请求将数据存到模型的状态里。然后要数据的时间不是随随便便的，而是进入我们的前端页面的时候。

接下来写services里的函数，我们要怎么问服务器要数据呢？

```JavaScript
import request from '../utils/request'
export function fetchPosts(){
  return request(`/api/posts`)
}
```
没错，就这么几行。就是用了request这个函数问服务器要数据。那么request又是何方神圣呢？你甚至可以不用了解，而是把这个当成一个底层的工具来使用。因为要数据的函数内部都大同小异，完全可以当成工具来用。这里还是展示一下吧：

```javascript
import fetch from 'dva/fetch';

function parseJSON(response) {
  return response.json();
}

function checkStatus(response) {
  if (response.status >= 200 && response.status < 300) {
    return response;
  }

  const error = new Error(response.statusText);
  error.response = response;
  throw error;
}

/**
 * Requests a URL, returning a promise.
 *
 * @param  {string} url       The URL we want to request
 * @param  {object} [options] The options we want to pass to "fetch"
 * @return {object}           An object containing either "data" or "err"
 */
export default function request(url, options) {
  return fetch(url, options)
    .then(checkStatus)
    .then(parseJSON)
    .then(data => ({ data }))
    .catch(err => ({ err }));
}
```

内部是怎么执行的对初学者来说不重要，你需要了解的就是这个函数如果请求到数据了，就会返回数据，没请求到数据，就会返回错误。


有了数据，那么我们来看怎么展现。说起展现，那么肯定是和UI有关了，在react里，有个非常好的UI库，叫ant design，简称antd，是阿里巴巴公司的UI库。所以我们先把这个库装了。```npm install antd --save --registry=https://registry.npm.taobao.org```

然后由于antd的组件导入有些小问题，所以我们装个阿里出的补丁，```npm i babel-plugin-import --save-dev --registry=https://registry.npm.taobao.org```

然后在```.roadhogrc```里配置一下，

```
{
  "entry": "src/index.js",
  "env": {
    "development": {
      "extraBabelPlugins": [
        "dva-hmr",
        "transform-runtime",
        ["import", { "libraryName": "antd", "style": "css" }]
      ]
    },
    "production": {
      "extraBabelPlugins": [
        "transform-runtime"
      ]
    }
  },
  "proxy": {
    "/api": {
      "target": "http://localhost:5000/",
      "changeOrigin": true,
      "pathRewrite": { "^/api" : "" }
    }
  }
}
```

现在可以使用这个强大的UI库了。



既然提到了前端的展示，那么哪个页面展示哪些东西呢？我们在routers这个文件里解决。这里我想要一个展示一篇文章的页面，一个展示所有文章的缩略的页面。展示单篇文章的页面我们放在```/```这个路由下，展示所有文章缩略的页面我们放在```/posts```这个路由下。

```javascript
import React from 'react';
import { Router, Route } from 'dva/router';
import Posts from './routes/Posts'
import Post from './routes/Post'
function RouterConfig({ history }) {
  return (
    <Router history={history}>
      <Route path="/" component={Posts} />
      <Route path="/post" component={Post}/>
    </Router>
  );
}

export default RouterConfig;
```
接下来我们去写各个页面里的组件，也就是在routes这个文件夹里创建Posts.js和Post.js这两个文件。顾名思义，一个代表所有文章的页面，一个代表单篇文章的页面。

来看看单篇文章页面```/```

```javascript
import {connect} from 'dva'
import {Layout,Menu} from 'antd'
import {Link} from 'dva/router'
const Header=Layout.Header;
function Post({loading,currentDisplay}){
  if(loading){
    return <h1>loading</h1>
  }
  else {
    return (
      <Layout>
        <Header>
          <Menu
            theme="dark"
            mode="horizontal"
            defaultSelectedKeys={['1']}
            style={{ lineHeight: '64px' }}
          >
            <Menu.Item key="1"><Link to="/">文章</Link></Menu.Item>
            <Menu.Item key="2"><Link to="/posts">文章库</Link></Menu.Item>
          </Menu>
        </Header>
        <p>标题:{currentDisplay.title}</p>
        <p>内容:{currentDisplay.text}</p>

      </Layout>
    )
  }
}
function mapStateToProps(state){
  const {currentDisplay} = state.posts;
  return{
    loading: state.loading.models.posts,
    currentDisplay
  }
}
export default connect(mapStateToProps)(Post)
```

```function Post```是我们的组件，它接受两个参数，分别是loading和currentDisplay，currentDisplay之前讲了，是posts这个模型里的一个状态（state)。loading是loading这个模型提供的，如果posts模型正在进行异步请求，那么其值为true，如果没有进行异步请求，那么其值为true。

等等，loading这个模型哪来的，我们刚刚不是只创建了posts模型吗？loading这个模型是dva的一个插件提供的，当我们的模型在请求数据的时候，就会更新loading这个状态，以免我们手动更新loading状态。你可能又要问了，为什么要管loading状态呢？你想，如果你正在请求数据，数据还没拿到，但是页面已经更新了，但是没有数据，所以就会出问题吧，所以我们需要知道数据到底什么时候拿到，然后再更新页面，这就是loading状态的作用。要用这个插件的话，得先用npm下载，```npm i dva-loading --save```
然后还要更新下`src/index.js`。

```JavaScript
import dva from 'dva';
import './index.css';
import createLoading from 'dva-loading';//更新的部分

const app = dva();

app.use(createLoading());//更新的部分

app.model(require('./models/posts'));

app.router(require('./router'));

app.start('#root');
```

回到我们的`Post`组件，当正在异步请求数据的时候，返回`<h1>loading</h1>`，当请求完数据时，返回我们要展示的东西，一个是导航栏`Header`,（里面有个`Link`,可以认为是`html里的<a>标签`的react版本），一个是单篇文章的数据`currentDisplay.title,currentDisplay.text`。

下面有个函数`mapStateToProps`和`connect`可能让人有些疑惑，说白了，就是把我们模型里的状态，作为属性传给我们的组件。具体可看react-redux。

再看所有文章的缩略页面`/posts`

```javascript
import {connect} from 'dva'
import {Layout,Menu} from 'antd'
import {Link} from 'dva/router'
const Header=Layout.Header;
function Posts({posts,loading}){
  if(loading){
    return <h1>loading</h1>
  }
  else {
    return (

      <Layout>
        <Header>
          <Menu
            theme="dark"
            mode="horizontal"
            defaultSelectedKeys={['2']}
            style={{ lineHeight: '64px' }}
          >
            <Menu.Item key="1"><Link to="/">文章</Link></Menu.Item>
            <Menu.Item key="2"><Link to="/posts">文章库</Link></Menu.Item>
          </Menu>
        </Header>
        {posts.map((post, index)=>(
          <p key={index}>标题:{post.title}</p>
        ))}

      </Layout>
    )
  }
}
function mapStateToProps(state){
  const {data:posts} = state.posts;
  return{
    posts,
    loading: state.loading.models.posts,
  }
}
export default connect(mapStateToProps)(Posts)

```

这两个页面几乎一模一样。所以要想个办法把相同的部分写一次就够了。究其原因，是因为这两个页面都有导航栏这个部分，所以这个部分写了两次，所以得把这个导航栏抽出来。代码如下：

```javascript
// routes/posts.js
import {connect} from 'dva'
import MainLayout from '../components/MainLayout'
function Posts({posts,loading}){
  if(loading){
    return <h1>loading</h1>
  }
  else {
    return (

      <MainLayout selectedKey="2">
        {posts.map((post, index)=>(
          <p key={index}>标题:{post.title}</p>
        ))}

      </MainLayout>
    )
  }
}
function mapStateToProps(state){
  const {data:posts} = state.posts;
  return{
    posts,
    loading: state.loading.models.posts,
  }
}
export default connect(mapStateToProps)(Posts)
```

```javascript
// routes/Post.js 
import {connect} from 'dva'
import MainLayout from '../components/MainLayout'
function Post({loading,currentDisplay}){
  if(loading){
    return <h1>loading</h1>
  }
  else {
    return (
     <MainLayout selectedKey="1">
        <p>标题:{currentDisplay.title}</p>
        <p>内容:{currentDisplay.text}</p>

     </MainLayout>
    )
  }
}
function mapStateToProps(state){
  const {currentDisplay} = state.posts;
  return{
    loading: state.loading.models.posts,
    currentDisplay
  }
}
export default connect(mapStateToProps)(Post)
```

```javascript
// components/MainLayout.js
import {Layout,Menu} from 'antd'
import {Link} from 'dva/router'
const Header=Layout.Header;
export default function MainLayout({selectedKey,children}) {
  return (

    <Layout>
      <Header>
        <Menu
          theme="dark"
          mode="horizontal"
          defaultSelectedKeys={[selectedKey]}
          style={{ lineHeight: '64px' }}
        >
          <Menu.Item key="1"><Link to="/">文章</Link></Menu.Item>
          <Menu.Item key="2"><Link to="/posts">文章库</Link></Menu.Item>
        </Menu>
      </Header>
      {children}

    </Layout>
  )
}
```

到此，前端的展示已经做的差不多了，效果如下图：
![post](http://oh8c4fk40.bkt.clouddn.com/1CC30482-C02D-4358-9D54-EE8CA8A6150E.png)
![posts](http://oh8c4fk40.bkt.clouddn.com/D73E74BF-03CD-416B-A666-147025C540D9.png)

里面的文章数据是我用shell向数据库添加的，前面有讲过怎么添加。

有的同学肯定觉得这也太丑了吧，因为没有写css的缘故，但是我们的整体架构已经搭好了，css相对来说比较容易写，先不急着写，最后统一写。

接下来有个问题是，怎么把前端用户输入的数据传入数据库，因为我们需要用户在前端写好博客，然后我们的程序把博客送到数据库里存储。而不是我们每次写博客都用shell添加。

###博客数据添加
有了前面的经验，这次我们如法炮制。

首先写models，由于都是posts这个model，所以不用另写一个model，就在这个model里添加东西。

