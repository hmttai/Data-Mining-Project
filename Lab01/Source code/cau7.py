import argparse

#lấy tham số từ cmd
parser = argparse.ArgumentParser()
parser.add_argument('filename', help='input CSV file')
parser.add_argument('--method', choices=['min-max','z-score'], default='min-max', help='normalize method')
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
if columns_todo == '':
    columns_todo = column_names

#check float
def is_float(x):
    try:
        float(x)
        return True
    except ValueError:
        return False

#check data type của các columns
data_types = []
for i in range(len(column_names)):
    col_data = [row[i] for row in data if row[i]]
    if all(is_float(x) for x in col_data):
        data_types.append('numeric')
    else:
        data_types.append('categorical')

#tính min max
if method == 'min-max':
    for i in range(len(column_names)):
        if column_names[i] in columns_todo:
            if data_types[i] == "numeric":
                #print([row[i] for row in data])
                min_val = min([row[i] != '' and float(row[i]) for row in data])
                max_val = max([row[i] != '' and float(row[i]) for row in data])
                #print(min_val)
                #print(max_val)
                for row in data:
                    if row[i] != '': 
                        attr_value = float(row[i])
                    if max_val == min_val:
                        normalized_value = 0.5
                    else:
                        normalized_value = (attr_value - min_val) / (max_val - min_val)
                    row[i] = normalized_value

#tính z-score
elif method == 'z-score':
    for i in range(len(column_names)):
        if column_names[i] in columns_todo:
            if data_types[i] == "numeric":
                attr_values = [row[i] != '' and float(row[i]) for row in data]

                attr_mean = sum(attr_values) / len(attr_values)
                attr_stddev = (sum((x - attr_mean)**2 for x in attr_values) / len(attr_values))**0.5
                
                for row in data:
                    if row[i] != '' and attr_stddev != 0:
                        z_score = (float(row[i]) - attr_mean) / attr_stddev
                        row[i] = str(z_score)

#xuat file
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