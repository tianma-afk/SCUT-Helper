如何启动后端？



工作目录在/backend

第一步、创建虚拟环境

```
python -m venv venv
```



第二步、启动虚拟环境

```
venv\Scripts\activate
```



第四步、下载依赖

```
pip install -r requirements.txt
```



第五步、初始化数据库

```
psql -U postgres -f create_database.sql
```



第六步、运行

```
python main.py
```

