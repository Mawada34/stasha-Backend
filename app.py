import os
from flask import Flask
from flask_cors import CORS
from routes.portfolio import portfolio_bp
from routes.testimonials import testimonials_bp
from routes.services import services_bp
from routes.content import content_bp
from routes.auth import auth_bp
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from routes.upload import upload_bp


load_dotenv()
print("DEBUG hash loaded:", os.environ.get("ADMIN_PASSWORD_HASH"))
app = Flask(__name__)
CORS(app)  # allows your frontend JS to call this API from a different origin

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt=JWTManager(app)

app.register_blueprint(portfolio_bp, url_prefix="/api/portfolio")
app.register_blueprint(testimonials_bp, url_prefix="/api/testimonials")
app.register_blueprint(services_bp, url_prefix="/api/services")
app.register_blueprint(content_bp, url_prefix="/api/content")
app.register_blueprint(auth_bp,url_prefix="/api/auth")
app.register_blueprint(upload_bp,url_prefix="/api/upload")


@app.route("/")
def home():
    return {"status": "Stasha Interior backend is running"}

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
