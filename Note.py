import tkinter as tk

# 1. Khởi tạo cửa sổ chính (Root Window)
root = tk.Tk()

# 2. Đặt tiêu đề cho cửa sổ
root.title("Note") 

root.geometry("800x600") # Đặt kích thước mặc định

from tkinter import filedialog, messagebox # Thêm filedialog và messagebox

# Bạn có thể đặt kích thước mặc định cho cửa sổ (tùy chọn)
# root.geometry("800x600")

# Vòng lặp chính của Tkinter (cần thiết để cửa sổ hiển thị và phản hồi sự kiện)
# Bạn sẽ đặt nó ở cuối file code.
# root.mainloop()

# Biến này để lưu trữ đường dẫn file hiện tại đang được mở/lưu
current_file = None 

# Hàm Mới (New)
def new_file():
    global current_file
    # Hỏi người dùng lưu file hiện tại nếu có thay đổi (optional, advanced)
    # Tạm thời, chỉ cần xóa nội dung
    
    # 1. Xóa toàn bộ nội dung trong Text Area
    text_area.delete("1.0", tk.END) 
    
    # 2. Reset tiêu đề cửa sổ và biến current_file
    root.title("Text Editor - Untitled")
    current_file = None

# Hàm Mở (Open)
def open_file():
    global current_file
    
    # 1. Mở hộp thoại chọn file
    filepath = filedialog.askopenfilename(
        defaultextension=".txt", 
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    
    if filepath:
        # Cập nhật đường dẫn file hiện tại và tiêu đề cửa sổ
        current_file = filepath
        root.title(f"Text Editor - {filepath.split('/')[-1]}")
        
        # 2. Xóa nội dung Text Area cũ
        text_area.delete("1.0", tk.END)
        
        # 3. Đọc nội dung file và chèn vào Text Area
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
                text_area.insert("1.0", content)
        except Exception as e:
            messagebox.showerror("Error", f"Không thể đọc file: {e}")

# Hàm Lưu (Save)
def save_file():
    global current_file
    
    # Nếu file chưa từng được lưu hoặc là file mới, gọi Save As
    if not current_file:
        save_as_file()
    else:
        # Nếu đã có đường dẫn, lưu trực tiếp vào file đó
        try:
            # Lấy toàn bộ nội dung từ Text Area
            content = text_area.get("1.0", tk.END) 
            
            # Ghi nội dung ra file
            with open(current_file, "w", encoding="utf-8") as file:
                file.write(content)
            
            messagebox.showinfo("Success", f"Đã lưu file: {current_file}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Lỗi khi lưu file: {e}")

# Hàm Lưu Với Tên Khác (Save As)
def save_as_file():
    global current_file
    
    # Mở hộp thoại lưu file
    filepath = filedialog.asksaveasfilename(
        defaultextension=".txt", 
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    
    if filepath:
        # Cập nhật đường dẫn file hiện tại
        current_file = filepath
        root.title(f"Text Editor - {filepath.split('/')[-1]}")
        
        # Gọi hàm lưu file để thực hiện ghi nội dung
        save_file()

# Hàm Thoát (Exit)
def exit_app():
    # Thêm logic kiểm tra xem có thay đổi chưa lưu hay không (optional)
    root.quit()

# Hàm Cắt (Cut)
def cut_text():
    # Mô phỏng phím tắt Ctrl+X
    text_area.event_generate("<<Cut>>") 

# Hàm Sao chép (Copy)
def copy_text():
    # Mô phỏng phím tắt Ctrl+C
    text_area.event_generate("<<Copy>>")

# Hàm Dán (Paste)
def paste_text():
    # Mô phỏng phím tắt Ctrl+V
    text_area.event_generate("<<Paste>>")

# Thêm chức năng Undo/Redo (Nếu bạn đã thiết lập undo=True khi tạo text_area)
def undo_text():
    # Mô phỏng phím tắt Ctrl+Z
    text_area.event_generate("<<Undo>>")

def redo_text():
    # Mô phỏng phím tắt Ctrl+Y (hoặc Ctrl+Shift+Z)
    text_area.event_generate("<<Redo>>")
# --- Bắt đầu tạo các thành phần mới ---

# 2. Tạo Thanh Cuộn Dọc
scrollbar = tk.Scrollbar(root)

# 3. Tạo Vùng Soạn thảo (Text Widget)
text_area = tk.Text(
    root,
    yscrollcommand=scrollbar.set,  # Gắn lệnh cuộn (scrollbar.set) vào Text
    font=("Arial", 12),
    undo=True # Kích hoạt chức năng Undo/Redo cơ bản
)

# 4. Gắn kết hai chiều (Hai thành phần nói chuyện với nhau)
# Khi Scrollbar được kéo, nó sẽ điều khiển Text
scrollbar.config(command=text_area.yview)

# 5. Bố cục (Sử dụng pack)
# Đặt thanh cuộn ở bên phải và trải dài theo chiều dọc
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Đặt vùng soạn thảo, chiếm toàn bộ không gian còn lại và tự mở rộng
text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) 

# Tạo Menu Bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar) # Gắn Menu Bar vào cửa sổ chính

# Tạo Menu "File"
file_menu = tk.Menu(menu_bar, tearoff=0)

# Thêm Menu "File" vào Menu Bar
menu_bar.add_cascade(label="File", menu=file_menu)

# Thêm các mục vào Menu "File" và gán hàm xử lý (command)
file_menu.add_command(label="New (Mới)", command=new_file)
file_menu.add_command(label="Open (Mở)", command=open_file)
file_menu.add_command(label="Save (Lưu)", command=save_file)
file_menu.add_command(label="Save As (Lưu với tên khác)", command=save_as_file)

# Thêm đường phân cách
file_menu.add_separator()

file_menu.add_command(label="Exit (Thoát)", command=exit_app)

# Tạo Menu "Edit"
edit_menu = tk.Menu(menu_bar, tearoff=0)

# Thêm Menu "Edit" vào Menu Bar (menu_bar đã được tạo ở bước trước)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Thêm các mục vào Menu "Edit"
edit_menu.add_command(label="Undo (Hoàn tác)", command=undo_text)
edit_menu.add_command(label="Redo (Làm lại)", command=redo_text)
edit_menu.add_separator()
edit_menu.add_command(label="Cut (Cắt)", command=cut_text)
edit_menu.add_command(label="Copy (Sao chép)", command=copy_text)
edit_menu.add_command(label="Paste (Dán)", command=paste_text)

# Cần biến toàn cục để lưu trữ cửa sổ tìm kiếm và vị trí con trỏ
find_toplevel = None
last_search_idx = "1.0" # Bắt đầu tìm kiếm từ đầu

def find_text_dialog():
    global find_toplevel, last_search_idx

    # Kiểm tra nếu cửa sổ đã tồn tại, đưa nó lên trên cùng
    if find_toplevel and find_toplevel.winfo_exists():
        find_toplevel.lift()
        return

    # Tạo cửa sổ phụ
    find_toplevel = tk.Toplevel(root)
    find_toplevel.title("Find & Replace")
    find_toplevel.geometry("350x150")
    
    # Biến lưu trữ chuỗi tìm kiếm và thay thế
    search_var = tk.StringVar()
    replace_var = tk.StringVar()

    # Tạo các nhãn và trường nhập liệu
    tk.Label(find_toplevel, text="Find:").grid(row=0, column=0, padx=5, pady=5)
    search_entry = tk.Entry(find_toplevel, textvariable=search_var, width=30)
    search_entry.grid(row=0, column=1, padx=5, pady=5)
    
    tk.Label(find_toplevel, text="Replace:").grid(row=1, column=0, padx=5, pady=5)
    replace_entry = tk.Entry(find_toplevel, textvariable=replace_var, width=30)
    replace_entry.grid(row=1, column=1, padx=5, pady=5)
    
    # Các nút lệnh
    tk.Button(find_toplevel, text="Find Next", command=lambda: find_next(search_var.get())).grid(row=2, column=0, padx=5, pady=5)
    tk.Button(find_toplevel, text="Replace", command=lambda: replace_once(search_var.get(), replace_var.get())).grid(row=2, column=1, padx=5, pady=5)
    tk.Button(find_toplevel, text="Replace All", command=lambda: replace_all(search_var.get(), replace_var.get())).grid(row=2, column=2, padx=5, pady=5)
    
    search_entry.focus_set()

# Hàm tìm kiếm thực tế
def find_next(search_string):
    global last_search_idx
    if not search_string: return

    # Xóa highlight cũ
    text_area.tag_remove('highlight', '1.0', tk.END)

    # Vị trí bắt đầu tìm kiếm (từ vị trí tìm thấy lần trước)
    start_index = last_search_idx
    
    # Tìm kiếm chuỗi
    idx = text_area.search(search_string, start_index, stopindex=tk.END, nocase=True) 

    if idx:
        end_index = f"{idx}+{len(search_string)}c" # Vị trí kết thúc
        text_area.tag_add('highlight', idx, end_index)
        text_area.tag_config('highlight', background='yellow', foreground='black')
        text_area.see(idx) # Cuộn đến vị trí tìm thấy

        # Cập nhật vị trí bắt đầu tìm kiếm lần tiếp theo (+1 ký tự)
        last_search_idx = f"{idx}+1c"
    else:
        # Nếu không tìm thấy, reset vị trí tìm kiếm về đầu và báo cáo
        last_search_idx = "1.0"
        messagebox.showinfo("Search", f"Không tìm thấy '{search_string}'")

# Hàm thay thế một lần
def replace_once(search_string, replace_string):
    if not search_string: return

    # Kiểm tra xem có highlight (tìm thấy) nào không
    ranges = text_area.tag_ranges('highlight')
    if ranges:
        start_idx = ranges[0]
        end_idx = ranges[1]
        
        # Thay thế văn bản đã highlight
        text_area.delete(start_idx, end_idx)
        text_area.insert(start_idx, replace_string)
        
        # Xóa highlight và tiếp tục tìm kiếm lần tiếp theo
        text_area.tag_remove('highlight', '1.0', tk.END)
        find_next(search_string)

# Hàm thay thế tất cả
def replace_all(search_string, replace_string):
    if not search_string: return
    
    # Xóa highlight cũ
    text_area.tag_remove('highlight', '1.0', tk.END)
    
    count = 0
    start_index = "1.0"
    
    while True:
        # Tìm kiếm chuỗi (không phân biệt chữ hoa/thường)
        idx = text_area.search(search_string, start_index, stopindex=tk.END, nocase=True)
        
        if idx:
            end_index = f"{idx}+{len(search_string)}c"
            
            # Thực hiện thay thế
            text_area.delete(idx, end_index)
            text_area.insert(idx, replace_string)
            
            # Cập nhật vị trí bắt đầu tìm kiếm (+ độ dài của chuỗi thay thế)
            start_index = f"{idx}+{len(replace_string)}c"
            count += 1
        else:
            break

    messagebox.showinfo("Replace", f"Đã thay thế {count} lần.")

# TẠO MENU ĐIỀU KHIỂN (CONTROL)
control_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Control", menu=control_menu)

# ... [Các lệnh Undo, Redo, Cut, Copy, Paste] ...
control_menu.add_separator()
control_menu.add_command(label="Find & Replace (Tìm & Thay thế)", command=find_text_dialog)

# --- THIẾT LẬP PHÍM TẮT (BINDINGS) ---
# <Control-s> là tổ hợp phím Ctrl + S

# 1. Quản lý File
root.bind('<Control-n>', lambda event: new_file())     # Ctrl + N: Mới
root.bind('<Control-o>', lambda event: open_file())    # Ctrl + O: Mở
root.bind('<Control-s>', lambda event: save_file())    # Ctrl + S: Lưu
root.bind('<Control-Key-S>', lambda event: save_as_file()) # Ctrl + Shift + S: Lưu với tên khác

# 2. Tìm kiếm
root.bind('<Control-f>', lambda event: find_text_dialog()) # Ctrl + F: Tìm kiếm

# 3. Thoát
root.bind('<Control-q>', lambda event: exit_app())     # Ctrl + Q: Thoát

# VÒNG LẶP CHÍNH
root.mainloop()