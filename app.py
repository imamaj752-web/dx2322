from flask import Flask
from models import init_db
from product.routes import product_bp
from auth.routes import auth_bp

app = Flask(__name__)
app.secret_key = '123'
init_db()

app.register_blueprint(product_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)