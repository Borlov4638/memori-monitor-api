import os
from dotenv import load_dotenv
from bson import ObjectId
from flask import Flask, request, jsonify
from pymongo import MongoClient

# Загрузка переменных из файла .env
load_dotenv()

app = Flask(__name__)

# Подключение к MongoDB
mongo_host = os.getenv('MONGO_HOST', 'localhost')
mongo_port = int(os.getenv('MONGO_PORT', 27017))
mongo_db = os.getenv('MONGO_DB', 'memory')
mongo_collection = os.getenv('MONGO_COLLECTION', 'monitor')

client = MongoClient(mongo_host, mongo_port)
db = client[mongo_db]
collection = db[mongo_collection]

# Обработчик GET запроса
@app.route('/', methods=['GET'])
def get_data():
    data = list(collection.find())  # Получаем все документы из коллекции
    # Преобразуем ObjectId в строки
    serialized_data = []
    for item in data:
        item['_id'] = str(item['_id'])
        serialized_data.append(item)
    return jsonify(serialized_data), 200

# Обработчик POST запроса
@app.route('/', methods=['POST'])
def add_data():
    new_data = request.json  # Получаем данные из запроса
    if not new_data:
        return jsonify({'error': 'No data provided'}), 400
    # Вставляем данные в коллекцию
    result = collection.insert_one(new_data)
    return jsonify({'message': 'Data added successfully', 'id': str(result.inserted_id)}), 201

# Обработчик PUT запроса
@app.route('/<string:data_id>', methods=['PUT'])
def update_data(data_id):
    updated_data = request.json  # Получаем обновленные данные из запроса
    if not updated_data:
        return jsonify({'error': 'No data provided'}), 400
    # Обновляем данные в коллекции
    try:
        result = collection.update_one({'_id': ObjectId(data_id)}, {'$set': updated_data})
        if result.modified_count == 0:
            return jsonify({'error': 'Data not found or no changes were made'}), 404
        return jsonify({'message': 'Data updated successfully'}), 200
    except:
        return jsonify({'error': 'Invalid ID'}), 400

if __name__ == '__main__':
    app.run(port=int(os.getenv('FLASK_PORT', 8080)), host='0.0.0.0')
