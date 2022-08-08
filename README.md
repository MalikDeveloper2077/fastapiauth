# fastapiauth
```
pip3 install -r requirements.txt
```

В корневой папке:  
```
uvicorn app.main:app
``` 
  
В alembic.ini настроить БД или использовать дефолтный URL.  
```
sqlalchemy.url = ...
```  
  
Как и в config.py  
```
DATABASE_URL = ...
```
