# -*- coding:utf-8 -*-

from aigc_intent_solt.models.chatbot_model import ChatbotModel
from aigc_intent_solt.utils.app_init import before_init
from aigc_intent_solt.utils.helpers import load_all_scene_configs
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from aigc_intent_solt.utils.db_utils import init_db

app = Flask(__name__)
CORS(app)

# 实例化ChatbotModel
chatbot_model = ChatbotModel(load_all_scene_configs())


@app.route('/multi_question', methods=['POST'])
def api_multi_question():
    data = request.json
    question = data.get('question')
    session_id = data.get('session_id')
    if not question:
        return jsonify({"error": "No question provided"}), 400

    response = chatbot_model.process_multi_question(question, session_id)
    return jsonify({"answer": response})


@app.route('/', methods=['GET'])
def index():
    return send_file('demo/user_input.html')


if __name__ == '__main__':
    before_init()
    init_db()
    app.run(host='0.0.0.0',port=5003, debug=True)
