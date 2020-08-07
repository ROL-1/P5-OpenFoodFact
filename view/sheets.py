"""Structure for products sheets."""

class Sheets:
    """Give structure for products sheets."""
      
    def sheet(product, stores):
        """Sheet."""        
        print('Nom :', product[1])
        print('Description :', product[2])
        print('Marque :', product[3])
        print('Nutriscore :', product[4])
        # Remove unwanted characters in 'stores'.
        stores = str(stores)  #TC
        remove_char = ['[','(','\'',']']
        stores = stores.replace(',)', "")
        for char in remove_char:
            stores = stores.replace(char, "")        
        print('Magasins :', stores)
        print('Lien OpenFoodFact :',product[5])
    
    def list_sheet(count, product):
        """Product list sheet."""
        # First row.
        if count == 0:
            print("Nb",'|',"{:>12}".format('Nutriscores'),'|',"{:50}".format('Marques'),'|','Produits')
            print('-'*120)
        # Rows.
        print("{:>2}".format(count+1),'|',"{:>12}".format(product[4]),'|',"{:50}".format(product[3]),'|',product[1])

    def saves_sheet(count, save):
        """Searches saved list sheet."""
        # First row.
        if count == 0:
            print("Nb",'|',"{:>60}".format('Produits'),'|',"{:60}".format('Substituts'),'|','Date')
            print('-'*150)
        # Rows.
        print("{:>2}".format(count+1),'|',"{:>60}".format(save[0]),'|',"{:60}".format(save[1]),'|',save[2])




