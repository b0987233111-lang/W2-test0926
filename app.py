from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
    topic = ""
    feedback = ""
    student_answer = ""
    question_text = "請先選擇學習主題"
    
    if request.method == "POST":
        topic = request.form.get("topic", "")
        action = request.form.get("action", "")
        print("我選擇的主題:", topic)
        
        # 根據選擇的主題出題與判斷答案
        if topic == "輸入輸出":
            question_text = "Python 使用哪個函數顯示文字？"
            if action == "check":
                student_answer = request.form.get("student_answer", "")
                if student_answer == "print":
                    feedback = "答對了！"
                else:
                    feedback = "答錯了，請再試一次！"
                    
        elif topic == "條件判斷":
            question_text = "Python 用來判斷條件的關鍵字是什麼？"
            if action == "check":
                student_answer = request.form.get("student_answer", "")
                if student_answer == "if":
                    feedback = "答對了！"
                else:
                    feedback = "答錯了，請再試一次！"
                    
        elif topic == "迴圈":
            question_text = "Python 用來建立固定次數迴圈的指令是什麼？"
            if action == "check":
                student_answer = request.form.get("student_answer", "")
                if student_answer == "for":
                    feedback = "答對了！"
                else:
                    feedback = "答錯了，請再試一次！"
                    
        elif topic == "串列":
            question_text = "Python 建立串列時要使用哪種括號？"
            if action == "check":
                student_answer = request.form.get("student_answer", "")
                if student_answer == "[]":
                    feedback = "答對了！"
                else:
                    feedback = "答錯了，請再試一次！"
                    
        else:
            question_text = "尚未選擇主題或尚未放置題目"
            
    return render_template("index.html",
                           topic=topic,
                           question_text=question_text,
                           feedback=feedback
                           )

if __name__ == "__main__":
    app.run(debug=True, port=5001)