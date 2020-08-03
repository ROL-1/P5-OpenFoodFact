"""Structure for products sheets."""

class Sheets:
    """Give structure for products sheets."""

      
    def sheet(product, stores):
        """Sheet."""        
        print('Nom :', product[1])
        print('Marque :', product[2])
        print('Nutriscore :', product[3])
        stores = str(stores)
        remove_char = ['[','(','\'',']']
        stores = stores.replace(',)', "")
        for char in remove_char:
            stores = stores.replace(char, "")        
        print('Magasins :', stores)
        print('Lien OpenFoodFact :',product[4])
    
    def list_sheet(count, product):
        """Product list sheet."""
        if count == 0:
            print("Nb",'|',"{:>12}".format('Nutriscores'),'|',"{:50}".format('Marques'),'|','Produits')
            print('----------------------------------------------------------\
----------------------------------------------------------------------------')
        print("{:>2}".format(count+1),'|',"{:>12}".format(product[3]),'|',"{:50}".format(product[2]),'|',product[1])




