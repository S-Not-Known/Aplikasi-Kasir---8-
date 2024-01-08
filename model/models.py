import sqlite3

# Membuat koneksi ke database
connection = sqlite3.connect('menu.db')
cursor = connection.cursor()

# Membuat tabel menu_makanan
cursor.execute('''
    CREATE TABLE IF NOT EXISTS menu_makanan (
        id_makanan INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_makanan TEXT NOT NULL,
        harga_makanan INTEGER NOT NULL
    )
''')

# Memasukkan data ke tabel menu_makanan
makanan_data = [
    ('Nasi Goreng', 15000),
    ('Mie Goreng', 12000),
    ('Ayam Goreng', 20000),
    ('Ikan Bakar', 25000),
    ('Soto Ayam', 18000)
]
cursor.executemany('INSERT INTO menu_makanan (nama_makanan, harga_makanan) VALUES (?, ?)', makanan_data)

# Membuat tabel menu_minuman
cursor.execute('''
    CREATE TABLE IF NOT EXISTS menu_minuman (
        id_minuman INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_minuman TEXT NOT NULL,
        harga_minuman INTEGER NOT NULL
    )
''')

# Memasukkan data ke tabel menu_minuman
minuman_data = [
    ('Es Teh', 5000),
    ('Es Jeruk', 6000),
    ('Jus Alpukat', 10000),
    ('Kopi Hitam', 7000),
    ('Soda Gembira', 8000)
]
cursor.executemany('INSERT INTO menu_minuman (nama_minuman, harga_minuman) VALUES (?, ?)', minuman_data)

cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id_order INTEGER PRIMARY KEY AUTOINCREMENT,
        id_makanan INTEGER,
        id_minuman INTEGER,
        jumlah_makanan INTEGER,
        jumlah_minuman INTEGER,
        total_harga INTEGER,
        uang_bayar INTEGER,
        kembalian INTEGER,
        FOREIGN KEY (id_makanan) REFERENCES menu_makanan(id_makanan),
        FOREIGN KEY (id_minuman) REFERENCES menu_minuman(id_minuman)
    )
''')
cursor.execute('''
    INSERT INTO orders (id_makanan, id_minuman, jumlah_makanan, jumlah_minuman, total_harga,uang_bayar,kembalian) VALUES
    (1, 2, 2, 3, 74000,80000,6000),
    (3, 5, 1, 2, 54000,10000,46000)
''')
# Menyimpan perubahan dan menutup koneksi
connection.commit()
connection.close()
