# Eco-Bot

Телеграм-бот для помощи с законами и вопросами, связанными с экологией.

## Ссылка на проект

[GitHub проекта Eco-Bot](https://github.com/CallofAbyss/eco-bot?utm_source=chatgpt.com)

---

# Системные требования

* ОС: Windows 10/11, Linux или macOS
* Процессор: Intel Core i3 / AMD Ryzen 3 или аналогичный
* Оперативная память: от 4 ГБ
* Свободное место на диске: ~200 МБ
* Стабильное интернет-соединение
* Установленный Python 3.10 или новее

---

# Инструкция по установке и запуску

## 1. Установка Python

1. Перейдите на официальный сайт Python:

[Python.org](https://www.python.org/downloads/?utm_source=chatgpt.com)

2. Скачайте последнюю версию Python.
3. Во время установки обязательно поставьте галочку:

```text id="h12aa"
Add Python to PATH
```
4. Завершите установку.

---

## 2. Скачивание проекта

1. Создайте отдельную папку для проекта.
2. Перейдите на GitHub проекта:

[Eco-Bot GitHub](https://github.com/CallofAbyss/eco-bot?utm_source=chatgpt.com)

3. Нажмите кнопку:

```text id="j22kl"
Code → Download ZIP
```

4. Распакуйте архив в созданную папку.

---

## 3. Установка библиотек

1. Откройте папку проекта.
2. Нажмите правой кнопкой мыши внутри папки.
3. Выберите:

```text id="f88lp"
Открыть в терминале
```

4. Установите необходимые библиотеки командой:

```bash id="u82js"
pip install python-telegram-bot==20.7 python-dotenv==1.0.0 requests==2.31.0
```

Либо используйте файл requirements.txt:

```bash id="s11qq"
pip install -r requirements.txt
```

---

# Используемые библиотеки

* python-telegram-bot==20.7
* python-dotenv==1.0.0
* requests==2.31.0

---

# 4. Запуск бота

1. После установки библиотек запустите файл:

```python id="r29dn"
bot.py
```

2. Если всё установлено правильно, бот начнёт работу.

---

# 5. Работа с Telegram

1. Установите Telegram:

[Telegram Desktop](https://desktop.telegram.org/?utm_source=chatgpt.com)

или мобильную версию:

[Telegram Mobile](https://telegram.org/apps?utm_source=chatgpt.com)

2. Войдите в свой аккаунт Telegram.
3. В поиске Telegram введите:

```text id="n77ka"
@Ecoprav_bot
```

4. Откройте бота и нажмите:

```text id="v31zl"
/start
```

5. После запуска можно задавать вопросы, связанные с экологическим законодательством.

---

# Возможные ошибки

## Python не найден

Если появляется ошибка:

```text id="q44op"
Python is not recognized
```

значит Python был установлен без добавления в PATH.

Решение:

* переустановить Python
* включить пункт:

```text id="m61er"
Add Python to PATH
```

---

## Библиотеки не устанавливаются

Попробуйте обновить pip:

```bash id="w91tx"
python -m pip install --upgrade pip
```

После этого повторите установку библиотек.
