import gradio as gr
import json
import os

FILE = 'passwords.json'

def load():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save(data):
    with open(FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add(service, login, password):
    if not service or not login or not password:
        return load_table(), 'Заполни все поля'
    data = load()
    data[service] = {'login': login, 'password': password}
    save(data)
    return load_table(), 'Добавлено'

def load_table():  
    data = load()
    return [[k, v['login'], v['password']] for k, v in data.items()]

def delete(service):
    data = load()
    if service in data:
        del data[service]
        save(data)
        return load_table(), 'Удалено'
    return load_table(), 'Такого сервиса нет'

with gr.Blocks(title='Мои пароли') as app:
    gr.Markdown('Мои пароли')
    gr.Markdown('дабавьте запись')

    with gr.Row():
        service = gr.Textbox(label='Сервис')
        login = gr.Textbox(label='Логин')
        password = gr.Textbox(label='Пароль')

    msg = gr.Markdown()

    table = gr.Dataframe(
        headers=['Сервис', 'Логин', 'Пароль'],
        value=load_table(),
        label='Сохранённые пароли',
        interactive=False       
    )

    gr.Markdown('Удаление')
    del_name = gr.Textbox(label='Введи название сервиса и нажми Enter')

    fields = [service, login, password]
    outputs = [table, msg, service, login, password]

    for field in fields:
        field.submit(add, fields, outputs)  

    del_name.submit(delete, [del_name], [table, msg, del_name])

app.launch()