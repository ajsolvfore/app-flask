from flask import Blueprint, request, jsonify
from src import db
from src.models.products_model import Product  # Import the Product model from products_model.py

product_blueprint = Blueprint('products', __name__, url_prefix='/products')

# 1. Route to get all products
@product_blueprint.route('/get_products', methods=['GET'])
def get_products():
    try:
        products = Product.query.all()
        return jsonify([product.as_dict() for product in products])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 2. Route to add a new product
@product_blueprint.route('/add_product', methods=['POST'])
def add_product():
    try:
        new_product = request.json
        product = Product(
            id=new_product['id'],
            name=new_product['name'],
            price=new_product['price']
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': 'Product added successfully', 'product': new_product}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 3. Route to delete a product by ID
@product_blueprint.route('/delete_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        product = Product.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return jsonify({'message': 'Product deleted successfully'})
        else:
            return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
