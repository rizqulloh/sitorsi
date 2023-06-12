from InquirerPy import inquirer, validator
from InquirerPy.base.control import Choice
from repositories.manage import Manage
from helper.header import header
from tabulate import tabulate
from validations.manage import ManageValidator

class ManagePages:
    def __init__(self, database):
        self.repositories = Manage(database)
        self.validator = ManageValidator(self.repositories)

    def main(self):    
        while True:    
            header(path="> Kelola Stok Barang")

            choice = inquirer.select(
                message="Berikut menu yang bisa anda pilih:",
                choices=[
                    Choice(value=1, name="Input data barang"),
                    Choice(value=2, name="Restok barang"),
                    Choice(value=3, name="Tampilkan semua data barang"),
                    Choice(value=0, name="Kembali ke menu utama"),
                ]
            ).execute()

            if choice == 0:
                return 0
            
            if choice == 1: self.insert()
            elif choice == 2: self.update_stock()
            elif choice == 3: self.show_all()


            input("Press any key to continue...")
            header()

    def insert(self):
        header(path="> Kelola Stok Barang > Tambahkan stok data barang")
        sku = inquirer.text(
            message="No. SKU:",
            validate=self.validator.sku_validate
        ).execute()

        name = inquirer.text(
            message="Nama Barang:",
            validate=validator.EmptyInputValidator(
                message="Nama barang tidak boleh kosong"
            )
        ).execute()

        price = inquirer.number(
            message="Harga: Rp.",
            min_allowed=0,
            validate=validator.EmptyInputValidator(
                message="Harga tidak boleh kosong"
            )
        ).execute()

        stock = inquirer.number(
            message="Jumlah Stok:",
            min_allowed=0
        ).execute()

        insert = self.repositories.insert({ 
            "sku": sku,
            "name": name,
            "price": int(price),
            "stock": int(stock)
        })

        if not insert:
            print("❌ Barang gagal ditambahkan.")
            input("Press any key to continue...")
            return

        print("✅ Barang berhasil ditambahkan.")

    def update_stock(self):
        header(path="> Kelola Stok Barang > Restok barang")
        print("Restok barang\n")
        sku = inquirer.text(
            message="No. SKU:",
            validate=self.validator.sku_exist_validate
        ).execute()

        print("\nBerikut barang yang akan diperbarui stoknya: ")
        data = [self.repositories.get(sku).data]
        mapped = self.mapping(data)
        alignments = ["center", "left", "left", "center"]
        print(tabulate(
            mapped["data"],
            mapped["headers"],
            colalign=alignments,
            tablefmt="rounded_grid"
        ))

        stock = inquirer.number(
            message="Tambah stok:",
            min_allowed=0
        ).execute()

        updated = self.repositories.update_stock(sku, int(stock))
        if not updated:
            print("❌ Stok barang gagal diperbarui")
            return
        
        print("✅ Stok berhasil diperbarui")


    def show_all(self):
        header(path="> Kelola Stok Barang > Tampilkan data barang")
        data = self.repositories.show_list()

        if len(data) == 0:
            print("🤷 Tidak ada data transaksi")
            return

        mapped = self.mapping(data)
        alignments = ["center", "left", "left", "center"]
        print(tabulate(
            mapped["data"], 
            mapped["headers"], 
            colalign=alignments,
            tablefmt="rounded_grid"
        ))

    def mapping(self, data):
        header_mapping = {
            "No. SKU" : "sku",
            "Nama Barang": "name",
            "Harga (Rp)": "price",
            "Stok": "stock"
        }
        
        mapped = [[item[key] for key in header_mapping.values()] for item in data]
        headers = list(header_mapping.keys())

        return {
            "data": mapped,
            "headers": headers
        }