#Create an application which manages an inventory of products. 
#Create a product class which has a price, id, and quantity on hand. 
#Then create an inventory class which keeps track of various products 
#and can sum up the inventory value.


class Product:
	'''Each product has a price, its id and its quantity'''
	'''Implement a time module to randomly decide which products will be discounted today'''
	def __init__(self, id_, price, quantity):
		self.id_ = id_
		self.price = price
		self.quantity = quantity

	def __str__(self):
		return f"Product: {self.id_}, price per unit: {self.price}, quantity: {self.quantity}"

	@classmethod
	def new_product(cls, nom):
		while True:
			try:
				prix = float(input('State the price of your product: '))
				quantite = int(input('Input the quantity of your product: '))
				if (prix or quantite) <= 0:
					print('The amount of product or its price cannot be lower than/equal to 0')
					continue
			except ValueError:
				print('Please input an integer for the quantity and price of the product')
			else:
				break
		return cls(
			nom,
			prix,
			quantite
			)


class Inventory:
	'''Shows the total amount of goods in stock, as well as the total value'''
	def __init__(self):
		self.stock = 0
		self.value = 0
		self.nomenclature = []
		self.namebook = [] #if a product's quantity at 0, deletes it from the namebook and nomenclature

	def __str__(self):
		return f"Current products in the inventory: {self.namebook}, overall {self.stock} pieces in stock, with a shared value of {self.value}"

	def create_many(self):
		'''an initialization function that creates many products in the inventory'''
		'''in case of duplicate prioritizes products already in the inventory'''
		'''maybe implement the choice system where you get to decide which product stays
		   in case of a conflict'''
		while True:
			name = None
			while not name and name != 'stop':
				name = input("Name your product (to quit enter 'stop'): ")
			if name.lower() == 'stop':
				break
			else:
				someproduct = Product.new_product(name)
				if someproduct.id_ in self.namebook:
					replace = input(f"=!!WARNING!!=\nThere is already a product with the name {someproduct.id_} in the inventory. Would you like to rename the new object? ({someproduct}) Enter 'yes' or 'no': ") #add an option to rename the conflicting product
					if replace == 'yes':
						print(f'Old name: {someproduct.id_}')
						someproduct.id_ = input('Rename your product: ')
						while not someproduct.id_:
							someproduct.id_ = input('Name cannot be empty. Rename your product: ')
					else:
						print("This object will not be added to the inventory")
						continue
				self.nomenclature.append(someproduct)
				self.namebook.append(someproduct.id_)
				self.value += someproduct.price*someproduct.quantity
				self.stock += someproduct.quantity
				self.__str__()


class Customer(Inventory):
	def __init__(self):
		super().__init__()
		self.money = 100 #add options for cash and a card money
		self.basket_lst = [] #add to the general str implementation
		while True:
			try:
				while self.money<0:
					self.money = float(input('How much money do you have? '))
			except ValueError:
				print('Please enter an integer')
			else:
				break

	def shop_cycle(self, till):
		'''If there are no products to add, skip the method'''
		while True:
			want = input("Do you want to add a product or proceed to the cash desk? Enter 'add' or 'pay': ")
			if want.lower() == 'pay':
				till.choice()
			elif want.lower() == 'add':
				self._prod_choice()
			else:
				want = input("Please enter 'add' or 'pay': ")

	def remove_from_stock(self, someproduct, inventory):
		'''removes a product if its amount in the inventory reaches 0'''
		inventory.nomenclature.remove(someproduct)
		inventory.namebook.remove(someproduct.id_)
		#print(f'The product "{someproduct.id_}" has been removed from the inventory')

	def prod_choice(self, inventory, till):
		while True:
			print(f'Currently available products in store: {inventory.namebook}')
			name = input("Enter the name of a product you'd like to add or 'pay' to proceed to the cash desk: ")
			'''Later: maybe add an order on demand clause when the product desired is not in stock'''
			if name in inventory.namebook:
				prod = inventory.nomenclature[inventory.namebook.index(name)]
				count = None
				while type(count) != int:
					try:
						count = int(input(f'How many units of {name} would you like to add to the inventory? Currently available: {prod.quantity}. Enter an integer: '))
						if count > prod.quantity:
							choice = input(f"There is not enough product in stock. Would you like to add the maximum quantity ({prod.quantity} units)? Enter 'yes' or 'no': ")
							if choice.lower() == 'yes':
								self._add_to_cart(prod, count)
							else:
								print("This product won't be added to your cart.")
								continue
					except ValueError:
						print('Please enter an integer')
					else:
						if count == 0:
							count = None
							continue
						self._add_to_cart(prod, count)
				if prod.quantity == 0:
					self.remove_from_stock(prod, inventory)
			elif name.lower() == 'pay':
				till.choice(self)
				break
			else:
				print("Make sure you're entering the product name correctly or write 'pay'.")

	def _add_to_cart(self, prod, count):
		'''Print the amount of products currently in basket every time something new is added'''
		self.nomenclature.append(prod)
		self.namebook.append(prod.id_)
		prod.quantity -= count
		self.value += prod.price*count
		self.stock += count
		self.basket_lst.append([prod.id_, count, prod.price*count, prod.price])
		print(f'{count} unit(s) of the product "{prod.id_}" has been added to the basket')
		print("Currently in basket:")
		for lst in self.basket_lst:
			print(f"{lst[0]}: {lst[1]} unit(s), {lst[2]} total cost;")
		print(f"\nOverall cost: {self.value}")


class Till:
	'''Has physical money and can take cards (maybe implement later), has a section for returned products, calculates discounts'''
	def __init__(self):
		#self.change = 1000 #maybe save the state and update to 1000 only every day?, probably useless
		#self.returns = [] #maybe stores returned products, cannot be accesed while here, get transfered to invent later
		self.discounts = [] #possibly put in special high-discount prods here? OR use to check which ones from the backet are on discount

	def choice(self, customer):
		'''Later maybe add cash or credit card functionality? Then which coins will customer have exactly?'''
		print(f"Hello and welcome to our store! Your have in your basket products with an altogether cost of {customer.value}.")
		while customer.money < customer.value:
			print(f"Looks like you don't have enough money on you! You only have {customer.money}, and your basket contains products for the sum of {customer.value}.")
			print("Your basket:")
			for product, units, cost, price in customer.basket_lst:
				print(f"{product}: {units} units, {cost} total cost")
			print(f"\nOverall cost: {customer.value}")
			remove = (input("Choose products you'd like to remove in the format 'product, units': "))
			r_name, r_units = tuple(remove.split(', '))
			prod = customer.nomenclature[customer.namebook.index(r_name)]
			customer.value -= prod.price*int(r_units)
			customer.stock -= int(r_units)
			customer.basket_lst[customer.namebook.index(r_name)][1] -= int(r_units)
			customer.basket_lst[customer.namebook.index(r_name)][2] -= prod.price*int(r_units)
		else:
			'''later add a discounts functonality'''
			'''needs to leave customer empty if in the future program will save its state between sessions'''
			'''customer.money -= customer.value
			customer.nomenclature = []
			customer.namebook = []
			customer.stock = 0
			customer.value = 0'''
			print("Your receipt:")
			for product, units, cost, price in customer.basket_lst:
				print(f"{product}: {price} * {units} = {cost}")
			print(f"\nResult: {customer.value}")
			print("** **    ** **    ** **\nThanks for your purchase. Come back soon!")