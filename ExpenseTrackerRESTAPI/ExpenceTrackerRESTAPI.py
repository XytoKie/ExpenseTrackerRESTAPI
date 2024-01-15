from flask import Flask, jsonify, request

app = Flask(__name__)

users = {}
categories = {}
records = {}

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    int_id = int(user_id)
    user = users.get(int_id)
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404


@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    int_id = int(user_id)
    if int_id in users.keys():
        del users[int_id]
        return jsonify({'message': 'User deleted successfully'})

    return jsonify({'error': 'User not found'}), 404


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    user_id = int(data.get('id'))
    name = data.get('name')

    if user_id and name:
        users[user_id] = {'id': user_id, 'name': name}
        return jsonify({'message': 'User created successfully'})

    return jsonify({'error': 'Invalid data'}), 400


@app.route('/users', methods=['GET'])
def get_all_users():
    return jsonify(list(users.values()))




if __name__ == '__main__':
    app.run(debug=True)
