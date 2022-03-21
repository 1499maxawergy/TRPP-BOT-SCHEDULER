import openpyxl

sheet = openpyxl.load_workbook("iit2.xlsx").active

group_cell = dict()

for column in range(5, sheet.max_column, 5):
    if sheet[2][column].value != "День недели":
        group_cell[sheet[2][column].value] = column

print(group_cell)
