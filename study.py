import tkinter as tk
from tkinter import font as tkfont
from openai import OpenAI
import re
import time

# 初始化OpenAI客户端(中转的限速开发中,先提供源码)
client = OpenAI(
    api_key="",  # 替换为实际API Key
    base_url="" #API请求地址
)

last_request_time = 0

def get_response():
    global last_request_time
    current_time = time.time()
    if current_time - last_request_time < 40:
        response_text.insert(tk.END, "请等待 40 秒后再提问。\n")
        return
    last_request_time = current_time

    question = text_input.get("1.0", "end-1c")  # 获取用户输入的问题
    if len(question) > 30:
        response_text.insert(tk.END, "输入字数超过限制，请重新输入。\n")
        return
    
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': f"请你作为一个高中数学老师以简短的话语解答这个问题(与数学无关的问题不回答,回答输出文字,使用md格式):{question}"}
            ]
        )
        response = completion.choices[0].message.content  # 获取回答内容
        render_markdown(response)  # 渲染Markdown内容
    except Exception as e:
        response_text.insert(tk.END, f"请求失败：{str(e)}\n")

def render_markdown(markdown):
    # 清空现有内容
    response_text.delete("1.0", tk.END)
    
    # 加载自定义字体
    custom_font = tkfont.Font(family="SimSun", size=14, weight="bold")
    custom_latex_font = tkfont.Font(family="SimSun", size=14, weight="bold")
    
    # 解析Markdown内容
    lines = markdown.split("\n")
    for line in lines:
        # 处理LaTeX公式
        latex_match = re.search(r'\\\[.*?\\\]', line, re.DOTALL)
        if latex_match:
            latex_content = latex_match.group().strip()
            line = line.replace(latex_content, '')
            response_text.insert(tk.END, latex_content + "\n", "latex")
        
        # 去除Markdown格式标识
        line = re.sub(r'^# ', '', line)  # 标题一级
        line = re.sub(r'^## ', '', line)  # 标题二级
        line = re.sub(r'^\* ', '', line)
        line = re.sub(r'^- ', '', line)
        line = re.sub(r'^> ', '', line)
        line = re.sub(r'\*\*(.*?)\*\*', r'\1', line)  # 双星号加粗
        line = re.sub(r'\*(.*?)\*', r'\1', line)  # 单星号斜体
        
        # 插入处理后的文本
        if line.strip():
            response_text.insert(tk.END, line.strip() + "\n", "normal")

    # 应用样式
    response_text.tag_config("latex", font=custom_latex_font)
    response_text.tag_config("normal", font=custom_font)
    response_text.tag_config("heading1", font=tkfont.Font(family="SimSun", size=18, weight="bold"))
    response_text.tag_config("heading2", font=tkfont.Font(family="SimSun", size=16, weight="bold"))
    response_text.tag_config("bullet", font=tkfont.Font(family="SimSun", size=14, weight="bold"), foreground="blue")
    response_text.tag_config("quote", font=tkfont.Font(family="SimSun", size=14, weight="bold"), foreground="green")
    response_text.tag_config("bold", font=tkfont.Font(family="SimSun", size=14, weight="bold"))
    response_text.tag_config("italic", font=tkfont.Font(family="SimSun", size=14, slant="italic"))

# 创建主窗口
root = tk.Tk()
root.title("学习园地")
root.geometry("1240x720")
root.configure(bg="#F0F0F0")  # 设置背景颜色

# 创建多行输入框
text_input = tk.Text(root, height=2, width=120, font=("SimSun", 14, "bold"))
text_input.pack(pady=20, padx=20)

# 更新字数统计
def update_word_count(*args):
    word_count = len(text_input.get("1.0", "end-1c"))
    word_count_label.config(text=f"字数: {word_count}/30")

text_input.bind("<KeyRelease>", update_word_count)

# 创建字数统计标签
word_count_label = tk.Label(root, text="字数: 0/30", font=("SimSun", 14, "bold"), bg="#F0F0F0")
word_count_label.pack(pady=10, padx=20)

# 创建按钮
button_frame = tk.Frame(root, bg="#F0F0F0")
button_frame.pack(pady=10, padx=20, side=tk.RIGHT)

button = tk.Button(button_frame, text="提问", command=get_response, font=("SimSun", 14, "bold"), bg="#4CAF50", fg="white", relief=tk.RAISED, bd=10)
button.pack(pady=10, padx=20)

# 创建输出框
response_text = tk.Text(root, height=20, width=120, font=("SimSun", 14, "bold"), spacing1=5, spacing3=5)
response_text.pack(pady=20, padx=20)

# 应用大圆角样式
button.config(relief=tk.RAISED, bd=10)

# 运行主循环
root.mainloop()

