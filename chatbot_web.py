import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Cấu hình thư viện Generative AI phiên bản ổn định
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Thiết lập model và công cụ tìm kiếm
model = genai.GenerativeModel(
    model_name="gemini-3-flash-preview", 
    # Nếu vẫn lỗi 500, Nam hãy tạm thời tắt dòng tools bên dưới bằng dấu #
    #tools=[{"google_search_retrieval": {}}], 
    system_instruction="Bạn là Đại sứ Văn hóa Đọc Việt Nam. Hãy trả lời chính xác, không bịa đặt."
)

chat_session = model.start_chat(history=[])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get("message")
    try:
        response = chat_session.send_message(user_msg)
        return jsonify({"reply": response.text})
    except Exception as e:
        print("LỖI THỰC TẾ:", e)
        return jsonify({"reply": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)