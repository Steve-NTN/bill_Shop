from tkinter import *
from tkinter import ttk, messagebox
from main import checkID, getNamePrice, getTotal, insertProduct, deleteProduct, updateProduct
# from setting import newWindow

class MainApplication(Frame):
    def __init__(self, parent, *args, **kwargs):
        self.total, self.indexPro = 0, 1
        #root.protocol("WM_DELETE_WINDOW", self.on_closing)
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        root.bind("<KeyPress>", self.keydown)
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
    

        self.id_pro = StringVar()
        self.entry_id = Entry(root, textvariable=self.id_pro)
        self.entry_id.grid(row=3, column = 0)
        self.qlt = StringVar()
        self.entry_qlt = Entry(root, textvariable=self.qlt)
        self.entry_qlt.grid(row=5, column = 0)

        # Button
        self.button_add = Button(root, text="Thêm đồ", command=self.clickAdd, width=15, height=2).grid(row=6, column=0, rowspan=2)
        self.button_del = Button(root, text="Xóa đồ", command=self.deleteProduct, width=15, height=2).grid(row=8, column=0, rowspan=2)
        self.button_setting = Button(root, text="Cài đặt", command=self.newWindow, height=5, width=20).grid(row=7, column=2, rowspan=2)
        self.button_back = Button(root, text="Tạo mới", command=self.delete, width= 30).grid(row=2, column=1, rowspan=2)
        
        # getSum
        self.labelSum = Label(root, text="Tổng tiền cần thanh toán: *").grid(row=2, column=2)
        self.sum = Entry(root, width = 30)
        self.sum.grid(row=3, column=2)
        self.sum.insert(0, "0")
    
    def keydown(self, e):
        if e.keycode == 37:
            print("Left")
        if e.keycode == 39:
            print("Right")

    # Click button to add product
    def clickAdd(self):
        if self.check():
            i = self.id_pro.get()
            q = self.qlt.get()
            if not checkID(i):
                self.messageToAdd()
            else: 
                self.sum.delete(0, END)
                self.total += int(q)*getNamePrice(i)[1]
                self.tree_main.insert("", "end", text=self.indexPro, values=(getNamePrice(i)[0], getNamePrice(i)[1], q, "{:,}".format(int(q)*getNamePrice(i)[1])))
                self.sum.insert(0, "{:,}".format(int(self.total)))
                self.indexPro += 1
                self.deleteInput() 

    # Get Sum
    def getSum(self):
        self.sum.delete(0, END)
        self.sum.insert(0, "{:,}".format(int(self.total)))

    # Click to clear tree_main       
    def delete(self):     
        listItem = self.tree_main.get_children()
        for i in listItem:
            self.tree_main.delete(i)
        self.sum.delete(0, END)
        self.sum.insert(0, 0)

    # Delete input bar code and quality
    def deleteInput(self):
        self.entry_id.delete(0, END)
        self.entry_qlt.delete(0, END)

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
        if m: self.addWindow()

    # Event when button back
    def deleteProduct(self):
        select = self.tree_main.selection()
        if select != ():
            f = self.tree_main.focus()
            self.total -= int(self.tree_main.item(f)['values'][3].replace(',', ''))
            self.tree_main.delete(select)
            self.getSum()

    def on_closing(self):
        if messagebox.askokcancel("Hỏi", "Bạn có muốn thoát không?"):
            root.destroy()

    # Event when click button setting
    def newWindow(self):
        self.newW = Toplevel(root)
        self.newW.geometry("490x100+500+100")
        self.newW.title("Cập nhập sản phẩm")
        self.newW.resizable(0, 0)
        #self.addIcon = PhotoImage(file="./photo/addIcon.png")
        self.addItem = Button(self.newW, text="Thêm", width=20, height=5, command=self.addWindow).grid(row=0, column=0, padx=10, pady=10)
        self.addItem = Button(self.newW, text = "Xóa", width=20, height=5, command=self.deleteWindow).grid(row=0, column=1, pady=10)
        self.addItem = Button(self.newW, text = "Sửa", width=20, height=5, command=self.updateWindow).grid(row=0, column=2, padx=10, pady=10)

    # Add window
    def addWindow(self):
        self.newAdd = Toplevel(root)
        self.newAdd.geometry("250x170+500+100")
        self.newAdd.resizable(0, 0)
        # Press ID
        self.newAdd.title("Thêm đồ")
        self.addItemID = Label(self.newAdd, text="Mã sản phẩm: *").grid(row=0, column=0, padx=10, pady=10)
        self.addId = StringVar()
        self.addIDEntry = Entry(self.newAdd, textvariable=self.addId)
        self.addIDEntry.grid(row=0, column=1)
        # Press Name
        self.addItemName = Label(self.newAdd, text="Tên sản phẩm: *").grid(row=1, column=0, padx=10, pady=10)
        self.addName = StringVar()
        self.addNameEntry = Entry(self.newAdd, textvariable=self.addName)
        self.addNameEntry.grid(row=1, column=1)
        # Press Price
        self.addItemPrice = Label(self.newAdd, text="Giá sản phẩm: *").grid(row=2, column=0, padx=10, pady=10)
        self.addPrice = StringVar()
        self.addPriceEntry = Entry(self.newAdd, textvariable=self.addPrice)
        self.addPriceEntry.grid(row=2, column=1)
        # Press OK
        self.addButtonCf = Button(self.newAdd, text="Xác nhận", command=self.clickButtonAddCf)
        self.addButtonCf.grid(row=3, column=0, columnspan=2)

    # Check to add product
    def checkAddProduct(self):
        try:
            int(self.addIDEntry.get())
            int(self.addPriceEntry.get())

            if self.addIDEntry.get() != "" and self.addNameEntry.get() != "" and self.addPriceEntry.get() != "" :
                if not checkID(self.addIDEntry.get()):
                    return True
                else :
                    messagebox.showwarning("Cảnh báo", "Mã hàng đã được nhập")
        except ValueError:
            return False
        return False

    # Event when click button addCf
    def clickButtonAddCf(self):
        if self.checkAddProduct():
            insertProduct(self.addIDEntry.get(), self.addNameEntry.get(), int(self.addPriceEntry.get())*1000)
            messagebox.showinfo("Thông báo", "Bạn đã thêm sản phẩm thành công!")
            self.newAdd.destroy()
    
    # Delete window
    def deleteWindow(self):
        self.newDelete = Toplevel(self.newW)
        self.newDelete.geometry("250x100+600+100")
        self.newDelete.register(0, 0)
        self.newDelete.title("Xóa đồ")
        # Press ID
        self.deleteLabelID = Label(self.newDelete, text="Mã sản phẩm: *").grid(row=0, column=0, padx=10, pady=10)
        self.deleteId = StringVar()
        self.deleteIDEntry = Entry(self.newDelete, textvariable=self.deleteId)
        self.deleteIDEntry.grid(row=0, column=1)
        # Press OK
        self.deleteButtonCf = Button(self.newDelete, text="Xác nhận", command=self.deleteProductWithID)
        self.deleteButtonCf.grid(row=2, column=0, columnspan=2)

    def deleteProductWithID(self):
        if not checkID(self.deleteIDEntry.get()):
            messagebox.showwarning("Thông báo", "Chưa nhập hoặc mã sản phẩm không tồn tại.")
        else:
            i = self.deleteIDEntry.get()
            n, p = getNamePrice(i)
            m = messagebox.askokcancel("Cảnh báo", f"Bạn có muốn xóa sản phẩm (Mã: {i} | Tên: {n} | Giá: {p}) không?")
            if m: 
                deleteProduct(i)
                messagebox.showinfo("Thông báo", "Sản phẩm đã được xóa.")
            self.newDelete.destroy()
            self.newW.destroy()

    # Update window
    def updateWindow(self):
        self.newUpdate = Toplevel(self.newW)
        self.newUpdate.geometry("250x100+700+100")
        self.newUpdate.register(0, 0)
        self.newUpdate.title("Sửa thông tin sản phẩm")
        # Press ID
        self.UpdateLabelID = Label(self.newUpdate, text="Mã sản phẩm: *").grid(row=0, column=0, padx=10, pady=10)
        self.updateId = StringVar()
        self.updateIDEntry = Entry(self.newUpdate, textvariable=self.updateId)
        self.updateIDEntry.grid(row=0, column=1)
        # Press OK
        self.updateButtonCf = Button(self.newUpdate, text="Xác nhận", command=self.updateProductWithID)
        self.updateButtonCf.grid(row=2, column=0, columnspan=2)
    # 
    def updateProductWithID(self):
        if not checkID(self.updateIDEntry.get()):
            messagebox.showwarning("Thông báo", "Chưa nhập hoặc mã sản phẩm không tồn tại.")
        else:
            i = self.updateIDEntry.get()
            n, p = getNamePrice(i)
            self.newUpdate.geometry("250x170+700+100")

            self.updateItemName = Label(self.newUpdate, text="Tên sản phẩm: *").grid(row=1, column=0, padx=10, pady=10)
            self.updateName = StringVar()
            self.updateNameEntry = Entry(self.newUpdate, textvariable=self.updateName)
            self.updateNameEntry.insert(0, f"{n}")
            self.updateNameEntry.grid(row=1, column=1)
            # Press Price
            self.updateItemPrice = Label(self.newUpdate, text="Giá sản phẩm: *").grid(row=2, column=0, padx=10, pady=10)
            self.updatePrice = StringVar()
            self.updatePriceEntry = Entry(self.newUpdate, textvariable=self.updatePrice)
            self.updatePriceEntry.insert(0, f"{p}")
            self.updatePriceEntry.grid(row=2, column=1)
            self.updateButtonCf.destroy()
            self.updateButtonCf = Button(self.newUpdate, text="Xác nhận", command=self.updateProductCf)
            self.updateButtonCf.grid(row=3, column=0, columnspan=2)
            
           
    def updateProductCf(self):
        i = self.updateIDEntry.get()
        n, p = getNamePrice(i)
        nn = self.updateNameEntry.get()
        pp = self.updatePriceEntry.get()
        m = messagebox.askokcancel("Cảnh báo", f"Bạn có muốn thay đổi thông tin sản phẩm từ *Tên: {n} | Giá: {int(p)})* thành *Tên: {nn} | Giá: {pp}* không?")
        if m:
            updateProduct(i, nn, int(int(pp)*1000))
            messagebox.showinfo("Thông báo", "Thông tin sản phẩm đã được cập nhập.")
            
if __name__ == "__main__":
    root = Tk()
    root.title("Tính tiền")
    root.geometry("720x700+400+50")
    root.resizable(0, 0)
    MainApplication(root)
    root.mainloop()
    