import argparse

#lấy tham số từ cmd
parser = argparse.ArgumentParser()
parser.add_argument('filename', help='input CSV file')
parser.add_argument('--method', choices=['mean', 'median', 'mode'], default='mean', help='imputation method')
parser.add_argument('--columns', nargs='+',default="", help='columns to impute')
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
if columns_todo == '':
    columns_todo = column_names

#hàm check float
def is_float(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

#chuyển các số đang ở kiểu str thành kiểu int, float
for row in data:
    for i in range(len(row)):
        if row[i].isdigit():    
            row[i] = int(row[i])
        elif row[i] == '':
            pass
        else:
            try:
                row[i] = float(row[i])    
            except ValueError:
                pass    

#check datatype của các column
data_types = []
for i in range(len(column_names)):
    col_data = [row[i] for row in data if row[i]]
    if all(is_float(x) for x in col_data):
        data_types.append('numeric')
    else:
        data_types.append('categorical')

#tính mean, median, mode
for i in range(len(column_names)):
    if column_names[i] in columns_todo:
        col_data = [row[i] for row in data if row[i]]
        if data_types[i] == 'numeric':
            col_data = [float(x) for x in col_data]
            if method == 'mean':
                if len(col_data) > 0:
                    col_mean = sum(col_data) / len(col_data)
                    for j in range(len(data)):
                        if not data[j][i]:
                            data[j][i] = col_mean
                else:
                    for j in range(len(data)):
                        if not data[j][i]:
                            data[j][i] = 0
            elif method == 'median':
                if len(col_data) > 0:
                    col_median = sorted(col_data)[len(col_data) // 2]
                    for j in range(len(data)):
                        if not data[j][i]:
                            data[j][i] = col_median
                else:
                    for j in range(len(data)):
                        if not data[j][i]:
                            data[j][i] = 0
        
        else:
            col_data = [x for x in col_data if x]
            if len(col_data) > 0:
                col_mode = max(set(col_data), key=col_data.count)
                for j in range(len(data)):
                    if not data[j][i]:
                        data[j][i] = col_mode
            else:
                for j in range(len(data)):
                    if not data[j][i]:
                        data[j][i] = ''


#xuat file output
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