import argparse

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

#tìm vị trí cột có missing values
missing_cols = []
for i in column_names:
    missing_count = 0
    for row in data:
        if row[column_names.index(i)] == '':
            missing_count += 1
    if missing_count > 0:
        missing_cols.append(i)

print("Columns with missing values:", ",".join(missing_cols))
