coffee_types = ["latte", "cappuccino", "americano", "expresso"]
cake_types = ["sansebastiancheesecake", "mosaiccake", "carrotcake"]


def report1():
    order_file = open("orders.txt", "r")
    orders = order_file.read().splitlines()
    if len(orders) == 0:
        return "report1;"

    coffee_count = {}

    # create dictionary for counting coffee orders initialized with zeros
    for coffee in coffee_types:
        coffee_count[coffee] = 0
    for line in orders:
        temp = line.split(";")[3:]
        for product in temp:
            product_quantity = (product.split("-"))
            if product_quantity[0] in coffee_count.keys():
                coffee_count[product_quantity[0]] += int(product_quantity[1])

    max_order = max(coffee_count.values())
    most_sold_coffees = []
    answer = ""

    # store most sold coffee names in a list
    for item in coffee_count.items():
        if item[1] == max_order:
            most_sold_coffees.append(item[0])

    # construct answer structure
    for c in most_sold_coffees:
        answer += c + ";"
    answer = answer[:-1]

    return "report1;" + answer


def report2():
    # create a dictionary for keeping track of baristas and their orders' count
    barista_dict = {}
    with open("orders.txt", 'r') as file:
        for line in file:
            line = line.split(";")
            if line[0] != "":
                if line[2] in barista_dict.keys():
                    barista_dict[line[2]] += 1
                else:
                    barista_dict[line[2]] = 1

    # if there is no order, return report name only
    if len(barista_dict) == 0:
        return "report2;"
    else:
        # find the barista with the most orders
        max_order = max(barista_dict.values())

        # find the barista names with the most orders
        answer = ""
        for key, value in barista_dict.items():
            if value == max_order:
                answer += key + ";"

        return "report2;" + answer[:-1]


def report3():
    # create a dictionary for keeping track of ordered products and their quantities
    product_dict = {}
    with open("orders.txt", 'r') as file:
        for line in file:
            line = line.strip().split(";")
            if line[0] != "" and line[1] != '0':
                for product_quantity in line[3:]:
                    product = product_quantity.split("-")[0]
                    quantity = product_quantity.split("-")[1]
                    if product in product_dict.keys():
                        product_dict[product] += int(quantity)
                    else:
                        product_dict[product] = int(quantity)

    # if there is no order, return report name only
    if len(product_dict) == 0:
        return "report3;"
    else:
        # find the product with the most orders
        max_order = max(product_dict.values())

        # find the product names with the most orders
        answer = ""
        for key, value in product_dict.items():
            if value == max_order:
                answer += key + ";"

        return "report3;" + answer[:-1]


def report4():
    order_file = open("orders.txt", "r")
    orders = order_file.read().splitlines()
    if len(orders) == 0:
        return "report4;"
    cake_count = {}
    ex_count = 0
    # create dictionary for counting cake orders with expresso initialized with zeros
    for cake in cake_types:
        cake_count[cake] = 0
    for line in orders:
        temp = line.split(";")[3:]
        if "expresso" in line:
            ex_count += 1
            for product in temp:
                product_quantity = (product.split("-"))
                if product_quantity[0] in cake_count.keys():
                    cake_count[product_quantity[0]] += int(product_quantity[1])

    max_order = max(cake_count.values())
    most_sold_cakes = []
    answer = ""

    # store most sold coffee names in a list
    for item in cake_count.items():
        if item[1] == max_order:
            most_sold_cakes.append(item[0])

    # construct answer structure
    for c in most_sold_cakes:
        answer += c + ";"
    answer = answer[:-1]

    if ex_count == 0:
        return "report4;noexpressoorder"
    return "report4;" + answer
