from flask import Blueprint, request, jsonify
from src.models.order_model import db, Order

order_blueprint = Blueprint('orders', __name__, url_prefix='/orders')

# 1. Get all orders
@order_blueprint.route('/get_orders', methods=['GET'])
def get_orders():
    try:
        orders = Order.query.all()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# 2. Get a single order by ID
@order_blueprint.route('/get/<int:order_id>', methods=['GET'])
def get_order(order_id):
    try:
        order = Order.query.get(order_id)
        if order:
            return jsonify(order.to_dict()), 200
        else:
            return jsonify({'message': 'Order not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# 3. Add a new order
@order_blueprint.route('/', methods=['POST'])
def add_order():
    try:
        data = request.json
        new_order = Order(
            product_name=data.get('product_name'),
            quantity=data.get('quantity'),
            total_price=data.get('total_price')
        )
        db.session.add(new_order)
        db.session.commit()
        return jsonify({'message': 'Order created successfully', 'order': new_order.to_dict()}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# 4. Update an existing order
@order_blueprint.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    try:
        data = request.json
        order = Order.query.get(order_id)
        if order:
            order.product_name = data.get('product_name', order.product_name)
            order.quantity = data.get('quantity', order.quantity)
            order.total_price = data.get('total_price', order.total_price)
            db.session.commit()
            return jsonify({'message': 'Order updated successfully', 'order': order.to_dict()}), 200
        else:
            return jsonify({'message': 'Order not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# 5. Delete an order by ID
@order_blueprint.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    try:
        order = Order.query.get(order_id)
        if order:
            db.session.delete(order)
            db.session.commit()
            return jsonify({'message': 'Order deleted successfully'}), 200
        else:
            return jsonify({'message': 'Order not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500
