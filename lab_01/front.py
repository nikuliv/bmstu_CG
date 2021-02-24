import PySimpleGUI as sg
from typing import TypeVar
from tkinter import messagebox as msg


def find_last_element(table):
    coefficient = 0
    while table[coefficient][0] != '   ':
        coefficient += 1
    return coefficient


def update_table(table_data, dots):
    k = 0
    if table_data[0][0] == '   ':
        for i in range(int(len(dots) / 2)):
            table_data[i][0] = str(i + 1)
            table_data[i][1] = round(dots[k], 3)
            table_data[i][2] = round(dots[k + 1], 3)
            k += 2
    else:
        coefficient = find_last_element(table_data)
        for i in range(int(len(dots) / 2)):
            table_data[coefficient + i][0] = str(coefficient + i + 1)
            table_data[coefficient + i][1] = round(dots[k], 3)
            table_data[coefficient + i][2] = round(dots[k + 1], 3)
            k += 2


def change_point_value(table_data: list[list[str]], coefficient: int, coords: list[str]) -> None:
    check = find_last_element(table_data)
    if coefficient <= check and table_data[0][0] != '   ':
        table_data[coefficient - 1][1] = coords[0]
        table_data[coefficient - 1][2] = coords[1]
    else:
        msg.showinfo("Ошибка",
                     "Точка не найдена")


def del_point(table_data: list[list[str]], coefficient: int) -> None:
    check = find_last_element(table_data)
    if coefficient > check or table_data[0][0] == '   ':
        msg.showinfo("Ошибка",
                     "Точка не найдена")
    else:
        while table_data[coefficient][0] != '   ':
            # print(table_data[coefficient][0])
            table_data[coefficient][0] = table_data[coefficient + 1][0]
            table_data[coefficient][1] = table_data[coefficient + 1][1]
            table_data[coefficient][2] = table_data[coefficient + 1][2]
            try:
                table_data[coefficient][0] = str(int(table_data[coefficient][0]) - 1)
            except:
                pass
            coefficient += 1


def make_win_del():
    layout = [[sg.Text('Выберите множество: ', font=2), sg.Combo(['1', '2'], default_value='1', font=2)],
              [sg.Text('Введите номер точки: ', font=2), sg.InputText('1', font=2, size=(5, 1))],
              [sg.Button('Удалить', font=2), sg.Button('Выход', font=2)]]
    return sg.Window('Удаление точки', layout, finalize=True)


def make_win_ch():
    layout = [[sg.Text('Выберите множество: ', font=2), sg.Combo(['1', '2'], default_value='1', font=2)],
              [sg.Text('Введите номер точки: ', font=2), sg.InputText('1', font=2, size=(5, 1))],
              [sg.Text('Введите новые координаты: ', font=2), sg.InputText('1 1', font=2, size=(10, 1))],
              [sg.Button('Изменить', font=2), sg.Button('Выход', font=2)]]
    return sg.Window('Изменение координат точки', layout, finalize=True)


def convert_table_data(set):
    dots = []
    i = 0
    while set[i][0] != '   ':
        dots.append(tuple([set[i][1], set[i][2]]))
        i += 1
    return dots