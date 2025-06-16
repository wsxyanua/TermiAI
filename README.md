# 🤖 AI Terminal Assistant

<div align="center">

![Version](https://img.shields.io/badge/version-1.1-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Một trợ lý terminal thông minh sử dụng AI để tăng cường khả năng tương tác với terminal của bạn.

[Giới thiệu](#-giới-thiệu) • 
[Tính năng](#-tính-năng) • 
[Cài đặt](#-cài-đặt) • 
[Sử dụng](#-sử-dụng) • 
[Đóng góp](#-đóng-góp)

</div>

## 📝 Giới thiệu

AI Terminal Assistant là một công cụ mạnh mẽ giúp bạn tương tác với terminal một cách thông minh và hiệu quả hơn. Sử dụng các mô hình ngôn ngữ local (DeepSeek-Coder và DeepSeek-R1) thông qua Ollama, công cụ này có thể:

- Chuyển đổi ngôn ngữ tự nhiên thành lệnh terminal
- Giải thích và phân tích lệnh shell
- Tự động sửa lỗi và gỡ lỗi
- Cung cấp hướng dẫn kỹ thuật
- Quản lý và tối ưu hóa quy trình làm việc của bạn

## ✨ Tính năng

### 🔍 Gợi ý lệnh thông minh
- Chuyển đổi yêu cầu ngôn ngữ tự nhiên thành lệnh terminal
- Hỗ trợ nhiều ngôn ngữ khác nhau
- Đề xuất lệnh phù hợp với ngữ cảnh
- Giao diện thân thiện với người dùng

```bash
# Ví dụ:
"Liệt kê ổ đĩa gắn ngoài" → lsblk, df -h, mount
"Tìm file lớn hơn 1GB" → find / -type f -size +1G
```

### 🤖 Phân tích lệnh shell
- Giải thích chi tiết từng thành phần của lệnh
- Phân tích mục đích và tác dụng của các tham số
- Cung cấp ví dụ sử dụng
- Hiển thị kết quả rõ ràng, dễ đọc

```bash
# Ví dụ:
explain sudo netstat -tulnp
→ Giải thích chi tiết về lệnh netstat và các tham số
```

### 🔧 Tự động gỡ lỗi
- Phát hiện và sửa lỗi cú pháp
- Đề xuất lệnh thay thế
- Hướng dẫn khắc phục sự cố
- Thông báo lỗi rõ ràng, dễ hiểu

```bash
# Ví dụ:
fix sudo apt get → sudo apt-get
fix chmod 777 / → chmod 755 /
```

### 💬 Chat kỹ thuật
- Trả lời câu hỏi về hệ thống
- Hướng dẫn cài đặt và cấu hình
- Giải thích khái niệm kỹ thuật
- Tương tác tự nhiên, dễ hiểu

```bash
# Ví dụ:
chat "Cách cài đặt Docker trên Ubuntu?"
chat "Giải thích về SELinux"
```

### 📂 Tìm kiếm nâng cao
- Tạo lệnh tìm kiếm tối ưu
- Hỗ trợ tìm kiếm theo nhiều tiêu chí
- Tích hợp với các công cụ tìm kiếm phổ biến
- Kết quả được hiển thị rõ ràng

```bash
# Ví dụ:
search "Tìm file log trong /var/log"
search "Tìm file lớn hơn 1GB trong /home"
```

### 📑 Quản lý script
- Tự động tạo và quản lý script
- Lưu trữ lịch sử lệnh
- Tích hợp với hệ thống quản lý phiên bản
- Giao diện quản lý trực quan

```bash
# Ví dụ:
save "backup_script" → Tạo script backup với các lệnh đã thực thi
```

## 🚀 Cài đặt

### Yêu cầu hệ thống
- Python 3.8 trở lên
- Ollama đã được cài đặt
- Các mô hình DeepSeek-Coder và DeepSeek-R1

### Bước 1: Cài đặt Ollama
```bash
# Tải và cài đặt Ollama
curl https://ollama.ai/install.sh | sh

# Tải các mô hình cần thiết
ollama pull deepseek-coder
ollama pull deepseek-r1
```

### Bước 2: Cài đặt dependencies
```bash
# Cài đặt các thư viện Python
pip install -r requirements.txt
```

## 💻 Sử dụng

### Chạy chương trình
```bash
# Sử dụng mô hình mặc định
python main.py

# Hoặc chỉ định mô hình
python main.py --model deepseek-coder
python main.py --model deepseek-r1
```

### Các lệnh có sẵn  
Các lệnh đặc biệt:
| Lệnh | Mô tả |
|------|--------|
| `help` | Hiển thị trợ giúp |
| `exit` | Thoát chương trình |
| `history` | Xem lịch sử lệnh |
| `model` | Xem/đổi thông tin mô hình |
| `save` | Lưu các lệnh thành script |  

Các lệnh thông minh:  
| Lệnh | Mô tả |
|------|--------|
| `explain <lệnh>` | Giải thích lệnh |
| `fix <lệnh>` | Sửa lệnh sai  |
| `chat <câu hỏi>` | Hỏi đáp kỹ thuật |
| `search <mô tả>` | Tìm kiếm file |
| `ask <câu hỏi>` | Hỏi câu hỏi thường ngày |
### Ví dụ sử dụng
1. **Gợi ý lệnh**:
```bash
What would you like to do? Liệt kê các tiến trình đang chạy
```

2. **Giải thích lệnh**:
```bash
What would you like to do? explain sudo netstat -tulnp
```

3. **Sửa lỗi**:
```bash
What would you like to do? fix sudo apt get
```

4. **Chat kỹ thuật**:
```bash
What would you like to do? chat Cách cài đặt Python?
```

5. **Tìm kiếm**:
```bash
What would you like to do? search Tìm file log trong /var/log
```

## 📁 Cấu trúc dự án
```
.
├── main.py              # File chính chứa toàn bộ logic
├── requirements.txt     # Danh sách các thư viện cần thiết
├── README.md           # Tài liệu hướng dẫn
└── .ai_terminal_scripts/ # Thư mục lưu các script được tạo
```

## ⚙️ Cấu hình
- Lịch sử lệnh: `~/.ai_terminal_history.json`
- Script được lưu: `~/.ai_terminal_scripts/`
- Có thể thay đổi mô hình mặc định trong code
- Giao diện được tùy chỉnh với Rich

## 🤝 Đóng góp
Chúng tôi rất hoan nghênh mọi đóng góp! Hãy tham gia phát triển dự án bằng cách:

1. Fork dự án
2. Tạo branch mới
3. Commit thay đổi
4. Push lên branch
5. Tạo Pull Request

## 📝 License
Dự án này được cấp phép theo giấy phép MIT - xem file [LICENSE](LICENSE) để biết thêm chi tiết.

---
<div align="center">
Tạo bởi xyanua.  
</div>
