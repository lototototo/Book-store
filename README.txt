У вас должен быть установлен Python версии 3.8 и выше.
Установить его можно по ссылке https://www.python.org

1. Сделайте git clone репозитория
```bash
git clone https://github.com/lototototo/Book-store
```
2. Откройте проект в PyCharm или другом редакторе.

3. Установите зависимости из файла requirements.txt
```bash
pip install -r requirements.txt
```
4. Запустите проект
```bash
python run.py
```

5. Ручки:
   5.1. Регистрация -- http://localhost:5466/register
   пример курла
   ```bash
    curl -X POST http://localhost:5466/register -H "Content-Type: application/json" -d '{
        "username": "test1user",
        "email": "t2es2t@example.com",
        "password": "securepassword",
        "confirm_password": "securepassword"
    }'
    ```

    5.2. Логин -- http://127.0.0.1:5466/login