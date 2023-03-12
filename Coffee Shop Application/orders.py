""" This module contains functions to create and save orders. """


# load prices of products from prices.txt
def load_prices():
    price_file = open("prices.txt", "r")
    prices = price_file.read().splitlines()
    price_dict = {}

    # read prices file and assign each product name and price to a dictionary
    for line in prices:
        temp = line.split(";")
        price_dict[temp[0]] = int(temp[1])
    price_file.close()
    return price_dict


# load discount codes and their discount rates from discountcodes.txt
def load_discounts():
    discount_file = open("discountcodes.txt", "r")
    discount = discount_file.read().splitlines()
    discount_dict = {}

    # read discounts file and assign each code and its discount rate to a dictionary
    for line in discount:
        temp = line.split(";")
        discount_dict[temp[0]] = float(temp[1]) / 100
    discount_file.close()
    return discount_dict


# remove discount code from discountcodes.txt after it is used
def remove_discount(discount_code):
    discount_file_r = open("discountcodes.txt", "r")
    discounts = discount_file_r.readlines()
    discount_file_r.close()
    discount_file_w = open("discountcodes.txt", "w")
    for line in discounts:
        if discount_code not in line:
            discount_file_w.write(line)
    discount_file_w.close()


# calculate total price and discount amount
def calculate_total_price(discount_code, product_quantity):
    total_price = 0
    discount_rate = 1
    discount_amount = 0

    # get prices of products from dictionary and multiply with quantity
    prices = load_prices()
    for tuple in product_quantity:
        total_price += (int(prices[tuple[0]]) * int(tuple[1]))

    if discount_code != "nodiscountcode":
        discounts = load_discounts()

        # if discount code exists return discount rate else return 1 which means no discount
        if discount_code in discounts.keys():
            discount_rate = discounts[discount_code]
            remove_discount(discount_code)
        else:
            discount_rate = 1
        prices = load_prices()

    # if discount rate is not 1, calculate discount amount and total price
    if discount_rate != 1:
        discount_amount = discount_rate * 100
        total_price *= (1 - discount_rate)
    return total_price, discount_amount


# create order info string
def create_order(discount_code, barista, product_quantity):
    if discount_code == "":
        discount_code = "nodiscountcode"
    order_info = discount_code + ";" + barista + ";"

    # add each product-quantity pair to the excepted output
    for tuple in product_quantity:
        order_info += tuple[0] + "-" + str(tuple[1]) + ";"
    order_info = order_info[:-1]
    return "order;" + order_info


# save order info to orders.txt
def save_order(order_info):
    order_info = order_info.split(";")
    discount_code = order_info[1]
    barista = order_info[2]
    temp = order_info[3:]

    # split each product-quantity pair and add to a list of tuples
    product_quantity = []
    for s in temp:
        x = s.split("-")
        product_quantity.append((x[0], x[1]))

    total_price, discount_amount = calculate_total_price(
        discount_code, product_quantity)

    # if discount code is invalid, change it to invaliddiscountcode
    if discount_amount == 0:
        discount_code = '0'

    order = str(total_price) + ";" + discount_code + ";" + barista + ";"
    for tuple in product_quantity:
        order += tuple[0] + "-" + str(tuple[1]) + ";"
    order = order[:-1]
    
    with open("orders.txt", "a+") as file:
        file.writelines(order + "\n")
    return "orderconfirmation;" + str(total_price)
