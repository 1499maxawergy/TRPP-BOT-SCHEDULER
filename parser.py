import openpyxl

group_cell = dict()

for number_of_xlxs in range(1, 4):
    sheet = openpyxl.load_workbook("iit" + str(number_of_xlxs) + ".xlsx").active
    for column in range(5, sheet.max_column, 5):
        if sheet[2][column].value != "День недели":
            group_cell[sheet[2][column].value] = column

print(group_cell)
