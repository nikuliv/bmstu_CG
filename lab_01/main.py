
from front import *
from back import *
import time

sg.theme('LightGreen6')  # Add a touch of color

# Example of table data
set_1 = [[' ' * 3, ' ' * 6, ' ' * 6] for col in range(100)]
set_2 = [[' ' * 3, ' ' * 6, ' ' * 6] for col in range(100)]

# All the stuff inside the window.
layout = [[sg.Text('Введите координаты точек через пробел: ', font=5)],
          [sg.InputText('10 20 40 40', size=(39, 2), font=4)],
          [sg.Button('Добавить точки в 1-е множество', size=(19, 2), font=2), sg.Button('Добавить точки во 2-е множество', size=(18, 2), font=2)],
          [sg.Table(set_1, headings=["№", "x", "y"], num_rows=10, key='set1', font=4),
           sg.Table(set_2, headings=["№", "x", "y"], num_rows=10, key='set2', font=4)],
          [sg.Button('Изменить точку', size=(12, 2), font=2), sg.Button('Удалить точку', size=(12, 2), font=2),
           sg.Button('Запуск', size=(12, 2), font=2)]]


# Create the Window
window = sg.Window('Лабораторная работа №1 Никуленко И.В.', layout)
figure = None
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
        break
    if event == 'Удалить точку':
        delete_wind = make_win_del()
        while True:
            d_event, d_values = delete_wind.read()
            if d_event == sg.WIN_CLOSED:
                break
            if d_event == 'Удалить':
                if d_values[0] == "1":
                    del_point(set_1, int(d_values[1]) - 1)
                else:
                    del_point(set_2, int(d_values[1]) - 1)
            elif d_event == 'Выход':
                delete_wind.close()
                break
            window['set1'].update(set_1)
            window['set2'].update(set_2)
    elif event == 'Добавить точки в 1-е множество':
        try:
            dots = [float(i) for i in values[0].split(" ")]
            if len(dots) % 2 != 0:
                msg.showinfo("Ошибка чтения",
                             "Некорректный ввод")
            else:
                update_table(set_1, dots)
        except:
            msg.showinfo("Ошибка чтения",
                         "Некорректный ввод")
    elif event == 'Добавить точки во 2-е множество':
        try:
            dots = [float(i) for i in values[0].split(" ")]
            if len(dots) % 2 != 0:
                msg.showinfo("Ошибка чтения",
                             "Некорректный ввод")
            else:
                update_table(set_2, dots)
        except:
            msg.showinfo("Ошибка чтения",
                         "Некорректный ввод")
    elif event == 'Изменить точку':
        change_wind = make_win_ch()
        while True:
            c_event, e_values = change_wind.read()
            if c_event == sg.WIN_CLOSED:
                break
            if c_event == 'Изменить':
                if e_values[0] == "1":
                    change_point_value(set_1, int(e_values[1]), e_values[2].split(" "))
                else:
                    change_point_value(set_2, int(e_values[1]), e_values[2].split(" "))
                change_wind.close()
            if c_event == 'Выход':
                change_wind.close()
                break
    elif event == 'Запуск':
        dots1 = convert_table_data(set_1)
        dots2 = convert_table_data(set_2)
        start_time = time.time()
        data = main_calculation(dots1, dots2)
        if data:
            res_wind = make_win_res(data[0])
            res_wind.TKroot.minsize(720, 750)
            figure = ans_draw(res_wind, figure, data[1])

        print("--- %s seconds ---" % (time.time() - start_time))

    window['set1'].update(set_1)
    window['set2'].update(set_2)

window.close()
