import requests
from bs4 import BeautifulSoup
import csv

# URL cần lấy dữ liệu
url = "https://www.booking.com/searchresults.html?ss=Hanoi%2C+Vietnam&checkin=2025-06-22&checkout=2025-06-23&group_adults=2&no_rooms=1&group_children=0"

# Header giả lập trình duyệt thật
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
}

# Gửi yêu cầu HTTP
response = requests.get(url, headers=headers)

# Kiểm tra kết nối
if response.status_code == 200:
    print("✅ Kết nối thành công Booking.com\n")
    html_content = response.text
    soup = BeautifulSoup(html_content, 'lxml')
    # Tìm tất cả các phần tử khách sạn
    hotel_divs = soup.find_all('div', role="listitem")
    
    # Mở file CSV để ghi dữ liệu
    with open('hotel_data.csv', 'w', newline='', encoding='utf-8') as file_csv:
        writer = csv.writer(file_csv)
        # Viết tiêu đề cột vào file CSV
        writer.writerow(['Hotel Name', 'Location', 'Price', 'Rating', 'Score', 'Review', 'Link'])

        # Duyệt qua tất cả khách sạn
        for hotel in hotel_divs:
            try:
                hotel_name = hotel.find('div', class_="b87c397a13 a3e0b4ffd1").text.strip()
            except AttributeError:
                hotel_name = "Không tìm thấy tên"

            try:
                location = hotel.find('span', class_="d823fbbeed f9b3563dd4").text.strip()
            except AttributeError:
                location = "Không tìm thấy vị trí"
            
            try:
                price = hotel.find('span', class_="b87c397a13 f2f358d1de ab607752a2").text.strip().replace('VND', '')
            except AttributeError:
                price = "Không tìm thấy giá"
            
            try:
                score = hotel.find('div', class_="f63b14ab7a f546354b44 becbee2f63").text.strip().split(' ')[-1]
            except AttributeError:
                score = "Không tìm thấy điểm số"
            
            try:
                rating = hotel.find('div', class_="f63b14ab7a dff2e52086").text.strip()
            except AttributeError:
                rating = "Không có đánh giá"
            
            try:
                review = hotel.find('div', class_="fff1944c52 fb14de7f14 eaa8455879").text.strip()
            except AttributeError:
                review = "Không có nhận xét"
            
            try:
                link = hotel.find('a', href=True).get('href')
            except AttributeError:
                link = "Không có liên kết"

            # In thông tin ra màn hình
            print(hotel_name)
            print(location)
            print(price)
            print(rating)
            print(score)
            print(review)
            print(link)
            print(' ')

            # Ghi vào file CSV
            writer.writerow([hotel_name, location, price, rating, score, review, link])

else:
    print(f"Kết nối không thành công! Mã lỗi: {response.status_code}")
