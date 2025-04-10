![image](../assets/logo_with_text.svg)

![PyPI](https://img.shields.io/pypi/v/ptnad)

# PT NAD Client

**Документация**: <a href="https://reversenant/test-nad">https://reversenant/test-nad</a>

**Исходный код**: <a href="https://github.com/reversenant/test-nad">https://github.com/reversenant/test-nad</a>

---

Библиотека на Python для взаимодействия с API PT NAD.

## 🚀 Установка
```python
pip install ptnad-client
```

### 📖 Пример использования
```python
from ptnad import PTNADClient

client = PTNADClient("https://1.3.3.7", verify_ssl=False)
client.set_auth(username="user", password="pass")
# client.set_auth(auth_type="sso", username="user", password="pass", client_id="ptnad", client_secret="11111111-abcd-asdf-12334-0123456789ab", sso_url="https://siem.example.local:3334")
client.login()

query = "SELECT src.ip, dst.ip, proto FROM flow WHERE end > 2025.02.25 and end < 2025.02.26 LIMIT 10"
result = client.bql.execute(query)
print(f"Результаты: {result}")
```
![image](../assets/pic_left.svg)
## ✅ Возможности

🔐 Аутентификация  
- Локальная аутентификация  
- IAM (SSO) аутентификация  

📊 BQL-запросы  
- Выполнение запросов  

📡 Мониторинг  
- Получение статуса системы  
- Управление триггерами  

🛡️ Сигнатуры  
- Получение классов  
- Получение правил (всех/конкретных)  
- Применение/откат изменений  

📋 Реплисты  
- Создание/редактирование базовых и динамических реплистов  
- Получение информации о реплистах  

### 🛠️ Планируемые функции  
- Документация  
- Управление источниками  
- Управление хостами  
- Управление группами  

## 🧑‍💻 Вклад в проект

Хотите внести свой вклад? Ознакомьтесь с материалами:

- [📄 Гайд для участников](CONTRIBUTING.md)

Мы открыты для любых идей, предложений и улучшений!

---

### 📜 Лицензия  
Этот проект лицензирован под MIT License – подробности см. в файле LICENSE.
