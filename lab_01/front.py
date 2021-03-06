import PySimpleGUI as sg
from typing import TypeVar
import matplotlib.pyplot as plt
import matplotlib.patches as pat
from matplotlib.ticker import NullFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')
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


def make_win_res(*data):
    if data is None:
        return
    circle1, circle2, tangent_points, square = data[0]
    layout = [[sg.Text('Первая окружность задана точками: ', font=2), sg.Text('Вторая окружность задана точками: ', font=2)],
              [sg.Text("№{:d} ({:.3f}, {:.3f})                           ".format(circle1[0][0], circle1[0][1], circle1[0][2]), font=2),
               sg.Text("    №{:d} ({:.3f}, {:.3f})".format(circle2[0][0], circle2[0][1], circle2[0][2]), font=2)],
              [sg.Text("№{:d} ({:.3f}, {:.3f})                           ".format(circle1[1][0], circle1[1][1], circle1[1][2]), font=2),
               sg.Text("    №{:d} ({:.3f}, {:.3f})".format(circle2[1][0], circle2[1][1], circle2[1][2]), font=2)],
              [sg.Text("№{:d} ({:.3f}, {:.3f})                           ".format(circle1[2][0], circle1[2][1], circle1[2][2]), font=2),
               sg.Text("    №{:d} ({:.3f}, {:.3f})".format(circle2[2][0], circle2[2][1], circle2[2][2]), font=2)],
              [sg.Text('Первая касательная задана точками: ', font=2)],
              [sg.Text("1. ({:.3f}, {:.3f})".format(tangent_points[0][0][0], tangent_points[0][0][1]), font=2)],
              [sg.Text("2. ({:.3f}, {:.3f})".format(tangent_points[0][1][0], tangent_points[0][1][1]), font=2)],
              [sg.Text('Вторая касательная задана точками: ', font=2)],
              [sg.Text("1. ({:.3f}, {:.3f})".format(tangent_points[1][0][0], tangent_points[1][0][1]), font=2)],
              [sg.Text("2. ({:.3f}, {:.3f})".format(tangent_points[1][1][0], tangent_points[1][1][1]), font=2)],
              [sg.Text('Разность площадей четырехугольников: {:.6f}'.format(square), font=2)],
              [sg.Canvas(key='-CANVAS-')]]
    return sg.Window('Результаты', layout, finalize=True, resizable=True, size=(720, 750))



def ans_draw(window, old_fig, *data):
    if old_fig:
        old_fig.gca().cla()
    circle1, circle2, tangents = data[0]
    circle_1 = pat.Circle((circle1[0][0], circle1[0][1]), circle1[1], color='b', fill=False)
    circle_2 = pat.Circle((circle2[0][0], circle2[0][1]), circle2[1], color='b', fill=False)

    # tangent 1 - line
    plt.plot([tangents[0][0][0], tangents[0][1][0]], [tangents[0][0][1], tangents[0][1][1]], color='r', lw=2)

    # tangent 2 - line
    plt.plot([tangents[1][0][0], tangents[1][1][0]], [tangents[1][0][1], tangents[1][1][1]], color='r', lw=2)

    # circle 1 - first radius
    plt.plot([tangents[0][0][0], circle1[0][0]], [tangents[0][0][1], circle1[0][1]], color='r', lw=2)

    # circle 1 - second radius
    plt.plot([tangents[1][0][0], circle1[0][0]], [tangents[1][0][1], circle1[0][1]], color='r', lw=2)

    # circle 2 - first radius
    plt.plot([circle2[0][0], tangents[0][1][0]], [circle2[0][1], tangents[0][1][1]], color='r', lw=2)

    # circle 2 - second radius
    plt.plot([circle2[0][0], tangents[1][1][0]], [circle2[0][1], tangents[1][1][1]], color='r', lw=2)

    # tangent №1 first point
    plt.plot(tangents[0][0][0], tangents[0][0][1], 'ro', color='black')
    centr_str = '({:.2f}, {:.2f})'.format(tangents[0][0][0], tangents[0][0][1])
    plt.text(tangents[0][0][0] + 0.125, tangents[0][0][1] + 0.125, centr_str)

    # tangent №1 second point
    plt.plot(tangents[0][1][0], tangents[0][1][1], 'ro', color='black')
    centr_str = '({:.2f}, {:.2f})'.format(tangents[0][1][0], tangents[0][1][1])
    plt.text(tangents[0][1][0] + 0.125, tangents[0][1][1] + 0.125, centr_str)

    # tangent №2 first point
    plt.plot(tangents[1][0][0], tangents[1][0][1], 'ro', color='black')
    centr_str = '({:.2f}, {:.2f})'.format(tangents[1][0][0], tangents[1][0][1])
    plt.text(tangents[1][0][0] + 0.125, tangents[1][0][1] + 0.125, centr_str)

    # tangent №2 second point
    plt.plot(tangents[1][1][0], tangents[1][1][1], 'ro', color='black')
    centr_str = '({:.2f}, {:.2f})'.format(tangents[1][1][0], tangents[1][1][1])
    plt.text(tangents[1][1][0] + 0.125, tangents[1][1][1] + 0.125, centr_str)

    # circle 1 - center
    plt.plot(circle1[0][0], circle1[0][1], 'ro', color='black')
    centr_str = '({:.2f}, {:.2f})'.format(circle1[0][0], circle1[0][1])
    plt.text(circle1[0][0] + 0.125, circle1[0][1] + 0.125, centr_str)

    # circle 2 - center
    plt.plot(circle2[0][0], circle2[0][1], 'ro', color='black')
    centr_str = '({:.2f}, {:.2f})'.format(circle2[0][0], circle2[0][1])
    plt.text(circle2[0][0] + 0.125, circle2[0][1] + 0.125, centr_str)

    fig = plt.gcf()
    ax = fig.gca()
    ax.add_patch(circle_1)
    ax.add_patch(circle_2)
    ax.set_aspect('equal')
    figure_canvas_agg = FigureCanvasTkAgg(fig, window['-CANVAS-'].TKCanvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return fig


def convert_table_data(set):
    dots = []
    i = 0
    while set[i][0] != '   ':
        dots.append(tuple([float(set[i][1]), float(set[i][2])]))
        i += 1
    return dots

