import argparse

#lấy tham số từ cmd
parser = argparse.ArgumentParser()
parser.add_argument('filename', help='input CSV file')
parser.add_argument('--method', choices=['+', '-','*','/'], default='+', help='calculate')
parser.add_argument('--columns', nargs='+', help='columns to impute')
parser.add_argument('--out', help='output CSV file')

args = parser.parse_args()

filename = args.filename
method = args.method
columns_todo = args.columns
output = args.out

with open(filename, 'r') as f:
    data = f.read()

# Phân tích chuỗi CSV và tìm tên cột và dữ liệu
rows = data.split('\n')
column_names = rows[0].split(',')
data = [row.split(',') for row in rows[1:] if row]

attr1 = columns_todo[0]
attr2 = columns_todo[1]

#phép cộng và lưu kết quả vào cột result
if method == '+':
    column_names.append("result")
    for row in data:
        if row[column_names.index(attr1)].isdigit() and row[column_names.index(attr2)].isdigit():        
            result = int(row[column_names.index(attr1)]) + int(row[column_names.index(attr2)])
            row.append(str(result))
        else:
            row.append("")

#phép trừ và lưu kết quả vào cột result
if method == '-':
    column_names.append("result")
    for row in data:
        if row[column_names.index(attr1)].isdigit() and row[column_names.index(attr2)].isdigit():
            result = int(row[column_names.index(attr1)]) - int(row[column_names.index(attr2)])
            row.append(str(result))
        else:
            row.append("")

#phép nhân và lưu kết quả vào cột result
if method == '*':
    column_names.append("result")
    for row in data:
        if row[column_names.index(attr1)].isdigit() and row[column_names.index(attr2)].isdigit():
            result = int(row[column_names.index(attr1)]) * int(row[column_names.index(attr2)])
            row.append(str(result))
        else:
            row.append("")

##phép chia và lưu kết quả vào cột result
if method == '/':
    column_names.append("result")
    for row in data:
        if row[column_names.index(attr1)].isdigit() and row[column_names.index(attr2)].isdigit():
            #check số bị chia != 0
            if int(row[column_names.index(attr2)]) == 0:
                result = ""
            else:
                result = int(row[column_names.index(attr1)]) / int(row[column_names.index(attr2)])
            row.append(str(result))
        else:
            row.append("")

#xuat file      
columns_todo.append("result")
column_index = []
for i in range(len(columns_todo)):
    if columns_todo[i] in column_names:
        column_index.append(column_names.index(columns_todo[i]))
new_data = []
for i in range(len(column_index)):
    temp = []
    for row in data:
        temp.append(row[column_index[i]])
    new_data.append(temp)

with open(output, 'w') as f:
     
    for i in range(len(columns_todo)):
        
        if i == len(columns_todo) - 1:
            f.write(str(columns_todo[i]) + '\n')
        else:
            f.write(str(columns_todo[i]) + ',')
    
    for col in range(len(new_data[0])):
        
        col_values = [str(row[col]) for row in new_data]
        f.write(','.join(col_values) + '\n')

