from core.bst import BinarySearchTree

from pages.home import home
from pages.manage import ManagePages
from pages.transactions import TransactionPages

def main():
    state = 0
    database = BinarySearchTree()
    manage = ManagePages(database)
    transaction = TransactionPages(database)

    while state != -1:
        if state == 0:
            state = home()
        elif state == 1:
            state = manage.main()
        elif state == 2:
            state = transaction.main()
        else: 
            break

    print("Terima kasih")

main()