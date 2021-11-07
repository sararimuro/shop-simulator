import sfuncs

stock = sfuncs.Inventory()
till = sfuncs.Till()
stock.create_many()
client = sfuncs.Customer()
if stock.nomenclature != []:
	client.prod_choice(stock, till)
else:
	print("Looks like we're out of stock at this time, please come back tomorrow!")