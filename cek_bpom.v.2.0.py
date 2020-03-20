from tkinter import Tk, Label, OptionMenu, StringVar, Entry, Button
from tkinter.ttk import Treeview, Scrollbar
import requests
from bs4 import BeautifulSoup
from tkinter.messagebox import askquestion, showinfo

# untuk setting form_utama
class application:
    katagori = [
        "Nomer Registrasi",
        "Nama Produk",
        "Merk",
        "Jumlah & Kemasan",
        "Bentuk Sediaan",
        "Komposisi",
        "Nama Pendaftar"
    ]

    def __init__(self, root):
        self.root = root
        self.root.title("Cek Barang Terdaftar Di BPOM")
        self.root.resizable(False, False)
        self.root.geometry("1220x490")
        self.set_gui(self.root)
        self.root.protocol('WM_DELETE_WINDOW', self.quit)

    # menangani exit user
    def quit(self):
        self.berjalan = False
        cek = askquestion("pemberitahuan", "Apakah Kamu yakin akan keluar?")
        if cek == "yes":
            self.root.destroy()

    class set_gui:
        # deklarasi semua komponen yang ada
        input_katagori = OptionMenu
        input_key = Entry
        variable = StringVar
        table = Treeview
        btn_back = Button
        btn_next = Button
        txt_halaman = Entry
        txt_jml_halaman = Label
        txt_tampil = Entry

        def __init__(self, root):
            self.root = root

            # membuat kolom untuk menentukan data yang akan di cari
            Label(self.root, text="Cari Berdasarkan : ").place(x=10, y=10)

            # membuat menu dropdown untuk mencari data berdasarkan katagori
            application.set_gui.variable = StringVar(self.root)
            application.set_gui.variable.set(application.katagori[0])
            application.set_gui.input_katagori = OptionMenu(self.root, application.set_gui.variable, *application.katagori)
            application.set_gui.input_katagori.place(x=10, y=30)

            # membuat kolom untuk cari
            Label(self.root, text="Keyword : ").place(x=10, y=65)
            application.set_gui.input_key = Entry(self.root)
            application.set_gui.input_key.place(x=10, y=85)

            #menangani keypress di kolom cari
            application.set_gui.input_key.bind('<Key>', application.command().key_search)

            # menampilkan tombol utuk memulai pencarian
            Button(self.root, text="Cari", command=application.command().cari_data).place(x=10, y=110)

            # membuat table
            self.buat_table()

            # membuat fungsi perpindahan halaman

            # membuat button untuk tombol kembali
            application.set_gui.btn_back = Button(self.root)
            application.set_gui.btn_back['text'] = "<< Kembali"
            application.set_gui.btn_back['state'] = "disable"
            application.set_gui.btn_back['command'] = application.command().prev_halaman
            application.set_gui.btn_back.place(x=400, y=390)

            # membuat kolom halaman
            application.set_gui.txt_halaman = Entry(self.root)
            application.set_gui.txt_halaman['width'] = 4
            application.set_gui.txt_halaman.place(x=510, y=395)
            application.set_gui.txt_halaman.insert(0, "0")

            # menangani keypress di kolom halaman
            application.set_gui.txt_halaman.bind('<Key>', application.command().key_got_to)

            Label(self.root,text=" Dari : ").place(x=540, y=395)
            application.set_gui.txt_jml_halaman = Label(self.root)
            application.set_gui.txt_jml_halaman['text'] = "1"
            application.set_gui.txt_jml_halaman.place(x=580, y=395)
            Label(self.root, text=" Halaman").place(x=630, y=395)

            # membuat tombol utnuk next
            application.set_gui.btn_next = Button(self.root)
            application.set_gui.btn_next['text'] = "Next >>"
            application.set_gui.btn_next['state'] = "disable"
            application.set_gui.btn_next['command'] = application.command().next_halaman
            application.set_gui.btn_next.place(x=715, y=390)

            # membuat kolom utuk setting jml data yang ditampilkan
            Label(self.root, text="Jumlah data yang ditampilkan : ").place(x=10, y=390)
            application.set_gui.txt_tampil = Entry(self.root)
            application.set_gui.txt_tampil.insert(0, "10")
            application.set_gui.txt_tampil['width'] = 6
            application.set_gui.txt_tampil.place(x=220, y=390)

            #menangani keypress di kolom tampil
            application.set_gui.txt_tampil.bind('<Key>', application.command().key_search)

            # copyrigth
            Label(self.root, text="Create By : Safrudin").place(x=500, y=440)
            Label(self.root, text="Email : bening244342@secmail.pro").place(x=445, y=460)

        def buat_table(self):
            application.set_gui.table = Treeview(self.root, columns=("nomer_regis", "terbit", "nama", "merk", "kemasan", "produsen",
                                                                     "lokasi"), height=10)

            # membuat tombol scrol atas ke bawah
            ybs = Scrollbar(self.root, orient='vertical', command=application.set_gui.table.yview)
            application.set_gui.table.configure(yscroll=ybs.set)  # setting scroll bal vertical
            ybs.place(x=1190, y=150, height=222)

            # membuat tombol utuk scrol kanan ke kiri
            xbs = Scrollbar(self.root, orient='horizontal', command=application.set_gui.table.xview)
            application.set_gui.table.configure(xscroll=xbs.set)
            xbs.place(x=10, y=371, width=1180)

            application.set_gui.table.configure()

            # setting header table

            # setting column id
            application.set_gui.table.heading('#0', text='ID')
            application.set_gui.table.column('#0', minwidth=40, width=40)

            # setting column nomer_regis
            application.set_gui.table.heading('nomer_regis', text='Nomer Regristasi')
            application.set_gui.table.column('nomer_regis', minwidth=150, width=150)

            # setting column terbit
            application.set_gui.table.heading('terbit', text="Tgl Terbit")
            application.set_gui.table.column('terbit', minwidth=100, width=100)

            # setting column nama
            application.set_gui.table.heading('nama', text='Nama Produk')
            application.set_gui.table.column('nama', minwidth=300, width=300)

            # setting column merk
            application.set_gui.table.heading('merk', text='Merk')
            application.set_gui.table.column('merk', minwidth=150, width=150)

            # setting column kemasan
            application.set_gui.table.heading('kemasan', text='Kemasan')
            application.set_gui.table.column('kemasan', minwidth=150, width=150)

            # setting column produsen
            application.set_gui.table.heading('produsen', text='Produsen')
            application.set_gui.table.column('produsen', minwidth=150, width=150)

            # setting column lokasi
            application.set_gui.table.heading('lokasi', text='Lokasi')
            application.set_gui.table.column('lokasi', minwidth=150, width=150)

            application.set_gui.table.place(x=10, y=150)

    class command:

        # memulai pencarian
        def cari_data(self):
            #membersihkan table
            self.kosong_table()

            katagori = application.katagori.index(application.set_gui.variable.get())
            keyword = application.set_gui.input_key.get()
            produk = self.cek_bpom(str(katagori), keyword, "1")

            # memasukkan data kedalam table
            self.input_data_ketable(produk)

            #enable btn_next
            max_halaman = application.set_gui.txt_jml_halaman['text']
            halaman = application.set_gui.txt_halaman.get()
            if int(max_halaman) > int(halaman):
                application.set_gui.btn_next['state'] = 'normal'
            else:
                application.set_gui.btn_next['state'] = 'disable'
                application.set_gui.btn_back['state'] = 'disable'

        # membaca halaman berikutnya
        def next_halaman(self):
            # membersihkan table
            self.kosong_table()

            halaman_sekarang = application.set_gui.txt_halaman.get()
            max_halaman = int(application.set_gui.txt_jml_halaman['text'])
            next = int(halaman_sekarang) + 1
            if next == max_halaman:
                application.set_gui.btn_next['state'] = 'disable'

            katagori = application.katagori.index(application.set_gui.variable.get())
            keyword = application.set_gui.input_key.get()
            produk = self.cek_bpom(str(katagori), keyword, str(next))

            # memasukkan data kedalam table
            self.input_data_ketable(produk)

            # enable btn_next
            application.set_gui.btn_back['state'] = "normal"

            #menambahkan halaman
            application.set_gui.txt_halaman.delete(0, 'end')
            application.set_gui.txt_halaman.insert(0, next)

        # membaca halaman sebelumnya
        def prev_halaman(self):
            application.set_gui.btn_next['state'] = 'normal'
            # membersihkan table
            self.kosong_table()

            halaman_sekarang = application.set_gui.txt_halaman.get()
            prev = int(halaman_sekarang) - 1
            if prev <= 0:
                application.set_gui.btn_back['state'] = 'disable'

            katagori = application.katagori.index(application.set_gui.variable.get())
            keyword = application.set_gui.input_key.get()
            produk = self.cek_bpom(str(katagori), keyword, str(prev))

            # memasukkan data kedalam table
            self.input_data_ketable(produk)

            #mengupdate halaman
            application.set_gui.txt_halaman.delete(0, 'end')
            application.set_gui.txt_halaman.insert(0, prev)

        # membuka halaman yang diinginkan
        def go_to_halaman(self):
            # mengosongkan table
            self.kosong_table()

            katagori = application.katagori.index(application.set_gui.variable.get())
            keyword = application.set_gui.input_key.get()
            page = application.set_gui.txt_halaman.get()
            produk = self.cek_bpom(str(katagori), keyword, str(page))

            # memasukkan data kedalam table
            self.input_data_ketable(produk)

            # update tompol next dan prev
            if page == application.set_gui.txt_jml_halaman['text']:
                application.set_gui.btn_next['state'] = 'disable'

            if int(page) == 1 or int(page) == 0:
                application.set_gui.btn_back['state'] = 'disable'

        # melakukan scraping ke website bpom
        def cek_bpom(self, katagori, keyword, page):
            id = '234kjhk43h53hk5h345h345'
            jml_tampil = application.set_gui.txt_tampil.get()

            # setting header
            header = {
                "user-agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1"}

            req = requests.session()
            req.cookies.update({"PHPSESSID": id})

            url = "http://ceknie.pom.go.id/index.php/home/produk/" + id + "/all/row/" + str(jml_tampil) + "/page/" + str(page) + "/order/4/DESC/search/" + katagori + "/" + keyword

            koneksi = False
            try:
                data = req.get(url, headers=header)
                koneksi = True
            except:
                showinfo('Warning', 'Kamu tidak terhubung ke internet!')
                koneksi = False

            if koneksi:
                data = data.text

                data = BeautifulSoup(data, "lxml")
                table = data.table

                # mendapatkan total halaman yang tersedia
                total = data.find(id="tb_total").text
                application.set_gui.txt_jml_halaman['text'] = str(total)
                application.set_gui.txt_halaman.delete(0, "end")
                application.set_gui.txt_halaman.insert(0, page)

                data_produk = []

                for baris in table.find_all("tr"):
                    sub_data = []
                    for isi in baris.find_all("td"):
                        isi = self.pisah_html(isi)
                        sub_data = sub_data + isi
                    if len(sub_data) != 0:
                        data_produk.append(sub_data)

                return data_produk
            else:
                data_produk = ['Tidak ada koneksi Internet']
                return data_produk

        # memisahkan tag html dari data
        def pisah_html(self,text):
            data_kata = []
            if len(text) == 1:
                data_kata.append(text.text)
            elif len(text) == 2:
                for data in text:
                    if len(data) > 5:
                        data_kata.append(data)
                    else:
                        for isi in data:
                            if len(isi) > 5:
                                isi = isi.split(":")
                                if len(isi) == 2:
                                    isi = isi[1]
                                else:
                                    isi = isi[0]
                                data_kata.append(isi)
            return data_kata

        # memasukkan data kedalam table
        def input_data_ketable(self, data = []):
            for sub_data in data:
                if len(sub_data) == 6:
                    sub_data.insert(1, "-")
                elif len(sub_data) == 5:
                    sub_data.insert(1, "-")
                    sub_data.insert(6, "-")
                else:
                    sub_data = ['Data tidak ada', 'Data tidak ada', 'Data tidak ada', 'Data tidak ada',
                                'Data tidak ada',
                                'Data tidak ada', 'Data tidak ada']
                application.set_gui.table.insert('', 'end', values=sub_data)

        # membuat fungsi untuk mengosongkan table
        def kosong_table(self):
            data = application.set_gui.table.get_children()
            for item in data:
                application.set_gui.table.delete(item)

        # membuat fungsi untuk menangani keypress di kolom text search
        def key_search(self, event):
            if event.keycode == 36:
                self.cari_data()

        # membuat fungsi untuk menangani leypress di kolom halaman
        def key_got_to(self, event):
            if event.keycode == 36:
                self.go_to_halaman()


root = Tk()
application(root)
root.mainloop()