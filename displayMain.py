from tkinter import *
from tkinter import ttk, messagebox
from main import getBill, checkID, getNamePrice, insertToBill, getTotal

indexBill = 1; indexPro = 1
dataBill = getBill(indexBill)

class MainApplication(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        # Text heading
        self.text_main = Label(root, text="Hóa Đơn", font=("Arial Bold", 30))
        self.text_main.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Tree view
        self.tree_main = ttk.Treeview(columns=("1", "2", "3","4"), height=20)
        self.tree_main.heading("#0", text="ID")
        self.tree_main.column("#0", width = 30)
        self.tree_main.heading("1", text = "Tên")
        self.tree_main.column("1", anchor="center", minwidth=150, width=250)
        self.tree_main.heading("2", text = "Giá")
        self.tree_main.column("2", anchor="center", minwidth=100, width=100)
        self.tree_main.heading("3", text = "Số lượng")
        self.tree_main.column("3", anchor="center", minwidth=100, width=100)
        self.tree_main.heading("4", text = "Thành tiền")
        self.tree_main.column("4", anchor="center", minwidth=150, width=180)
        self.tree_main.grid(row=1, column=0, columnspan=3, padx= 25)
        
        # ScrollBar
        self.scrollBar = Scrollbar(root, orient="vertical",command=self.tree_main.yview)
        self.scrollBar.grid(row=1, column=2, sticky="NSE")
        self.tree_main.configure(yscrollcommand=self.scrollBar.set)
        
        # Text
        self.pressID = Label(root, text="Nhập mã: *").grid(row = 2, column = 0,  pady=2)
        self.pressQlt = Label(root, text="Nhập số lượng: *").grid(row = 4, column = 0,  pady=2)
        self.indexB = Label(root, text=f"Hóa đơn hiện tại là: {indexBill}",).grid(row = 2, column = 1)
        

        # Insert data
        for i in range(len(dataBill)):
            global indexPro
            self.tree_main.insert("", 'end',text = indexPro, value=(dataBill[i][0], dataBill[i][1], dataBill[i][2], dataBill[i][3]))
            indexPro += 1

        self.id_pro = StringVar()
        self.entry_id = Entry(root, textvariable=self.id_pro).grid(row=3, column = 0)
        self.qlt = StringVar()
        self.qlt_qlt = Entry(root, textvariable=self.qlt).grid(row=5, column = 0)

        # Button
        self.button_add = Button(root, text="Thêm đồ", command=self.clickAdd, width=15, height=2).grid(row=6, column=0, rowspan=2)
        self.button_del = Button(root, text="Xóa đồ", command=self.delete, width=15, height=2).grid(row=8, column=0, rowspan=2)
        self.button_setting = Button(root, text="Cài đặt", command=self.getSum, height=2).grid(row=6, column=1, rowspan=1)
        self.button_sum = Button(root, text="Tính tiền", command=self.getSum, width = 20).grid(row=3, column=2, rowspan=2)
        self.button_back = Button(root, text="Trước", command=self.getSum).grid(row=4, column=1)
        self.button_next = Button(root, text="  Sau  ", command=self.getSum).grid(row=5, column=1)
        
        # getSum
        self.sum = Entry(root, width = 30)
        self.sum.grid(row=2, column=2, rowspan = 2)

    # Get sum cost
    def getSum(self):
        self.sum.delete(0, END)       
        self.sum.insert(0, getTotal(indexBill))

    # Click button to add product
    def clickAdd(self):
        if self.check():
            i = self.id_pro.get()
            q = self.qlt.get()
            if not checkID(i):
                self.messageToAdd()
            else: 
                self.tree_main.insert("", "end", text=indexPro, values=(getNamePrice(i)[0], getNamePrice(i)[1], q, int(q)*getNamePrice(i)[1]))
                self.sum.delete(0, END)
                insertToBill(indexBill, i, q)  
    # Click to clear tree_main       
    def delete(self):     
        list = self.tree_main.get_children()
        for i in list:
            self.tree_main.delete(i)

    # Check can be add product
    def check(self):
        try:
            int(self.qlt.get())
            if self.id_pro.get() != "" and self.qlt.get() != "":
                return True    
        except ValueError:
            return False
        return False

    # Event when id_product not availble
    
    def messageToAdd(self):
        m = messagebox.askokcancel("Thông báo","Mã sản phẩm chưa có. Thêm vào?")
        print("Add Product API" if m els "Cancle")

if __name__ == "__main__":
    root = Tk()
    root.title("Tính tiền")
    root.geometry("720x700")
    MainApplication(root)
    root.mainloop()