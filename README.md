# dva-flask-blog
一个博客模板，前端使用dva框架（封装了react，redux，redux-saga，react-redux，react-router等，个人感觉这框架是react最佳实践，让你的前端代码写起来更轻松，更易维护），后端使用python的轻量级web框架flask（连接数据库，为前端提供RESTful的api接口）。
##后端
后端有两个作用：
连接数据库，从数据库中拿出前端需要展现的数据。
提供API，便于前端调用。说白了，就是提供数据。

1.连接数据库：
先谈谈怎样构造一个flask的后端。
