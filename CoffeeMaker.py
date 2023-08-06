from CMInfo import *


total_cash = 0


def main():
    global total_cash
    while True:
        buying = True
        coffee = which_coffee()

        if coffee == "report":
            print(
                f"Water: {resources['water']}mL\nMilk: {resources['milk']}mL\nCoffee: {resources['coffee']}g\nCash: ${round(total_cash, 2)}"
            )

        if coffee == "off":
            break

        if coffee in ("espresso", "latte", "cappuccino"):
            cost = MENU[coffee]["cost"]
            check = check_resources(coffee)
            if check == False:
                buying = False
                enough = enough_resources()
                if enough == False:
                    print(
                        "In fact, there's not enough resources for any coffee.", end=" "
                    )
                    fill = choice("Would you like to refill the resources? y or n ")
                    if fill == "y":
                        refill()
                    elif fill == "n":
                        break

                elif enough == "espresso" and coffee in ("cappuccino", "latte"):
                    dilemma = choice(
                        "There's still enough for an espresso, would you like to try it? y or n or refill "
                    )
                    if dilemma == "y":
                        # change the coffee into an espresso
                        coffee = "espresso"
                        cost = MENU["espresso"]["cost"]
                        buying = True
                    elif dilemma == "n":
                        print("Okay, sorry for the inconvience. Bye!")
                        break
                    else:
                        refill()

                elif enough == ("espresso", "latte") and coffee == "cappuccino":
                    dilemma = choice(
                        "There's still enough for a latte or an espresso, would you like one of them? y or n or refill "
                    )
                    if dilemma == "y":
                        # Until user types in espresso or latte, it will keep on asking which one they would like
                        while True:
                            try:
                                dilemma2 = input("Which one would you like? ").lower()
                                if dilemma2 not in ("espresso", "latte"):
                                    raise ValueError
                            except ValueError:
                                print("type either espresso or latte")
                            else:
                                break
                        # change the coffee and price to which coffee the user wanted to change it to
                        if dilemma2 == "espresso":
                            coffee = "espresso"
                            cost = MENU["espresso"]["cost"]
                            buying = True
                        else:
                            coffee = "latte"
                            cost = MENU["latte"]["cost"]
                            buying = True
                    elif dilemma == "n":
                        print("Okay, sorry for the inconvience. Bye!")
                        break
                    else:
                        refill()
            if buying == True:
                coins = ask_coins(coffee, cost)
            else:
                coins = 0

            if coins >= cost:
                cash = cost
                total_cash += cash
                print(f"Here's ${round(coins - cost, 2)} refunded.")
                print(f"Enjoy your coffee!")
                subtract_resources(coffee)


# Check if there's enough resources to make a coffee
def check_resources(coffee):
    for ingredient in MENU[coffee]["ingredients"]:
        if MENU[coffee]["ingredients"][ingredient] <= resources[ingredient]:
            pass
        else:
            print(f"You don't have enough {ingredient} for the {coffee}.")
            return False
    return True


def subtract_resources(coffee):
    for ingredient in MENU[coffee]["ingredients"]:
        resources[ingredient] -= MENU[coffee]["ingredients"][ingredient]


# Ask for the amount of each coins
def ask_coins(coffee, cost):
    print(f"The {coffee} costs ${cost}0.")
    while True:
        try:
            pennies = int(input("How many pennies? ")) * 0.01
            nickles = int(input("How many nickles? ")) * 0.05
            dimes = int(input("How many dimes? ")) * 0.10
            quarters = int(input("How many quarters? ")) * 0.25
            if pennies + nickles + dimes + quarters < cost:
                raise ZeroDivisionError
        except ZeroDivisionError:
            if again(coffee) == True:
                pass
            else:
                return 0
        except ValueError:
            print("Type the amount of each coin as an integer.")
        else:
            break
    return round(pennies + nickles + dimes + quarters, 2)


# Ask which type of coffee
def which_coffee():
    while True:
        try:
            coffee = input(
                "What coffee would you like? (Espresso/Latte/Cappuccino) "
            ).lower()
            if coffee not in ("espresso", "latte", "cappuccino", "report", "off"):
                raise ValueError
        except ValueError:
            print("Not a coffee flavor")
        else:
            break
    return coffee


def again(coffee):
    while True:
        try:
            again = input(
                f"Not enough money for the {coffee}. Would you like to try again? 'y' or 'n' "
            ).lower()
            if again not in ("y", "n"):
                raise ValueError
            if again == "y":
                return True
            else:
                return False
        except ValueError:
            print("type 'y' or 'n'")


def enough_resources():
    w = resources["water"]
    m = resources["milk"]
    c = resources["coffee"]
    if w < 50 or m < 0 or c < 18:
        return False
    if w >= 250 and m >= 150 and c >= 24:
        return "espresso", "latte", "cappuccino"
    elif w >= 250 and 100 <= m < 150 and c >= 24:
        return "espresso", "cappuccino"
    elif 200 <= w < 250 and m >= 150 and c >= 24:
        return "espresso", "latte"
    else:
        return "espresso"


def choice(prompt=""):
    while True:
        try:
            choice = input(prompt).lower()
            if choice not in ("y", "n", "refill"):
                raise ValueError
        except ValueError:
            print("please type one of the valid options. ")
        else:
            return choice


def refill():
    global total_cash
    print(
        "2mL of water costs 1 cent\n1ml of milk costs 1 cent\n1g of coffee costs 5 cents"
    )

    def number(resource):
        while True:
            try:
                num = int(input(f"How much {resource} are you going to refill? "))
            except ValueError:
                print("type a number.")
            else:
                return num

    refill_water, refill_milk, refill_coffee = (
        number("water"),
        number("milk"),
        number("coffee"),
    )

    if total_cash - 0.01 * refill_water < 0:
        print("Not enough money to refill water. ")
    else:
        resources["water"] += 2 * refill_water
        total_cash -= 0.01 * refill_water

    if total_cash - 0.01 * refill_milk < 0:
        print("Not enough money to refill milk. ")
    else:
        resources["milk"] += refill_milk
        total_cash -= 0.01 * refill_milk

    if total_cash - 0.05 * refill_coffee < 0:
        print("Not enough money to refill coffee. ")
    else:
        resources["coffee"] += refill_coffee
        total_cash -= 0.05 * refill_coffee


if __name__ == "__main__":
    main()
