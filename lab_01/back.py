import sympy as sy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pat
from tkinter import messagebox as msg


# calculating funcs
def find_circle_center(dot1, dot2, dot3) -> tuple[float, float]:
    h, k, r = sy.symbols("h k r")
    eq1 = (dot1[0] - h) * (dot1[0] - h) + (dot1[1] - k) * (dot1[1] - k) - r * r
    eq2 = (dot2[0] - h) * (dot2[0] - h) + (dot2[1] - k) * (dot2[1] - k) - r * r
    eq3 = (dot3[0] - h) * (dot3[0] - h) + (dot3[1] - k) * (dot3[1] - k) - r * r
    accur_h = np.abs(dot1[0] - dot2[0])
    accur_k = np.abs(dot1[1] - dot2[1])
    accur_r = (accur_h * accur_h + accur_k * accur_k) ** 0.5
    solve = sy.nsolve((eq1, eq2, eq3), (h, k, r), (accur_h, accur_k, accur_r)).tolist()
    return solve[0][0], solve[1][0]


def calc_tan(point, r1, r2):
    eps = 1e-9
    r = r2 - r1
    z = point[0] * point[0] + point[1] * point[1]
    d = z - r * r
    if d < -eps:
        return None
    d = (np.abs(d)) ** 0.5
    res = [0.0, 0.0, 0.0]
    res[0] = (point[0] * r + point[1] * d) / z
    res[1] = (point[1] * r - point[0] * d) / z
    res[2] = r1
    return res


def tangents(f_circle_center, s_circle_center, radius1, radius2):
    result = []
    temp_center = [0, 0]
    temp_center[0] = s_circle_center[0] - f_circle_center[0]
    temp_center[1] = s_circle_center[1] - f_circle_center[1]
    for i in range(-1, 2, 2):
        for j in range(-1, 2, 2):
            temp = calc_tan(temp_center, radius1 * i, radius2 * j)
            if temp:
                result.append(temp)
    for i in range(0, len(result)):
        result[i][2] -= result[i][0] * f_circle_center[0] + result[i][1] * f_circle_center[1]
    if len(result) != 4:
        result = None
    return result


def determ_points_dist(x1, y1, x2, y2):
    return ((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)) ** 0.5


def find_intersection_point(radius, center, a, b, c):
    x, y = sy.symbols('x, y')
    eq1 = sy.Eq((x - center[0]) * (x - center[0]) + (y - center[1]) * (y - center[1]), radius * radius)
    eq2 = sy.Eq(a * x + b * y + c, 0)
    result = sy.solve([eq1, eq2], [x, y])
    # print("\nResult type: ", type(result[0]))
    # print("Result[0] type: ", type(result[0][0]))
    res = [0, 0]
    res[0] = complex(result[0][0]).real
    res[1] = complex(result[0][1]).real
    return res


def find_lines_intersection_point(a1, b1, c1, a2, b2, c2):
    x, y = sy.symbols('x, y')
    eq1 = sy.Eq(a1 * x + b1 * y + c1, 0)
    eq2 = sy.Eq(a2 * x + b2 * y + c2, 0)
    result = sy.solve([eq1, eq2], [x, y])
    res = []
    res.append(result[x])
    res.append(result[y])
    return res


def determ_interior_tangents(tangents_list, f_circle_center, s_circle_center, radius1, radius2):
    eps = 1e-7
    minimum, second_minimum = None, None
    interior_tangents = [[None, None], [None, None]]
    interior_tangents_sec = [[None, None], [None, None]]
    indices = [None, None]
    for i in range(len(tangents_list)):
        intersection = find_intersection_point(radius1, f_circle_center, tangents_list[i][0], tangents_list[i][1],
                                               tangents_list[i][2])
        temp_dist = determ_points_dist(intersection[0], intersection[1],
                                       s_circle_center[0], s_circle_center[1])
        if not minimum or temp_dist - minimum < eps:
            second_minimum = minimum
            minimum = temp_dist
            interior_tangents[1][0] = interior_tangents[0][0]
            interior_tangents[1][1] = interior_tangents[0][1]
            interior_tangents[0][0] = intersection[0]
            interior_tangents[0][1] = intersection[1]
            indices[1] = indices[0]
            indices[0] = i
        elif not second_minimum or temp_dist - second_minimum < eps:
            second_minimum = temp_dist
            interior_tangents[1][0] = intersection[0]
            interior_tangents[1][1] = intersection[1]
            indices[1] = i
    intersection = find_intersection_point(radius2, s_circle_center, tangents_list[indices[0]][0],
                                           tangents_list[indices[0]][1], tangents_list[indices[0]][2])
    interior_tangents_sec[0][0] = intersection[0]
    interior_tangents_sec[0][1] = intersection[1]
    intersection = find_intersection_point(radius2, s_circle_center, tangents_list[indices[1]][0],
                                           tangents_list[indices[1]][1], tangents_list[indices[1]][2])
    interior_tangents_sec[1][0] = intersection[0]
    interior_tangents_sec[1][1] = intersection[1]
    result = [[tuple(interior_tangents[0]), tuple(interior_tangents_sec[0])],
              [tuple(interior_tangents[1]), tuple(interior_tangents_sec[1])]]
    intersec = find_lines_intersection_point(tangents_list[indices[0]][0], tangents_list[indices[0]][1],
                                             tangents_list[indices[0]][2],
                                             tangents_list[indices[1]][0], tangents_list[indices[1]][1],
                                             tangents_list[indices[1]][2])
    return result, intersec


def calculate_square(center1, center2, radius1, radius2):
    tangents_forms = tangents(center1, center2, radius1, radius2)
    if not tangents_forms:
        return -1
    tang_points, inter_point = determ_interior_tangents(tangents_forms, center1, center2, radius1, radius2)
    square = 0.0
    temp = determ_points_dist(inter_point[0], inter_point[1], tang_points[0][0][0], tang_points[0][0][1])
    square += radius1 * temp
    temp = determ_points_dist(inter_point[0], inter_point[1], tang_points[0][1][0], tang_points[0][1][1])
    square += radius2 * temp
    return square, tang_points


def find_radius(dot1, dot2, dot3):
    h, k, r = sy.symbols("h k r")
    eq1 = (dot1[0] - h) * (dot1[0] - h) + (dot1[1] - k) * (dot1[1] - k) - r * r
    eq2 = (dot2[0] - h) * (dot2[0] - h) + (dot2[1] - k) * (dot2[1] - k) - r * r
    eq3 = (dot3[0] - h) * (dot3[0] - h) + (dot3[1] - k) * (dot3[1] - k) - r * r
    accur_h = np.abs(dot1[0] - dot2[0])
    accur_k = np.abs(dot1[1] - dot2[1])
    accur_r = (accur_h * accur_h + accur_k * accur_k) ** 0.5
    solve = sy.nsolve((eq1, eq2, eq3), (h, k, r), (accur_h, accur_k, accur_r)).tolist()
    return np.abs(solve[2][0])


def main_calculation(set1, set2):
    if len(set1) <= 2 or len(set2) <= 2:
        msg.showinfo("Ошибка выполнения",
                     "Требуется больше точек\nдля выполнения программы")
        return

    result_circles = [[[None, None], None], [[None, None], None]]
    tangent_points = None
    min_square = None
    degenerates = 0

    for i in range(len(set1)):
        for j in range(i + 1, len(set1)):
            for k in range(j + 1, len(set1)):
                s1_dot_1, s1_dot_2, s1_dot_3 = set1[i], set1[j], set1[k]
                try:
                    s1_radius = find_radius(s1_dot_1, s1_dot_2, s1_dot_3)
                except:
                    continue
                for l in range(len(set2)):
                    for m in range(i + 1, len(set2)):
                        for n in range(j + 1, len(set2)):
                            s2_dot_1, s2_dot_2, s2_dot_3 = set2[i], set2[j], set2[k]
                            try:
                                s2_radius = find_radius(s2_dot_1, s2_dot_2, s2_dot_3)
                            except:
                                continue
                            s1_circle_center = find_circle_center(s1_dot_1, s1_dot_2, s1_dot_3)
                            s2_circle_center = find_circle_center(s2_dot_1, s2_dot_2, s2_dot_3)
                            temp_square, temp_tangents = calculate_square(s1_circle_center, s2_circle_center, s1_radius,
                                                                          s2_radius)
                            if temp_square == -1 or temp_square == 0:
                                degenerates += 1
                            else:
                                if not min_square or temp_square - min_square < 1e-7:
                                    result_circles = [[s1_circle_center, s1_radius], [s2_circle_center, s2_radius]]
                                    tangent_points = temp_tangents
                                    min_square = temp_square
    if not min_square:
        msg.showinfo("Не найдено решений",
                     "Количество вырожденных случаев:", degenerates)
        return
    else:
        ans_draw(result_circles[0], result_circles[1], tangent_points)


def ans_draw(circle1, circle2, tangents):
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
    plt.text(tangents[0][0][0] + 0.25, tangents[0][0][1] + 0.25, centr_str)

    # tangent №1 second point
    plt.plot(tangents[0][1][0], tangents[0][1][1], 'ro', color='black')
    centr_str = '({:.2f}, {:.2f})'.format(tangents[0][1][0], tangents[0][1][1])
    plt.text(tangents[0][1][0] + 0.25, tangents[0][1][1] + 0.25, centr_str)

    # tangent №2 first point
    plt.plot(tangents[1][0][0], tangents[1][0][1], 'ro', color='black')
    centr_str = '({:.2f}, {:.2f})'.format(tangents[1][0][0], tangents[1][0][1])
    plt.text(tangents[1][0][0] + 0.25, tangents[1][0][1] + 0.25, centr_str)

    # tangent №2 second point
    plt.plot(tangents[1][1][0], tangents[1][1][1], 'ro', color='black')
    centr_str = '({:.2f}, {:.2f})'.format(tangents[1][1][0], tangents[1][1][1])
    plt.text(tangents[1][1][0] + 0.25, tangents[1][1][1] + 0.25, centr_str)

    # circle 1 - center
    plt.plot(circle1[0][0], circle1[0][1], 'ro', color='black')
    centr_str = '({:.2f}, {:.2f})'.format(circle1[0][0], circle1[0][1])
    plt.text(circle1[0][0] + 0.25, circle1[0][1] + 0.25, centr_str)

    # circle 2 - center
    plt.plot(circle2[0][0], circle2[0][1], 'ro', color='black')
    centr_str = '({:.2f}, {:.2f})'.format(circle2[0][0], circle2[0][1])
    plt.text(circle2[0][0] + 0.25, circle2[0][1] + 0.25, centr_str)

    fig = plt.gcf()
    ax = fig.gca()
    ax.add_patch(circle_1)
    ax.add_patch(circle_2)
    plt.show(block=False)
