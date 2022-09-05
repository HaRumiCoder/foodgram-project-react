def create_shopping_cart(ingredient_list):
    shopping_cart = "Список покупок \n" + "\n".join(
        f" - {name.title()} ({measurement_unit}) -> {total_amount} "
        for name, total_amount, measurement_unit in ingredient_list
    )
    return shopping_cart
