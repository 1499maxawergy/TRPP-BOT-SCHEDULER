import openpyxl

group_cell = dict()


# init - просматривает все xlsx файлы и создает словарь с нахождением расписания этих групп
def __init__():
    for number_of_xlxs in range(1, 4):
        sheet = openpyxl.load_workbook("iit" + str(number_of_xlxs) + ".xlsx").active
        for column in range(5, sheet.max_column, 5):
            if sheet[2][column].value != "День недели":
                group_cell[sheet[2][column].value] = column


# get_xlsx - по имени группы выводит название файла, в котором лежит расписание с этой группой
def get_xlsx(group_name):
    if group_name[-2:] == "21":
        return "iit1.xlsx"
    elif group_name[-2:] == "20":
        return "iit2.xlsx"
    elif group_name[-2:] == "19":
        return "iit3.xlsx"
    elif group_name[-2:] == "18":
        return "iit4.xlsx"
    else:
        return None


# print_week - вывод недели расписания по имени группы (week: 0 - нечетная, 1 - четная)
def print_week(group_name, week):
    group_name = group_name.upper()
    if group_cell.get(group_name) is not None:
        answer = "```\n"
        excel_filename = get_xlsx(group_name)
        sheet = openpyxl.load_workbook(excel_filename).active

        for day in range(4, 64, 12):
            answer += sheet[day][0].value + '\n'
            for para in range(day + week, day + 12, 2):
                if sheet[para][group_cell[group_name]].value is not None:
                    answer += '№' + str(sheet[para][1].value) + '\t'
                    if sheet[para][1].value is not None:
                        answer += str(sheet[para][2].value) + '\t'
                        answer += str(sheet[para][3].value) + '\t'
                    else:
                        answer += str(sheet[para - 1][2].value) + '\t'
                        answer += str(sheet[para - 1][3].value) + '\t'

                    answer += str(sheet[para][group_cell[group_name] + 3].value) + '\n'
                    answer += str(sheet[para][group_cell[group_name]].value) + '\n\n'
            answer += '\n\n'

        answer += "```"
        return answer
    else:
        return "Ваша группа не найдена."
