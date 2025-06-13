import requests
from bs4 import BeautifulSoup

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
    soup = BeautifulSoup(response.text, 'html.parser')

    # Tìm tất cả các thẻ chứa thông tin khách sạn
    hotels = soup.find_all('div', {'data-testid': 'property-card'})

    if not hotels:
        print("⚠️ Không tìm thấy khách sạn nào. Có thể trang được render bằng JavaScript.")
    else:
        print("📋 Danh sách khách sạn:")
        for idx, hotel in enumerate(hotels[:10], start=1):  # Lấy tối đa 10 khách sạn đầu
            name_tag = hotel.find('div', {'data-testid': 'title'})
            name = name_tag.get_text(strip=True) if name_tag else "Không có tên"
            print(f"{idx}. {name}")
else:
    print(f"❌ Kết nối thất bại! Mã lỗi: {response.status_code}")
