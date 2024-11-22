import tkinter as tk
from tkinter import messagebox, ttk


users = {} 
students = []
majors = ["Công nghệ thông tin", "Kinh tế", "Kỹ thuật", "Y dược"]

def register_user():
    username = entry_username.get().strip()
    password = entry_password.get().strip()

    if not username or not password:
        messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu!")
        return

    if username in users:
        messagebox.showerror("Lỗi", "Tài khoản đã tồn tại!")
        return

    users[username] = password
    messagebox.showinfo("Thành công", "Đăng ký thành công! Vui lòng đăng nhập.")
    clear_login_inputs()

def login_user():
    username = entry_username.get().strip()
    password = entry_password.get().strip()

    if users.get(username) == password:
        messagebox.showinfo("Thành công", "Đăng nhập thành công!")
        login_window.destroy()
        show_main_window()
    else:
        messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không chính xác!")

def clear_login_inputs():
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)

def add_student():
    name = entry_name.get().strip()
    gender = gender_var.get()
    mssv = entry_mssv.get().strip()
    major = major_var.get()

    if not name or not mssv or not major:
        messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin!")
        return

    for student in students:
        if student["MSSV"] == mssv:
            messagebox.showerror("Lỗi", "MSSV đã tồn tại!")
            return

    students.append({"Họ và tên": name, "Giới tính": gender, "MSSV": mssv, "Chuyên ngành": major})
    update_student_table()
    clear_student_inputs()

def update_student_table():
    for row in student_table.get_children():
        student_table.delete(row)

    for student in students:
        student_table.insert("", "end", values=(student["Họ và tên"], student["Giới tính"], student["MSSV"], student["Chuyên ngành"]))

def clear_student_inputs():
    entry_name.delete(0, tk.END)
    entry_mssv.delete(0, tk.END)
    gender_var.set("Nam")
    major_var.set(majors[0])

def delete_student():
    selected_item = student_table.selection()
    if not selected_item:
        messagebox.showerror("Lỗi", "Vui lòng chọn sinh viên để xóa!")
        return

    selected_student = student_table.item(selected_item)["values"]
    mssv_to_delete = str(selected_student[2]).strip()  # Lấy MSSV của sinh viên cần xóa

    global students
    students = [student for student in students if student["MSSV"] != mssv_to_delete]

    update_student_table()

    clear_student_inputs()
    messagebox.showinfo("Thành công", "Xóa sinh viên thành công!")


def edit_student():
    selected_item = student_table.selection()
    if not selected_item:
        messagebox.showerror("Lỗi", "Vui lòng chọn sinh viên để sửa!")
        return

    selected_student = student_table.item(selected_item)["values"]
    old_mssv = str(selected_student[2]).strip()

    new_name = entry_name.get().strip()
    new_gender = gender_var.get()
    new_major = major_var.get()
    new_mssv = entry_mssv.get().strip() 

    if not new_name or not new_mssv or not new_major:
        messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
        return

    for student in students:
        if student["MSSV"] == new_mssv and student["MSSV"] != old_mssv:
            messagebox.showerror("Lỗi", f"MSSV {new_mssv} đã tồn tại!")
            return

    for student in students:
        if student["MSSV"] == old_mssv:
            student["Họ và tên"] = new_name
            student["Giới tính"] = new_gender
            student["Chuyên ngành"] = new_major
            student["MSSV"] = new_mssv 
            break
    else:
        messagebox.showerror("Lỗi", f"Không tìm thấy sinh viên với MSSV: {old_mssv}")
        return

    update_student_table()

    clear_student_inputs()
    messagebox.showinfo("Thành công", "Thông tin sinh viên đã được sửa!")

def add_major():
    new_major = entry_major.get().strip()
    if not new_major:
        messagebox.showerror("Lỗi", "Vui lòng nhập tên chuyên ngành!")
        return

    if new_major in majors:
        messagebox.showerror("Lỗi", "Chuyên ngành đã tồn tại!")
        return

    majors.append(new_major)
    update_major_table()
    update_major_dropdown()
    clear_major_input()

def delete_major():
    selected_item = major_table.selection()
    if not selected_item:
        messagebox.showerror("Lỗi", "Vui lòng chọn chuyên ngành để xóa!")
        return

    selected_major = major_table.item(selected_item)["values"][0]
    if selected_major in majors:
        majors.remove(selected_major)

    update_major_table()
    update_major_dropdown()

def update_major_table():
    for row in major_table.get_children():
        major_table.delete(row)

    for major in majors:
        major_table.insert("", "end", values=(major,))

def update_major_dropdown():
    major_var.set(majors[0])
    combobox_major["values"] = majors

def clear_major_input():
    entry_major.delete(0, tk.END)

def show_main_window():
    global entry_name, entry_mssv, gender_var, major_var, student_table, entry_major, major_table, combobox_major

    main_window = tk.Tk()
    main_window.title("Quản lý sinh viên và chuyên ngành")

    frame_student = tk.LabelFrame(main_window, text="Quản lý sinh viên")
    frame_student.pack(pady=10, padx=10, fill="x")

    tk.Label(frame_student, text="Họ và tên:").grid(row=0, column=0, padx=5, pady=5)
    entry_name = tk.Entry(frame_student, width=25)
    entry_name.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_student, text="Giới tính:").grid(row=1, column=0, padx=5, pady=5)
    gender_var = tk.StringVar(value="Nam")
    tk.Radiobutton(frame_student, text="Nam", variable=gender_var, value="Nam").grid(row=1, column=1, sticky="w")
    tk.Radiobutton(frame_student, text="Nữ", variable=gender_var, value="Nữ").grid(row=1, column=2, sticky="w")

    tk.Label(frame_student, text="MSSV:").grid(row=2, column=0, padx=5, pady=5)
    entry_mssv = tk.Entry(frame_student, width=25)
    entry_mssv.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame_student, text="Chuyên ngành:").grid(row=3, column=0, padx=5, pady=5)
    major_var = tk.StringVar(value=majors[0])
    combobox_major = ttk.Combobox(frame_student, textvariable=major_var, values=majors, state="readonly")
    combobox_major.grid(row=3, column=1, padx=5, pady=5)

    tk.Button(frame_student, text="Thêm", command=add_student).grid(row=4, column=0, padx=5, pady=5)
    tk.Button(frame_student, text="Sửa", command=edit_student).grid(row=4, column=1, padx=5, pady=5)
    tk.Button(frame_student, text="Xóa", command=delete_student).grid(row=4, column=2, padx=5, pady=5)

    student_table = ttk.Treeview(frame_student, columns=("Họ và tên", "Giới tính", "MSSV", "Chuyên ngành"), show="headings", height=10)
    for col in ("Họ và tên", "Giới tính", "MSSV", "Chuyên ngành"):
        student_table.heading(col, text=col)
        student_table.column(col, width=150)
    student_table.grid(row=5, column=0, columnspan=3, pady=10)

    frame_major = tk.LabelFrame(main_window, text="Quản lý chuyên ngành")
    frame_major.pack(pady=10, padx=10, fill="x")

    tk.Label(frame_major, text="Tên chuyên ngành:").grid(row=0, column=0, padx=5, pady=5)
    entry_major = tk.Entry(frame_major, width=25)
    entry_major.grid(row=0, column=1, padx=5, pady=5)

    tk.Button(frame_major, text="Thêm", command=add_major).grid(row=1, column=0, padx=5, pady=5)
    tk.Button(frame_major, text="Xóa", command=delete_major).grid(row=1, column=1, padx=5, pady=5)

    major_table = ttk.Treeview(frame_major, columns=("Tên chuyên ngành",), show="headings", height=5)
    major_table.heading("Tên chuyên ngành", text="Tên chuyên ngành")
    major_table.column("Tên chuyên ngành", width=200)
    major_table.grid(row=2, column=0, columnspan=2, pady=10)

    update_major_table()

    main_window.mainloop()

login_window = tk.Tk()
login_window.title("Đăng nhập/Đăng ký")

tk.Label(login_window, text="Tên đăng nhập:").grid(row=0, column=0, padx=5, pady=5)
entry_username = tk.Entry(login_window, width=25)
entry_username.grid(row=0, column=1, padx=5, pady=5)

tk.Label(login_window, text="Mật khẩu:").grid(row=1, column=0, padx=5, pady=5)
entry_password = tk.Entry(login_window, show="*", width=25)
entry_password.grid(row=1, column=1, padx=5, pady=5)

tk.Button(login_window, text="Đăng nhập", command=login_user).grid(row=2, column=0, padx=5, pady=5)
tk.Button(login_window, text="Đăng ký", command=register_user).grid(row=2, column=1, padx=5, pady=5)

login_window.mainloop()