from flask import Flask, jsonify, request
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy.schema import SQLAlchemyAutoSchemaMeta
import json

### Flask initialization

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://Freddy:1@localhost:5432/Labs'
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Swagger documentation route
@app.route('/swagger')
def get_swagger():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Expences Tracker API"
    return jsonify(swag)

# Swagger UI route
SWAGGER_URL = '/swagger-ui'
API_URL = '/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Expences Tracker API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/swagger.json')
def swagger():
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))

### Database ORM

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column('user_id', db.Integer, primary_key = True)
    name = db.Column('name', db.String(64), primary_key = False, nullable = False)
    currency_id = db.Column('currency_id', db.Integer, primary_key = False, nullable = True)

class CurrencyModel(db.Model):
    __tablename__ = 'currency'
    id = db.Column('currency_id', db.Integer, primary_key = True)
    code = db.Column('code', db.String(10), primary_key = False, nullable = False)
    full_name = db.Column('full_name', db.String(64), primary_key = False, nullable = False)

class RecordModel(db.Model):
    __tablename__ = 'expences'
    id = db.Column('expences_id', db.Integer, primary_key = True)
    currency_id = db.Column('currency_id', db.Integer, primary_key = False, nullable = False)
    user_id = db.Column('user_id', db.Integer, primary_key = False, nullable = False)
    amount = db.Column('value', db.Double, primary_key = False, nullable = False)

### Validation schemas

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_instance = True
    
class CurrencySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CurrencyModel
        load_instance = True
    
class RecordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RecordModel
        load_instance = True
    
### Users endpoints
    
@app.route('/users', methods=['GET'])
def get_all_users():
    user_list = UserModel.query.all()
    return jsonify(UserSchema().dump(user_list, many = True))

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    int_id = int(user_id)
    user = UserModel.query.get(int_id)
    if user:
        return jsonify(UserSchema().dump(user))
    return jsonify({'error': 'User not found'}), 404

@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    int_id = int(user_id)
    user = UserModel.query.get(int_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'})
    return jsonify({'error': 'User not found'}), 404

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    user = UserSchema().load(data)
    if user:
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'})
    return jsonify({'error': 'Bad User data'}), 400

### Currencies endpoints

@app.route('/currencies', methods=['GET'])
def get_all_currencies():
    cur_list = CurrencyModel.query.all()
    return jsonify(CurrencySchema().dump(cur_list, many = True))

@app.route('/currency/<currency_id>', methods=['GET'])
def get_currency(currency_id):
    int_id = int(currency_id)
    cur = CurrencyModel.query.get(int_id)
    if cur:
        return jsonify(CurrencySchema().dump(cur))
    return jsonify({'error': 'Currency not found'}), 404

@app.route('/currency/<currency_id>', methods=['DELETE'])
def delete_currency(currency_id):
    int_id = int(currency_id)
    cur = CurrencyModel.query.get(int_id)
    if cur:
        db.session.delete(cur)
        db.session.commit()
        return jsonify({'message': 'Currency deleted successfully'})
    return jsonify({'error': 'Currency not found'}), 404

@app.route('/currency', methods=['POST'])
def create_currency():
    data = request.get_json()
    cur = CurrencySchema().load(data)
    if cur:
        db.session.add(cur)
        db.session.commit()
        return jsonify({'message': 'Currency created successfully'})
    return jsonify({'error': 'Bad Currency data'}), 400

### Expences records endoints

@app.route('/records', methods=['GET'])
def get_records():
    user_id = None
    if request.args.get('user_id'):
        user_id = int(request.args.get('user_id'))
    currency_id = None
    if request.args.get('currency_id'):
        currency_id = int(request.args.get('currency_id'))
    
    filtered_records = []
    if user_id is None and currency_id is None:
        filtered_records = RecordModel.query.all()
    elif user_id is None:
        filtered_records = db.session.query(RecordModel).filter(RecordModel.currency_id == currency_id)
    elif currency_id is None:
        filtered_records = db.session.query(RecordModel).filter(RecordModel.user_id == user_id)
    else:
        filtered_records = db.session.query(RecordModel).filter(RecordModel.user_id == user_id, RecordModel.currency_id == currency_id)

    return jsonify(RecordSchema().dump(filtered_records, many = True))

@app.route('/record', methods=['POST'])
def add_record():
    data = request.get_json()
    rec = RecordSchema().load(data)
    if rec:
        db.session.add(rec)
        db.session.commit()
        return jsonify({'message': 'Expencies record created successfully'})
    return jsonify({'error': 'Bad Expencies Record data'}), 400

### application run

if __name__ == '__main__':
    app.run(debug=True)
