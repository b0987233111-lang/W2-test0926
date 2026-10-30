import os
import json
from dotenv import load_dotenv
from google import genai
from flask import Flask, render_template, request, session

# 讀取 .env 檔案與初始化 Gemini 用戶端
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # 設定 Flask Session 密鑰

# 建立 AI 出題函式並呼叫 Gemini API 自動出題
def generate_question(topic):
    prompt = f"""
    請根據主題「{topic}」產生一道 Python 初學者的四選一選擇題。
    只能有一個正確答案。
    請回傳 JSON 格式，包含 question、option1、option2、option3、option4、answer、explanation 七個欄位。
    answer 只能填入 A、B、C 或 D。
    explanation 請用繁體中文，50字以內。
    """
    
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",  # 對應講義指定的模型
        contents=prompt,
        config={"response_mime_type": "application/json"}
    )
    
    try:
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3].strip()
        question_data = json.loads(text)
        return question_data
    except Exception as e:
        print("JSON 解析錯誤：", e)
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    question_data = session.get("question_data")
    is_correct = None
    
    if request.method == "POST":
        action = request.form.get("action")
        
        # 點擊產生題目按鈕
        if action == "generate":
            topic = request.form.get("topic")
            if topic:
                question_data = generate_question(topic)
                session["question_data"] = question_data  # 用 Session 保存題目與答案
                session["selected_answer"] = None
                
        # 判斷學生答案並顯示 AI 解釋
        elif action == "check":
            student_answer = request.form.get("student_answer")
            session["selected_answer"] = student_answer
            if question_data:
                correct_answer = question_data.get("answer")
                is_correct = (student_answer == correct_answer)

    return render_template(
        "index.html", 
        question_data=question_data, 
        selected_answer=session.get("selected_answer"),
        is_correct=is_correct
    )

if __name__ == "__main__":
    app.run(debug=True)