# Django后端

## 安装依赖

``` bash
pip install -r requirements.txt
```

## 使用

需要在settings中修改数据库的配置信息

配置你自己的端口号等信息，然后，创建数据库迁移

 ``` bash
    python manage.py makemigrations
    python manage.py migrate
```
获取[图床密钥](https://www.picgo.net/api-v1)，填入`settings.py`中的`PICGO_SECRET_KEY`中

## 原作者个人博客
[回锅炒辣椒的个人博客](https://www.xsblog.site/)

## 功能
用户登录

用户注册

主页帖子

帖子详情

用户主页

用户评论

用户更新个人信息

用户帖子管理

未完待续
