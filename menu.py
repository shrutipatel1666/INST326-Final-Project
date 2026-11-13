def recommend_menu(drinks, recipes, customer_groups, max_drinks):
    """
    Recommend a daily menu based on customer preferences and drink
    preparation times.
    """
    if max_drinks < 0:
        raise ValueError("max_drinks cannot be negative.")
    
    for drink_name in drinks:
        if drinks[drink_name]["price"] < 0:
            raise ValueError("Price cannot be negative.")
    
    for recipe_name in recipes:
        if recipes[recipe_name]["prep_time"] <= 0:
            raise ValueError("Prep time must be positive.")
        ingredients = recipes[recipe_name]["ingredients"]
        for ing in ingredients:
            if ingredients[ing] < 0:
                raise ValueError("Ingredient quantity cannot be negative.")
            
    for group in customer_groups:
        if group["budget"] < 0 or group["size"] < 0:
            raise ValueError("Budget and size cannot be negative.")
    
    drink_names = list(drinks.keys())
    
    if max_drinks == 0 or len(drink_names) == 0:
        unserved = []
        i = 0
        while i < len(customer_groups):
            unserved.append(i)
            i += 1
        return {
            "menu": [],
            "score": 0, 
            "total_prep_time": 0,
            "unserved_groups": unserved
        }
        
    all_menus = [[]] 
    limit = min(max_drinks, len(drink_names))
    
    if limit >= 1: 
        i = 0
        while i < len(drink_names):
            all_menus.append([drink_names[i]])
            i += 1
            
    if limit >= 2:
        i = 0
        while i < len(drink_names):
            j = i + 1
            while j < len(drink_names):
                pair = sorted([drink_names[i], drink_names[j]])
                all_menus.append(pair)
                j += 1
            i += 1
            
    if limit >= 3:
        i = 0
        while i < len(drink_names):
            j = i + 1
            while j < len(drink_names):
                k = j + 1
                while k < len(drink_names):
                    trip = sorted([drink_names[i],
                                  drink_names[j],
                                  drink_names[k]])
                    all_menus.append(trip)
                    k += 1  # Fixed infinite loop bug here
                j += 1
            i += 1
            
    best_menu = []
    best_score = -1
    best_time = 999999
    best_unserved = []
    
    menu_index = 0
    while menu_index < len(all_menus):  # Fixed loop condition here
        menu = all_menus[menu_index]
        menu_score = 0
        unserved = []
        
        g_index = 0
        while g_index < len(customer_groups):
            group = customer_groups[g_index]
            prefs = group["preferences"]
            budget = group["budget"]
            g_size = group["size"]
            
            top_matches = -1
            d_index = 0
            while d_index < len(menu):
                d_name = menu[d_index]
                d_dict = drinks[d_name]
                if d_dict["price"] <= budget:
                    matches = 0
                    for tag in prefs:
                        if tag in d_dict["tags"]:
                            matches += 1  # Fixed match counting bug here
                    if matches > top_matches:
                        top_matches = matches
                d_index += 1
                
            if top_matches > 0:
                menu_score += top_matches * g_size
            else: 
                unserved.append(g_index)
            g_index += 1
            
        total_time = 0
        d_index = 0
        while d_index < len(menu):
            total_time += recipes[menu[d_index]]["prep_time"]
            d_index += 1
            
        is_better = False
        if menu_score > best_score:
            is_better = True
        elif menu_score == best_score:
            if total_time < best_time: 
                is_better = True
            elif total_time == best_time:
                if menu < best_menu:
                    is_better = True
                    
        if is_better:
            best_score = menu_score
            best_menu = menu
            best_time = total_time
            best_unserved = unserved
            
        menu_index += 1
    
    if best_score == -1:
        best_score = 0
        best_time = 0
        
    return {
        "menu": best_menu,
        "score": best_score,
        "total_prep_time": best_time,
        "unserved_groups": best_unserved
    }