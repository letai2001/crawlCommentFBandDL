import csv

filtered_links = []

# Đọc file CSV hiện tại và lưu các liên kết thỏa mãn vào danh sách filtered_links
with open('output.csv', 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        if row[0].startswith("https://www.facebook.com/fabrizioromanoherewego/posts"):
            filtered_links.append(row[0])

# Ghi các liên kết đã lọc vào một file mới (hoặc ghi đè lên file hiện tại nếu bạn muốn)
with open('filtered_output.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['link_post'])  # Ghi tiêu đề cột vào dòng đầu tiên của file
    for link in filtered_links:
        writer.writerow([link])
