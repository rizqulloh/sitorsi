from InquirerPy import validator
from repositories.manage import Manage

class ManageValidator:
    def __init__(self, repositories: Manage):
        self.repositories = repositories

    def sku_validate(self, result):
        if len(result) != 4:
            raise validator.ValidationError(
                message="No. SKU harus terdiri dari 4 digit"
            )
        
        if self.repositories.isExists(result):
            raise validator.ValidationError(
                message="No. SKU sudah terdaftar."
            )
        
        return True
    
    def sku_exist_validate(self, result):
        if not self.repositories.isExists(result):
            raise validator.ValidationError(
                message=f"Produk dengan SKU {result} belum terdaftar. Silahkan tambahkan terlebih dahulu"
            )
        
        return True
    