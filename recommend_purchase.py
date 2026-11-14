#!/usr/bin/env python
# coding: utf-8

# In[3]:


def recommend_purchases(inventory, recipes, predicted_sales, prices, budget):
    """
    This function helps us decide what ingredients to buy for the next day.
    It checks what we have, what we expect to sell, and our budget.
    The goal is to make as many drinks as possible without overspending.
    """
    if budget < 0:
        raise ValueError("Budget cannot be negative")

    for amount in inventory.values():
        if amount < 0:
            raise ValueError("Inventory cannot be negative")

    for ingredient in prices:
        if prices[ingredient] <= 0:
            raise ValueError("Prices must be positive")

    for drink in predicted_sales:
        if predicted_sales[drink] < 0:
            raise ValueError("Sales cannot be negative")

        for ingredient in recipes[drink]["ingredients"]:
            if recipes[drink]["ingredients"][ingredient] < 0:
                raise ValueError("Ingredient amount cannot be negative")
            if ingredient not in prices:
                raise ValueError("Missing ingredient price")

    drinks = sorted(predicted_sales)
    ingredients = sorted(prices)

    needed = {}

    # Figure out how much we might need for tomorrow
    for ingredient in ingredients:
        needed[ingredient] = 0

        for drink in drinks:
            recipe = recipes[drink]["ingredients"]
            amount = recipe.get(ingredient, 0)
            needed[ingredient] += amount * predicted_sales[drink]

    # Make different purchase options
    purchase_options = [{}]

    for ingredient in ingredients:
        new_options = []
        missing = max(0, needed[ingredient] - inventory.get(ingredient, 0))

        for option in purchase_options:
            for amount in range(missing + 1):
                new_option = option.copy()
                new_option[ingredient] = amount
                new_options.append(new_option)

        purchase_options = new_options

    # Make possible combinations of expected drink sales
    sales_options = [{}]

    for drink in drinks:
        new_options = []

        for option in sales_options:
            for amount in range(predicted_sales[drink] + 1):
                new_option = option.copy()
                new_option[drink] = amount
                new_options.append(new_option)

        sales_options = new_options

    best_purchases = {}
    best_sales = {}
    best_count = -1
    best_cost = float("inf")
    best_quantities = None

    # Compare the purchases without going over budget
    for purchase in purchase_options:
        cost = 0
        available = inventory.copy()

        for ingredient in ingredients:
            amount = purchase[ingredient]
            cost += amount * prices[ingredient]
            available[ingredient] = available.get(ingredient, 0) + amount

        if cost > budget:
            continue

        supported = {}
        count = -1
        best_sales_order = None

        # Check which drinks can actually be made
        for sales in sales_options:
            used = {}
            possible = True

            for drink in drinks:
                recipe = recipes[drink]["ingredients"]

                for ingredient in recipe:
                    if ingredient not in used:
                        used[ingredient] = 0

                    used[ingredient] += recipe[ingredient] * sales[drink]

            for ingredient in used:
                if used[ingredient] > available.get(ingredient, 0):
                    possible = False
                    break

            if possible:
                total = sum(sales.values())
                sales_order = tuple(sales[drink] for drink in drinks)

                if (total > count or
                    (total == count and
                     (best_sales_order is None or sales_order > best_sales_order))):
                    count = total
                    supported = sales.copy()
                    best_sales_order = sales_order

        quantities = tuple(purchase[ingredient] for ingredient in ingredients)

        # Keep the option that supports the most orders
        if (count > best_count or
            (count == best_count and cost < best_cost) or
            (count == best_count and cost == best_cost and
             (best_quantities is None or quantities < best_quantities))):

            best_count = count
            best_cost = cost
            best_quantities = quantities
            best_purchases = purchase.copy()
            best_sales = supported.copy()

    # Only show ingredients we actually need to buy
    final_purchases = {}

    for ingredient in best_purchases:
        if best_purchases[ingredient] > 0:
            final_purchases[ingredient] = best_purchases[ingredient]

    return {
        "purchases": final_purchases,
        "total_cost": round(best_cost, 2),
        "supported_sales": best_sales
    }


# In[4]:


inventory = {
    "milk": 2,
    "coffee": 3,
    "syrup": 1
}

recipes = {
    "Latte": {
        "ingredients": {"milk": 2, "coffee": 1},
        "prep_time": 5
    },
    "Vanilla Latte": {
        "ingredients": {"milk": 2, "coffee": 1, "syrup": 1},
        "prep_time": 6
    }
}

predicted_sales = {
    "Latte": 2,
    "Vanilla Latte": 1
}

prices = {
    "milk": 2,
    "coffee": 1,
    "syrup": 1
}

budget = 8

print(recommend_purchases(inventory, recipes, predicted_sales, prices, budget))


# In[ ]:




