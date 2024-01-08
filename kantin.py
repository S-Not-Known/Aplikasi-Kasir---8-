from tkinter import *
import customtkinter as CTk
from CTkTable import *
import sqlite3
from CTkMessagebox import CTkMessagebox
from PIL import Image

CTk.set_appearance_mode("light")

class WindowHistory:
    def __init__(self, app, db_name='./database/menu.db'):
        self.app = app
        app.title('Menu')
        app.geometry('800x500')
        # app.configure('white')
        
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

        title_label = CTk.CTkLabel(
            app,
            text='Aplikasi Kasir Kantin UTY',
            font=('Helvetica', 26),
            fg_color="transparent",
            corner_radius=8,
            pady=20
        )
        title_label.pack()

        my_image=CTk.CTkImage(light_image=Image.open("./images/p.jpg"),
                    dark_image=Image.open("./images/p.jpg"),  # Added "./" to the path
                    size=(800, 500))
        image_label = CTk.CTkLabel(
            app, image=my_image, text="", font=('Helvetica', 26),fg_color="transparent" )
        image_label.pack(pady=10)
        image_label.place()

        self.create_button(
            text='Makanan',
            command=self.show_makanan,
            
            x=190, y=150
        )
        self.create_button(
            text='Minuman',
            command=self.show_minuman,
            x=295, y=150
        )
        self.create_button(
            text='Order',
            command=self.order,
            x=400, y=150
        )
        self.create_button(
            text='Riwayat Order',
            command=self.read_orders,
            x=505, y=150
        )

        title_label.pack()
        self.create_button(
            text='Tambah Menu',
            command=self.addMenu,
            x=250, y=250
        )

        self.create_button(
            text='Hapus Menu',
            command=self.deleteMenu,
            x=450, y=250
        )        

    def create_button(self, text, command, x, y):
        button = CTk.CTkButton(
            self.app,
            text=text,
            command=command,
            width=100,
            height=50,
            text_color='#607274',
            fg_color='#FBF9F1',
            
            hover_color='#E5E1DA',
            corner_radius=10
        )
        button.pack(pady=10)
        button.place(x=x, y=y)
        
    def show_makanan(self):
        makanan = CTk.CTkToplevel(self.app)
        makanan.title("Makanan Data")
        makanan.geometry('500x200')
        self.show_table(makanan, 'menu_makanan')

    def show_minuman(self):
        minuman = CTk.CTkToplevel(self.app)
        minuman.title("Minuman Data")
        minuman.geometry('500x200')
        self.show_table(minuman, 'menu_minuman')

    def show_table(self, parent, table_name):
        parent.title(f"{table_name.capitalize()} Data")
        parent.geometry('500x200')
        self.cursor.execute(f'SELECT * FROM {table_name}')
        data = self.cursor.fetchall()
        column_names = [description[0] for description in self.cursor.description]
        values = [column_names] + [list(row) for row in data]
        table = CTkTable(master=parent, row=len(values), column=len(values[0]), values=values)
        table.pack(pady=10)
        table.colors=["yellow", "green"]

    def read_orders(self):
        orders_window = CTk.CTkToplevel(self.app)
        orders_window.title("Order History")
        orders_window.geometry('600x400')
        self.cursor.execute("SELECT * FROM orders")
        data = self.cursor.fetchall()
        column_names = [description[0] for description in self.cursor.description]
        values = [column_names] + [list(row) for row in data]
        orders_table = CTkTable(master=orders_window, row=len(values), column=len(values[0]), values=values)
        orders_table.pack(pady=10)

    def pesan(self):
        jumlah_makanan = int(self.jummakanan.get())
        jumlah_minuman = int(self.jumminuman.get())
        selected_makanan = self.makanan.get()
        selected_minuman = self.minuman.get()
        harga_makanan = self.fetch_harga('menu_makanan', selected_makanan)
        harga_minuman = self.fetch_harga('menu_minuman', selected_minuman)

        if harga_makanan == 0 or harga_minuman == 0:
            CTkMessagebox(title="Error", message="Harga makanan or minuman is zero. Cannot calculate total harga.")
            return

        total_harga = (harga_makanan * jumlah_makanan) + (harga_minuman * jumlah_minuman)
        dialog = CTk.CTkInputDialog(text=f"Total Harga: {total_harga}\nMasukkan jumlah uang pembayaran:", title="Pembayaran")
        bayar = float(dialog.get_input())  # waits for input

        kembalian = bayar - total_harga
        self.cursor.execute(
            "INSERT INTO orders (id_makanan, id_minuman, jumlah_makanan, jumlah_minuman, total_harga, uang_bayar, kembalian) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                self.fetch_menu_options('menu_makanan').index(selected_makanan) + 1,
                self.fetch_menu_options('menu_minuman').index(selected_minuman) + 1,
                jumlah_makanan, jumlah_minuman, total_harga, 
                bayar ,kembalian
            )
        )
        self.connection.commit()
        CTkMessagebox(title="Info", message=f"Pesanan berhasil disimpan!\nTotal Harga: {total_harga}\nBayar: {bayar}\nKembalian: {kembalian}")

    def fetch_harga(self, table_name, selected_item):
        column_name = f"harga_{table_name.split('_')[1]}"
        self.cursor.execute(f"SELECT {column_name} FROM {table_name} WHERE nama_{table_name.split('_')[1]} = ?", (selected_item,))
        harga = self.cursor.fetchone()
        print(harga)
        if harga is not None:
            return harga[0]
        else:
            CTkMessagebox.showerror("Error", f"{selected_item} not found in {table_name}. Cannot fetch harga.")
            return 0
        
    def fetch_menu_options(self, table_name):
                # Mengambil daftar nama menu dari tabel di database
                self.cursor.execute(f"SELECT nama_{table_name.split('_')[1]} FROM {table_name}")
                options = [row[0] for row in self.cursor.fetchall()]
                return options
    
    def addmenuyy(self):
        # Assuming you have appropriate error handling for conversion to int and float
        nama_makanan = self.makanan.get()
        harga_makanan = float(self.hargaMakanan.get())
        
        nama_minuman = self.minuman.get()
        harga_minuman = float(self.hargaMinuman.get())

        # Insert data into menu_makanan table
        self.cursor.execute("INSERT INTO menu_makanan (nama_makanan, harga_makanan) VALUES (?, ?)", (nama_makanan, harga_makanan))
        self.connection.commit()

        # Insert data into menu_minuman table
        self.cursor.execute("INSERT INTO menu_minuman (nama_minuman, harga_minuman) VALUES (?, ?)", (nama_minuman, harga_minuman))
        self.connection.commit()

        CTkMessagebox(title="Info", message="Data Makanan dan Minuman berhasil ditambahkan!")

    def deletemenuyy(self):
        # Assuming you have appropriate error handling for conversion to int and float
        id_makanan = self.makanan.get()
        
        id_minuman = self.minuman.get()
    

        self.cursor.execute("DELETE FROM menu_makanan WHERE id_makanan = ?", (id_makanan,))
        self.connection.commit()
        self.cursor.execute("DELETE FROM menu_minuman WHERE id_minuman = ?", (id_minuman,))
        self.connection.commit()

        CTkMessagebox(title="Info", message="Data Makanan dan Minuman berhasil dihapus!")

    def order(self):
        new = CTk.CTkToplevel(app)
        new.title("Order Baru")
        new.geometry('550x315')

        title_label = CTk.CTkLabel(
            new,
            text='Tambah Order',
            font=('Helvetica', 26),
            fg_color="transparent",
            corner_radius=8,
            pady=20
        )
        title_label.pack()
        makananLabel = CTk.CTkLabel(
            new,
            text='Makanan : ',
            font=('Calibri', 14),
            fg_color=("transparent"),
            corner_radius=8,
            pady=10, padx=50
        )
        self.makanan = CTk.CTkOptionMenu(
            new,
            fg_color='#144272',
            button_color='#0A2647',
            button_hover_color='#205295',
            dropdown_fg_color='#2C74B3',
            dropdown_hover_color='#205295',
            values=self.fetch_menu_options('menu_makanan')
        )
        self.jummakanan = CTk.CTkEntry(
            new,
            placeholder_text='Jumlah Makanan'
        )
        minumanLabel = CTk.CTkLabel(
            new,
            text='Minuman : ',
            font=('Calibri', 14),
            fg_color=("transparent"),
            corner_radius=8,
            pady=10, padx=50
        )
        self.minuman = CTk.CTkOptionMenu(
            new,
            fg_color='#144272',
            button_color='#0A2647',
            button_hover_color='#205295',
            dropdown_fg_color='#2C74B3',
            dropdown_hover_color='#205295',
            values=self.fetch_menu_options('menu_minuman')
        )
        self.jumminuman = CTk.CTkEntry(
            new,
            placeholder_text='Jumlah Minuman'
        )
        self.makanan.place(x=150, y=65)
        makananLabel.pack()
        makananLabel.place(x=10, y=63)
        self.jummakanan.place(x=315, y=65)
        self.minuman.place(x=150, y=125)
        minumanLabel.pack()
        minumanLabel.place(x=10, y=123)
        self.jumminuman.place(x=315, y=125)
        self.button_create = CTk.CTkButton(
            new,
            text='Add',
            command=self.pesan,
            width=100,
            height=50,
            text_color='white',
            hover_color='#205295',
            fg_color='#0A2647',
            corner_radius=15
        )
        self.button_create.pack(pady=10)
        self.button_create.place(x=225, y=214)


    def addMenu(self):
        new = CTk.CTkToplevel(app)
        new.title("Tambah Menu")
        new.geometry('550x315')
        title_label = CTk.CTkLabel(
            new,
            text='Kasir - Tambah Makanan',
            font=('Raleway', 28),
            text_color='black',
            corner_radius=8,
            width=555, 
            height=70
        )
        title_label.place(x=1, y=10)


        makananLabel = CTk.CTkLabel(
            new,
            text='Makanan : ',
            font=('Calibri', 14),
            fg_color=("transparent"),
            corner_radius=8,
            pady=10, padx=50
        )
        self.makanan = CTk.CTkEntry(
                    new,
                    placeholder_text='Nama Makanan'
                )
        self.hargaMakanan = CTk.CTkEntry(
            new,
            placeholder_text='Harga Makanan'
        )
        minumanLabel = CTk.CTkLabel(
            new,
            text='Minuman : ',
            font=('Calibri', 14),
            fg_color=("transparent"),
            corner_radius=8,
            pady=10, padx=50
        )
        self.minuman = CTk.CTkEntry(
            new,
            placeholder_text='Jumlah Minuman'
        )
        self.hargaMinuman = CTk.CTkEntry(
            new,
            placeholder_text='Harga Minuman'
        )
        self.makanan.place(x=150, y=95)
        makananLabel.pack()
        makananLabel.place(x=10, y=93)
        self.hargaMakanan.place(x=315, y=95)

        self.minuman.place(x=150, y=155)
        minumanLabel.pack()
        minumanLabel.place(x=10, y=153)
        self.hargaMinuman.place(x=315, y=155)
        self.button_create = CTk.CTkButton(
            new,
            text='Add',
            command=self.addmenuyy,
            width=100,
            height=50,
            text_color='white',
            hover_color='#205295',
            fg_color='#0A2647',
            corner_radius=15
        )
        self.button_create.pack(pady=10)
        self.button_create.place(x=225, y=214)

    def deleteMenu(self):
        new = CTk.CTkToplevel(app)
        new.title("Delete Menu")
        new.geometry('550x315')
        title_label = CTk.CTkLabel(
            new,
            text='Kasir - Hapus Menu',
            font=('Raleway', 28),
            text_color='black',

            corner_radius=8,
            width=555, 
            height=70
        )

        makananLabel = CTk.CTkLabel(
            new,
            text='Makanan : ',
            font=('Calibri', 14),
            fg_color=("transparent"),
            corner_radius=8,
            pady=10, padx=50
        )

        title_label.place(x=1, y=10)
        self.makanan = CTk.CTkEntry(
            new,
            placeholder_text='Id Makanan'
        )
        minumanLabel = CTk.CTkLabel(
            new,
            text='Minuman : ',
            font=('Calibri', 14),
            fg_color=("transparent"),
            corner_radius=8,
            pady=10, padx=50
        )
        self.minuman = CTk.CTkEntry(
            new,
            placeholder_text='Id Minuman'
        )
        self.makanan.place(x=150, y=95)
        makananLabel.pack()
        makananLabel.place(x=10, y=93)
        self.minuman.place(x=150, y=155)
        minumanLabel.pack()
        minumanLabel.place(x=10, y=153)
        self.button_create = CTk.CTkButton(
            new,
            text='Hapus',
            command=self.deletemenuyy,
            width=100,
            height=50,
            text_color='white',
            hover_color='#BF3131',
            fg_color='#7D0A0A',
            corner_radius=15
        )
        self.button_create.pack(pady=10)
        self.button_create.place(x=225, y=214)

app = CTk.CTk()
WindowHistory(app)
app.mainloop()
