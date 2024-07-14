
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from app.routes.event_routes import event_bp
from app.routes.user_routes import user_bp
from app.routes.participant_routes import participant_bp
from app.routes.auth_routes import auth_bp
from app.routes.analytics_routes import analytics_bp
from config import Config
from flask_request_validator.exceptions import InvalidRequestError
import traceback

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)

app.register_blueprint(event_bp, url_prefix='/events')
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(participant_bp, url_prefix='/participants')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(analytics_bp, url_prefix='/analytics')

@app.errorhandler(InvalidRequestError)
def handle_invalid_request(error):
    response = jsonify({'error': 'Bad Request', 'message': str(error)})
    response.status_code = 400
    return response

# Global error handler for other exceptions
@app.errorhandler(Exception)
def handle_unexpected_error(error):
    # Log the exception traceback for debugging
    traceback.print_exc()
    
    response = jsonify({'error': 'Internal Server Error', 'message': str(error)})
    response.status_code = 500
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5001)