参考[HelloDjango - Django博客教程（第二版）](https://www.zmrenwu.com/courses/hellodjango-blog-tutorial/materials/59/)

跳过三个部署教程和 HTTPS 证书，最后再整
进入最后的测试环节前回到部署环节，里面对设置进行拆分为开发板和生产版

## 环境

- python 3.6.4
- django 2.2.3

```bash
django-admin startproject blogDjango  # 创建工程
python manage.py runserver  # 启动 web 服务

python manage.py makemigrations # 检查模型修改
python manage.py migrate  # 数据迁移

python manage.py createsuperuser  # 创建用户

python -m scripts.fake  # 生成测试数据

python manage.py test # 运行测试

python manage.py collectstatic # 收集静态文件
gunicorn blogproject.wsgi -w 2 -k gthread -b 127.0.0.1:8000 # 启动 gunicorn
```