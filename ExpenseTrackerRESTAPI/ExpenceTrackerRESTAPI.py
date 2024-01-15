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


@app.route('/category/<category_id>', methods=['GET'])
def get_category(category_id):
    int_id = int(category_id)
    category = categories.get(int_id)
    if category:
        return jsonify(category)
    return jsonify({'error': 'Category not found'}), 404


@app.route('/category/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    int_id = int(category_id)
    if int_id in categories.keys():
        del categories[int_id]
        return jsonify({'message': 'Category deleted successfully'})
    return jsonify({'error': 'Category not found'}), 404


@app.route('/category', methods=['POST'])
def create_category():
    data = request.get_json()
    category_id = int(data.get('id'))
    name = data.get('name')

    if category_id and name:
        categories[category_id] = {'id': category_id, 'name': name}
        return jsonify({'message': 'Category created successfully'})
    return jsonify({'error': 'Invalid data'}), 400


@app.route('/category', methods=['GET'])
def get_all_categories():
    return jsonify(list(categories.values()))



@app.route('/record', methods=['GET'])
def get_records():
    user_id = int(request.args.get('user_id'))
    category_id = int(request.args.get('category_id'))

    if not user_id and not category_id:
        return jsonify({'error': 'Missing parameters. Please provide user_id or category_id'}), 400

    filtered_records = []
    for record_id, record in records.items():
        if (not user_id or record['user_id'] == user_id) and (not category_id or record['category_id'] == category_id):
            filtered_records.append(record)

    return jsonify(filtered_records)


if __name__ == '__main__':
    app.run(debug=True)
