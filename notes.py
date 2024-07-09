import tkinter as tk
import customtkinter
import sqlite3


def db_start():  # 15
    global conn, cur  # 16

    conn = sqlite3.connect('notes.db')  # 17 подключение к db с помощью connect
    cur = conn.cursor()  # 18 создание объекта курсора

    # 19 запрос создание таблицы только в том случае если в db ее нет
    cur.execute("""CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, note TEXT)""")


# 27 ф-я для добавления заметок
def save_note():
    # 28 сначала получим текст из виджета введенного текста note_entry
    note = note_entry.get()
    # 29 добавляем новую заметку в db
    cur.execute("INSERT INTO notes (note) VALUES (?)", (note,))
    conn.commit()
    # 30 вызываем update_note_list для обновления заметки
    update_notes_list()
    # 31 очистим текстовое поле
    note_entry.delete(0, customtkinter.END)


# 32 создадим ф-ю для удаления заметок
def delete_note():
    # 33 сначала получим индекс по которому находится выбранная заметка
    index = notes_list.curselection()
    # 34 если он существует то удалим его
    if index:
        selected_note = notes_list.get(index)
        cur.execute("DELETE FROM notes WHERE note=?", (selected_note,))
        # обновляем список заметок
        update_notes_list()


# 22 создане функции update_notes_list для обнавление списка заметок
def update_notes_list():
    # 23 сначала очистим виджет notes_list
    notes_list.delete(0, customtkinter.END)
    # 24 получаем заметки хранящиеся в db
    cur.execute("SELECT * FROM notes")
    notes = cur.fetchall()
    # 25 при помощи цикла отобразим в виджите note_list
    for note in notes:
        note_text = note[1]
        notes_list.insert(customtkinter.END, note_text)


root = customtkinter.CTk()  # 1 создадим объект класса CTk
customtkinter.set_appearance_mode("dark")  # добавили темную тему
root.title("My notes")  # 2 указываем загаловок
root.geometry("300x400")  # 3 размеры окна
root.resizable(0, 0)  # 4 запрет на изменение размеров


note_lable = customtkinter.CTkLabel(root, font=('Caveat', 20), text='Заметка')  # 5 виджет lable
note_lable.pack(pady=5)  # 6 отображение при помощи метода pack и установка отступа по оси 'y'=5

note_entry = customtkinter.CTkEntry(root)  # 7 виджет текстового поля
note_entry.pack(pady=5)  # 8 отображение

# 9 виджет кнопка сохнанить
save_button = customtkinter.CTkButton(root, text='Добавить заметку', fg_color='green', command=save_note)
save_button.pack(pady=5)  # 10 отобаражение кнопки сохранить

# 11 виджет кнопка удалить
delete_button = customtkinter.CTkButton(root, text='Удалить заметку', fg_color='green', command=delete_note)
delete_button.pack(pady=5)  # 12 отобаражение кнопки удалить

notes_list = tk.Listbox(root, font=('Caveat', 10), width=45, height=15)  # 13 виджет для отображения всех
# добавленных заметок хранящихся в db
notes_list.pack(padx=5)  # 14

# 20 Добавим вызов функции db_start перед mainloop
db_start()
# 26 добавим вызов ф-и update_notes_list после db_start
update_notes_list()

root.mainloop()
# 21 после mainloop закроем соединение с db
conn.close()
