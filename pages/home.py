from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from helper.header import header

def home():
    header(main=True)
    print("Selamat datang di Sistem Informasi Stok dan Transaksi 👋\n")

    choice = inquirer.select(
        message="Berikut menu yang dapat anda pilih:",
        choices=[
            Choice(value=1, name="Kelola Barang"),
            Choice(value=2, name="Kelola Transaksi Konsumen"),
            Choice(value=0, name="Keluar")
        ],
    ).execute()

    if choice == 0:
        return -1

    return choice
