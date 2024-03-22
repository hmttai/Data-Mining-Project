import argparse

#lấy tham số từ cmd
parser = argparse.ArgumentParser()
parser.add_argument('filename', help='input CSV file')
args = parser.parse_args()

filename = args.filename

with open(filename, 'r') as f:
    data = f.read()

# Phân tích chuỗi CSV và tìm tên cột và dữ liệu
rows = data.split('\n')
column_names = rows[0].split(',')
data = [row.split(',') for row in rows[1:] if row]

#Đếm dòng có missing values
missing_row_count = 0
for i in data:
    if '' in i:
        missing_row_count += 1

print("Number of rows with missing values:", missing_row_count)