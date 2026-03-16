# ========The beginning of the class==========

import os  # importing os outside of the function to improve efficiency

class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        
        '''
        A class to represent a Shoe.

        Attributes
        ----------
        country : str
            The country name where the shoe is in stock.
        code : str
            The product code.
        product : str
            The specific product name.
        cost : float
        The cost of the specified shoe.
        quantity : int
            The number of shoe units in stock
            
        '''
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity
        
        
    def get_cost(self):
        """
        The method to get the cost attribute from a shoe object.

        Returns:
            cost (float): The cost attribute of an object
        """
        return self.cost
       
        

    def get_quantity(self):
        """
        The method to get the quantity of a shoe item in stock

        Returns:
            quantity (int): The number of shoe item units in stock
        """
        return self.quantity

    def __str__(self):
        '''
        A method to return a string representation of a class.
        '''
        format =(
        f"Country: {self.country}\n"
        f"Code: {self.code}\n"
        f"Product: {self.product}\n"
        f"Cost: {self.cost}\n"
        f"Quantity: {self.quantity}"
        )
        return format
        

# =============Shoe list===========
'''
The list will be used to store a list of objects of shoes.
'''

shoe_list = []


# ==========Functions outside the class==============

def read_shoes_data():
    '''
    This function will open the file inventory.txt
    and read the data from this file, then create a shoes object with this data
    and append this object into the shoes list. One line in this file represents
    data to create one object of shoes. You must use the try-except in this function
    for error handling. Remember to skip the first line using your code.
    '''
    try:
        with open("inventory.txt", 'r') as file:
            
            # iterating through the lines of the file and split them into relevant features
            temp_list = []
            for line in file:
                if line.strip():
                    temp_list.append(line.strip().split(","))
                else:
                    continue
                
            # error handling for when data type casting outputs an error
            try:
                
                # extracting attributes to make the object (excluding headers)
                for items in temp_list[1:]:
                    
                    # Extracting the country, code, product,cost, and quantity features
                    # of a specific shoe item.
                    country, code, product, cost, quantity = items
                    
                    
                    shoe_list.append(Shoe(country, code, product, float(cost), int(quantity)))
                    
                return shoe_list
            
            except ValueError:
                
                return print("The item does not have a relevant cost or quantity")
    # error handling for when the txt file is not found
    except FileNotFoundError:
        
        return print("The file name is not found")

def capture_shoes():
    '''
    This function will allow a user to capture data
    about a shoe and use this data to create a shoe object
    and append this object inside the shoe list.
    '''
    #
    while True:
        
        # Prompting the user to specify country, code and product
        while True:
            try:
                country =  input("Specify the country where the shoe item is in stock: ").strip()
                code = input("Please specify the product code (e.g. SKU38773): ").strip()
                product = input("Please specify the product name: ").strip()
                break
            except Exception as e:
                print("Please do not leave any field empty")
    
        #
        while True:
            try:
                cost = float(input("Please specify the cost of the product in Rands: ").strip())
                quantity = int(input("Please specify the number of product items in stock: ").strip())
                break
            except ValueError:
                print("The cost and quantity must be numerical values and all the fields must not be empty")
                continue
        
        #The condition checks if each field is empty
        if not country or not code or not product:
            print("The cost, code and product fields must not be empty")
            continue
        else:
            item =  Shoe(country, code, product, cost, quantity)
            

            shoe_list.append(item)

        
        # Save to inventory.txt
        file_exists = os.path.isfile("inventory.txt")
        with open("inventory.txt", "a") as f:
            if not file_exists:
                # Write header if file is new
                f.write("Country,Code,Product,Cost,Quantity\n")
            
            # Write the captured item
            f.write(f"{item.country},{item.code},{item.product},{item.cost},{item.quantity}\n")
            
                        #
            print(f"""\nYou have captured a product with the following stock details:
                  \nCountry: {item.country}
                  \nCode: {item.code}
                  \nproduct: {item.product}
                  \ncost: R{item.cost}
                  \nquantity: {item.quantity} items in stock
                  """)
            
        # Prompt the user to check if they want to capture another stock items
        while True:
            
            prompt = input("Do you want to enter more shoe items to the database? (y/n): ").strip().lower()
            
            # condition to monitor 'prompt' for adding shoe to a database
            if prompt == 'y':
                break
            
            elif prompt == 'n':
                
                return
            
            # default when a y or n is not specified
            else:
                print("Please specify either a yes or no")
                
        return None


    
def view_all():
    '''
    This function will iterate over the shoes list and
    print the details of the shoes returned from the __str__
    function. Optional: you can organise your data in a table format
    by using Python’s tabulate module.
    '''
    print("The shoe items in stock are:\n")
    
    for item in shoe_list:
        print(item)
        print("-" * 30)
    
    return None

    

def re_stock(shoe_list):
    '''
    This function finds the shoe object with the lowest quantity.
    It asks the user if the shoe has been restocked and updates the
    quantity both in memory and in the inventory file.
    '''

    if not shoe_list:
        print("Inventory is empty.")
        return

    # Find shoe with lowest quantity
    lowest_shoe = min(shoe_list, key=lambda shoe: shoe.get_quantity())

    print(f"\nThe following shoe needs restocking:\n{lowest_shoe}")

    restock = input("Did the shoe item get restocked? (y/n): ").strip().lower()

    # condition to monitor the restock prompt field
    if restock == 'y':

        try:
            new_quantity = int(input("Enter the quantity added: ").strip())
        except ValueError:
            print("Invalid quantity.")
            return

        # Use search_shoe to locate the shoe
        result = search_shoe(shoe_list, lowest_shoe.code)

        if result:
            shoe, index = result

            # Update quantity
            shoe.quantity += new_quantity

            print(f"\nUpdated quantity: {shoe.quantity}")

            # Update file
            with open("inventory.txt", "r") as f:
                lines = f.readlines()

            with open("inventory.txt", "w") as f:
                for line in lines:

                    parts = line.strip().split(",")

                    # Matching the product code that needs an update and checking if the format is correct
                    if len(parts) >= 5 and parts[1] == shoe.code:
                        parts[4] = str(shoe.quantity)
                        line = ",".join(parts) + "\n"

                    f.write(line)

            print("\nInventory file updated successfully.")

    elif restock == 'n':
        print("\nNo restock performed.")



def search_shoe(shoe_list,shoe_code):
    '''
     This function will search for a shoe from the list
     using the shoe code and return this object so that it will be printed.
        '''
    # Iterate over the list to search for shoe object
    for index in range(len(shoe_list)): # source: Hyperiondev sorting and searching notes
        if shoe_list[index].code == shoe_code:
            return shoe_list[index], index
    # If the target item is not found, return None.
    return None
    

def value_per_item():
    
    '''
    This function will calculate the total value for each item.
    Please keep the formula for value in mind: value = cost * quantity.
    Print this information on the console for all the shoes.
    '''
    print("\nList of product values:\n")

    # Iterating through a shoe list to get cost and quantity for calculating value of each shoe item
    for shoe in shoe_list:
        value = round(shoe.get_cost() * shoe.quantity, 3)
        print(f"\nProduct: {shoe.product}  Value: R{value}")

def highest_qty(shoe_list):
    '''
    The function determine the product with the highest quantity and
    print this shoe as being for sale.
    '''
    # Find the shoe object with the maximum quantity
    highest_shoe = max(shoe_list, key=lambda shoe: shoe.quantity) # source: stack overflow
    
    print(f"\n{highest_shoe.product} with {highest_shoe.quantity} units is FOR SALE!.")



#==========Main Menu=============
'''
Create a menu that executes each function above.
This menu should be inside the while loop. Be creative!
'''
def menu():
    """ 
    The menu function to control the progression of the program with multiple menu selections.
    """
    while True:
        
        print("\n===== Welcome to the INVENTORY MANAGEMENT SYSTEM =====")

        print(f""""\n Please select a task option you would like to perform: 
            \n1. Capture new shoe
            \n2. View all shoes
            \n3. Re-stock item with lowest quantity
            \n4. Search for a shoe item
            \n5. View the value of all items
            \n6. View Shoe item with highest quantity
            \n0. Exit""")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            capture_shoes()

        elif choice == "2":
            view_all()

        elif choice == "3":
            re_stock(shoe_list)

        elif choice == "4":
            code = input("\nEnter shoe code: ").strip()
            result = search_shoe(shoe_list, code)

            if result:
                shoe, index = result
                print(shoe)
            else:
                print("Shoe not found.")

        elif choice == "5":
            value_per_item()

        elif choice == "6":
            highest_qty(shoe_list)

        elif choice == "0":
            print("\nExiting Inventory System.")
            break

        else:
            print("\nInvalid option. Please select a valid menu number.")
    
# main function that calls read shoe data by default    
def main():
    read_shoes_data()
    menu()


if __name__ == '__main__':
    main()
