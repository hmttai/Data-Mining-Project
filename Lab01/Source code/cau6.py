import argparse

#lấy tham số từ cmd
parser = argparse.ArgumentParser()
parser.add_argument('filename', help='input CSV file')
parser.add_argument('--out', help='output CSV file')

args = parser.parse_args()

filename = args.filename
output = args.out

with open(filename, 'r') as f:
    data = f.read()

# Phân tích chuỗi CSV và tìm tên cột và dữ liệu
rows = data.split('\n')
column_names = rows[0].split(',')
data = [row.split(',') for row in rows[1:] if row]

#tạo 1 list chứa các row độc nhất từ data và chuyển giá trị từ list đó vào lại data
unique_data = set(tuple(row) for row in data)
data = [list(row) for row in unique_data]

#xuat file
with open(output, 'w') as f:
     
    for i in range(len(column_names)):     
        if i == len(column_names) - 1:
            f.write(str(column_names[i]) + '\n')
        else:
            f.write(str(column_names[i]) + ',')

    for row in data:
        row_str = ",".join(map(str, row))
        f.write(row_str + "\n")