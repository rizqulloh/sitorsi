from InquirerPy import inquirer, validator
from InquirerPy.base.control import Choice
from repositories.manage import Manage
from helper.header import header
from tabulate import tabulate
from validations.manage import ManageValidator

class TransactionPages:
    def __init__(self, database):
        self.repositories = Manage(database)
        self.validator = ManageValidator(self.repositories)
        self.transactions = []

    def main(self):    
        while True:   
            header(path="> Kelola Transaksi Konsumen") 

            choice = inquirer.select(
                message="Berikut menu yang bisa anda pilih:",
                choices=[
                    Choice(value=1, name="Input data transaksi baru"),
                    Choice(value=2, name="Lihat transaksi konsumen"),
                    Choice(value=3, name="Lihat transaksi berdasarkan subtotal"),
                    Choice(value=0, name="Kembali ke menu utama\n"),
                ]
            ).execute()

            if choice == 0:
                return 0
            
            if choice == 1: self.insert()
            elif choice == 2: self.show_all()
            elif choice == 3: self.show_by_subtotal()


            input("Press any key to continue...")

    def insert(self):
        header(path="> Kelola Transaksi Konsumen > Input Transaksi Baru")
        name = inquirer.text(
            message="Nama konsumen:",
            validate=validator.EmptyInputValidator(
                message="Nama konsumen tidak boleh kosong"
            )
        ).execute()

        product = None
        quantity = 0

        while True:
            sku = inquirer.text(
                message="No. SKU:",
                validate=self.validator.sku_exist_validate
            ).execute()

            product = self.repositories.get(sku)

            qty = inquirer.number(
                message="Jumlah beli:",
                min_allowed=0,
                max_allowed=product.data["stock"]
            ).execute()

            quantity += int(qty)
            subtotal = product.data['price'] * int(qty)

            print(f"Subtotal: {subtotal}")
            
            if product.data["stock"] >= quantity:
                self.repositories.update_stock(product.data["sku"], (-quantity))
                self.transactions.append({
                    "consumer": name,
                    "sku": sku,
                    "qty": qty,
                    "subtotal": subtotal
                })
                print("\n✅ Data transaksi konsumen berhasil diinputkan\n")
            else:
                print("\n❌ Jumlah Stok No.SKU yang Anda beli tidak mencukupi\n")
        
            repeat = inquirer.confirm(
                message="Apakah ingin menambahkan data pembelian untuk konsumen ini?",
                default=True
            ).execute()

            if not repeat:
                return
    
    def show_all(self):
        header(path="> Kelola Transaksi Konsumen > Lihat Seluruh Transaksi")

        if len(self.transactions) == 0:
            print("🤷 Tidak ada data transaksi")
            return

        mapped = self.mapping(self.transactions)
        alignments = ["left", "center", "center", "left"]

        print(tabulate(
            mapped["data"],
            mapped["headers"],
            colalign=alignments,
            tablefmt="rounded_grid"
        ))

    def show_by_subtotal(self):
        header(path="> Kelola Transaksi Konsumen > Lihat Data Transaksi (berdasarkan subtotal)")

        if len(self.transactions) == 0:
            print("🤷 Tidak ada data transaksi")
            return

        subtotal = inquirer.number(
            message="Subtotal: ",
            min_allowed=0
        ).execute()

        data = [data for data in self.transactions if data["subtotal"] == int(subtotal)]
        mapped = self.mapping(data)
        alignments = ["left", "center", "center", "left"]

        if len(data) == 0: 
            print("❌ Tidak ada data transaksi")
            return

        print(tabulate(
            mapped["data"],
            mapped["headers"],
            colalign=alignments,
            tablefmt="rounded_grid"
        ))


    def mapping(self, data):
        header_mapping = {
            "Nama Konsumen" : "consumer",
            "No. SKU": "sku",
            "Jumlah Barang yang Dibeli": "qty",
            "Subtotal (Rp)": "subtotal"
        }
        
        mapped = [[item[key] for key in header_mapping.values()] for item in data]
        headers = list(header_mapping.keys())

        return {
            "data": mapped,
            "headers": headers
        }

        

        

        
        