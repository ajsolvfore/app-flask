from src import db

# Define the Product model
class Product(db.Model):
    __tablename__ = 'products'

    # Define the columns for the Product table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    # Define a method to serialize the product data as a dictionary
    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price
        }
