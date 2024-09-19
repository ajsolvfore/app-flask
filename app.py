from src import create_app
from src.models.order_model import db
from src.models.users_model import db
from src.models.products_model import db
app = create_app()

# Create tables if not exist


if __name__ == '__main__':
    app.run(debug=True)
