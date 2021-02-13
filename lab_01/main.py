import PySimpleGUI as sg

sg.theme('LightGreen6')   # Add a touch of color

# Example of table data
data = [[' ' * 3, ' ' * 6, ' ' * 6]for col in range(15)]
data[0][0] = "1"
data[0][1] = "5"
data[0][2] = "5"

# All the stuff inside the window.
layout = [[sg.InputText('10 20 40 40')],
          [sg.Button('Add points to 1st set', size=(18, 1)), sg.Button('Add points to 2nd set', size=(18, 1))],
          [sg.Table(data, headings=["№", "x", "y"], num_rows=10), sg.Table(data, headings=["№", "x", "y"], num_rows=10)],
          [sg.Button('Change point', size=(11, 1)), sg.Button('Delete point', size=(11, 1)),
           sg.Button('Cancel', size=(11, 1))],
          [sg.Button('Run', size=(38, 1))]]


# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print('You entered ', values[0])

window.close()