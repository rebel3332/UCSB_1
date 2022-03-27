from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from pyparsing import Regex
from wtforms import StringField
from wtforms.validators import ValidationError, Regexp, DataRequired
# import os
import psycopg2
from config import *

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY


# Описание класса для формы запроса
class RegForm(FlaskForm):
    """Класс для формы запроса на сайте
    
    Предусмотрены следующие валидаторы:
    1. проверка что оба поля не пустые
    2. Допустимые форматы для телефона: xxxxx, xxxxxx, xxxxxxx, +7xxxxxxxxxx, +7(xxx)xxxxxxx, +7(xxxx)xxxxxx, +7(xxxxx)xxxxx
    """    
    
    phohe_message = """
    Допустимые форматы: xxxxx, xxxxxx, xxxxxxx, +7xxxxxxxxxx, +7(xxx)xxxxxxx, +7(xxxx)xxxxxx, +7(xxxxx)xxxxx
    """
    phone_re = r'^(((\+7|7|8)[0-9]{10})|((\+7|7|8)\([0-9]{3}\)[0-9]{7})|((\+7|7|8)\([0-9]{4}\)[0-9]{6})|((\+7|7|8)\([0-9]{5}\)[0-9]{5})|([1-9][0-9]{4,6}))$'
    
    text1 = StringField('Текстовое поле 1', validators=[DataRequired()])
    text2 = StringField(label='телефон', validators=[Regexp(regex=phone_re, 
                                                            message=phohe_message),
                                                     DataRequired()])
    
    
def insert_record(text1:str, text2:str) -> None:
    """Процедура добавляет запись в таблицу

    Args:
        text1 (str): текст из текстового поля 1
        text2 (str): телефон
    """
    
    try:
        # Подключение к базе данных
        connection = psycopg2.connect(
            host=host_psql,
            port=port_psql,
            user=user,
            password=password,
            database=db_name
        )
        print(f'[INFO] PostgreSQL connection open')
        # Добавление данных в базу
        with connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO {table} (text1, text2) VALUES
                ('{text1}', '{text2}');"""
            )
            print (f'[INFO] Запись успешно добавлена ​​в таблицу {table}')
        connection.commit()

    except Exception as error:
        print('[ERROR] Ошибка при работе с PostgreSQL', error)
    finally:
        # Закрытие подключения к базе
        if connection:
            connection.close()
            print('[INFO] PostgreSQL connection closed')


@app.route('/', methods=['GET','POST'])
def index():
    """Обработчик для страницы index нашего сайта
    1. Выводит шаблон
    2. При нажатии "Отправить" запускает процедуру добавления

    """    
    form = RegForm()
    if form.validate_on_submit():
        text1 = request.form.get('text1')
        text2 = request.form.get('text2')
        insert_record(text1, text2)
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=False, host=host_web, port=port_web)