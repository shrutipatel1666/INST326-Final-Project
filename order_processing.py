    """
    if minutes_available < 0:
        raise ValueError("Available time cannot be negative.")

    for quantity in inventory.values():
        if quantity < 0:
            raise ValueError("Inventory quantities cannot be negative.")

    for recipe in recipes.values():
        prep_time = recipe.get("prep_time")
        if prep_time <= 0:
            raise ValueError("Preparation time must be positive.")
        ingredients = recipe.get("ingredients")
        for quantity in ingredients.values():
            if quantity < 0:
                raise ValueError("Ingredient quantities cannot be negative.")

    for order in orders:
        patience = order.get("patience")
        if patience < 0:
            raise ValueError("Customer patience cannot be negative.")
        drink = order.get("drink")
        if drink not in recipes:
            raise KeyError(drink)

    # Each order can either be included in a plan or skipped.
    all_plans = [[]]
    for position in range(len(orders)):
        new_plans = []
        for plan in all_plans:
            new_plans.append(plan + [position])
        all_plans.extend(new_plans)

    best_plan = []
    best_revenue = 0.0
    best_time = 0

    for plan in all_plans:
        remaining = inventory.copy()
        time_used = 0
        revenue = 0.0
        can_serve = True

        for position in plan:
            order = orders[position]
            drink = order.get("drink")
            recipe = recipes[drink]
            ingredients = recipe.get("ingredients")
            prep_time = recipe.get("prep_time")
            patience = order.get("patience")
            time_used += prep_time

            if time_used > patience or time_used > minutes_available:
                can_serve = False
                break

            for ingredient, quantity in ingredients.items():
                available = remaining.get(ingredient, 0)
                if available < quantity:
                    can_serve = False
                    break

            if not can_serve:
                break

            for ingredient, quantity in ingredients.items():
                available = remaining.get(ingredient, 0)
                remaining[ingredient] = available - quantity
            revenue += order.get("price")

        if not can_serve:
            continue

        revenue = round(revenue, 2)
        is_better = False
        if len(plan) > len(best_plan):
            is_better = True
        elif len(plan) == len(best_plan):
            if revenue > best_revenue:
                is_better = True
            elif revenue == best_revenue:
                if plan < best_plan:
                    is_better = True

        if is_better:
            best_plan = plan
            best_revenue = revenue
            best_time = time_used

    # Only subtract ingredients after choosing the best plan.
    served = []
    not_served = []
    for position in range(len(orders)):
        order = orders[position]
        order_id = order.get("order_id")
        if position in best_plan:
            served.append(order_id)
            drink = order.get("drink")
            ingredients = recipes[drink].get("ingredients")
            for ingredient, quantity in ingredients.items():
                if quantity > 0:
                    inventory[ingredient] -= quantity
        else:
            not_served.append(order_id)

    return {
        "served": served,
        "not_served": not_served,
        "revenue": best_revenue,
        "time_used": best_time
    }

