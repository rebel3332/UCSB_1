# UCSB_1
Данная работа выполнена для **Уральского Центра Систем Безопасности**

Проект реализует Web форму для ввода 2-х текстовых значений.

Реализованы проверки:
* что оба поля не пустые.
* второе поле является номером телефона
Если все проверки пройдены, данные заносятся в таблицу

**Для корректной работы требуется**:
* Иметь у себя сервер PostgreSQL
* Создать на нем тестовую базу
* Создать в ней тестовую таблицу с двумя текстовыми полями text1 и text2
* Зайти в файл config.py проекта и изменить настройки на актуальные

**Применяемые технологии:**
* Python
* PostgreSQL
* flask
* flask_wtf
* pyparsing
* wtforms
* psycopg2
