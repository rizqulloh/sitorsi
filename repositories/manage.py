from core.bst import BinarySearchTree

class Manage:
    def __init__(self, database: BinarySearchTree):
        self.database = database

    def show_list(self):
        datas = self.database.fetch()
        return datas
    
    def get(self, sku):
        return self.database.get(sku, "sku")

    def insert(self, data) -> bool:
        print("\n🔁 Menambahkan data")
        created = self.database.insert(data, "sku")

        return created
    
    def update_stock(self, sku, stock: int) -> bool:
        product = self.database.get(identifier="sku", value=sku)
        if product is None:
            print("❌ Gagal memperbarui stok barang.")
            return False

        updated = self.database.update(new_data={
            "sku": product.data["sku"],
            "name": product.data["name"],
            "price": product.data["price"],
            "stock": product.data["stock"] + stock
        }, identifier="sku", value=sku)
        
        return updated
    
    def isExists(self, id):
        return self.database.contains(id, "sku")
