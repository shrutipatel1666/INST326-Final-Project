#!/usr/bin/env python
# coding: utf-8

# In[5]:


def update_inventory(inventory, recipes, order):
"""
Updtaes inventory after an order. 
If there are not enough ingredients, the order is rejected
Returns True if the order goes through and False if it cannot.
"""
    needed = {}
#Should go through the drinks in order
    for drink in order:
        for ingredient in recipes[drink]["ingredients"]:
            amount = recipes[drink]["ingredients"][ingredient]

            if ingredient not in needed:
                needed[ingredient] = 0

            needed[ingredient] += amount
#Checking if we have enough ingredients for the order
    for ingredient in needed:
        if inventory.get(ingredient, 0) < needed[ingredient]:
            return False
#Take the ingredients out of inventory
    for ingredient in needed:
        inventory[ingredient] -= needed[ingredient]

    return True


# In[6]:


inventory = {
    "milk": 10,
    "coffee": 8,
    "syrup": 5
}

recipes = {
    "Latte": {
        "prep_time": 5,
        "ingredients": {
            "milk": 2,
            "coffee": 1
        }
    },
    "Vanilla Latte": {
        "prep_time": 6,
        "ingredients": {
            "milk": 2,
            "coffee": 1,
            "syrup": 1
        }
    }
}

order = ["Latte", "Vanilla Latte"]

print(update_inventory(inventory, recipes, order))
print(inventory)


# In[ ]:




