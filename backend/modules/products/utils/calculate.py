from decimal import Decimal, InvalidOperation


def calculate_markup(data):
    try:
        cost_price = Decimal(data.get('cost_price', 0))
        retail_price = Decimal(data.get('retail_price', 0))

        if cost_price > 0 and retail_price > 0:
            markup = ((retail_price - cost_price) / cost_price) * 100
            return round(markup, 2)
    except (InvalidOperation, ValueError, TypeError):
        pass
    
    return None


def calculate_average_cost(data, business):
    product_quantity = data.get('quantity', 0)
    product_cost = data.get('cost_price', 0)
    product_id = data.get('product', '')

    product_total_cost = product_cost * product_quantity

    products = business.products
    product = products.filter(id=product_id).first()
    if not product:
        return None

    cost_history = product.cost_history.all()

    total_cost = product_total_cost
    total_quantity = product_quantity


    for history in cost_history:
        total_cost += history.cost_price * history.quantity
        total_quantity += history.quantity

    if total_quantity == 0:
        return None
    
    return round(total_cost / total_quantity, 2)
