Итоговый проект по автоматизации тестирования.
Автоматизированное тестирование интерфейса в личном кабинете от заказчика Ростелеком Информационные Технологии (https://b2c.passport.rt.ru/).

-Тест-Кейсы и Баг-репорты доступны по ссылке: https://docs.google.com/spreadsheets/d/1oOZBRTWLLIYFMBdDQtqnugRCUOEW6tf0-USikoVl8Jk/edit?usp=sharing

-в файле base_page.py находится конструктор webdriver и общие для всех тестируемых страниц методы

-в файле My_pages находятся методы проверок формы авторизации, восстановления пароля, регистрации

-в файле main.py находятся тесты. Все тесты помечены номером, совпадающим с номером тест-кейса

-в файле conftest.py находится фикстура с функцией открытия и закрытия браузера

-в файле settings.py находятся методы и переменные для параметризации тестов

-в файле requirements.py описаны используемые библиотеки.
