import tkinter as tk
from tkinter import scrolledtext, messagebox
import ctypes
import json
import os

# 修复Windows高DPI模糊
ctypes.windll.shcore.SetProcessDpiAwareness(1)
CONFIG_FILE = "rules_config.json"

# 加载所有规则
def load_all_rules():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["base_rules"] + data["custom_rules"]

# 添加自定义规则到JSON
def add_custom_rule(rule):
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    data["custom_rules"].append(rule)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 生成语法
def generate_syntax():
    domain = entry_domain.get().strip()
    if not domain:
        text_result.delete(1.0, tk.END)
        text_result.insert(tk.END, "⚠️ 请输入目标域名！")
        return

    res = []
    for rule in load_all_rules():
        try:
            syntax = rule["template"].format(domain=domain)
            res.append(f"【{rule['name']}】\n{syntax}\n\n")
        except:
            res.append(f"【{rule['name']}】\n{rule['template']}\n\n")
    
    text_result.delete(1.0, tk.END)
    text_result.insert(tk.END, "".join(res))

# 界面添加规则
def add_rule_ui():
    name = entry_name.get().strip()
    template = text_template.get("1.0", tk.END).strip()
    if not name or not template:
        messagebox.showwarning("提示", "名称和模板不能为空！")
        return
    add_custom_rule({"name": name, "template": template})
    entry_name.delete(0, tk.END)
    text_template.delete(1.0, tk.END)
    messagebox.showinfo("成功", "规则已保存！")

# 界面初始化
root = tk.Tk()
root.title("谷歌语法生成工具")
root.geometry("700x750")
root.minsize(500, 500)
FONT = ("微软雅黑", 11)
FONT_BOLD = ("微软雅黑", 11, "bold")

# 生成区域
frame_gen = tk.Frame(root, padx=10, pady=8)
frame_gen.pack(fill=tk.X)
tk.Label(frame_gen, text="目标域名:", font=FONT).pack(side=tk.LEFT)
entry_domain = tk.Entry(frame_gen, font=FONT)
entry_domain.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
tk.Button(frame_gen, text="生成语法", command=generate_syntax, font=FONT_BOLD, bg="#409EFF", fg="white").pack(side=tk.LEFT)

# 添加规则区域
frame_add = tk.LabelFrame(root, text="自定义添加规则", font=FONT_BOLD, padx=10, pady=8)
frame_add.pack(fill=tk.X, padx=10, pady=5)
tk.Label(frame_add, text="规则名称:", font=FONT).grid(row=0, column=0, sticky="w", padx=5, pady=3)
entry_name = tk.Entry(frame_add, font=FONT)
entry_name.grid(row=0, column=1, sticky="we", padx=5, pady=3)
tk.Label(frame_add, text="规则模板:\n{domain}=目标域名", font=FONT).grid(row=1, column=0, sticky="nw", padx=5, pady=3)
text_template = scrolledtext.ScrolledText(frame_add, font=FONT, height=4)
text_template.grid(row=1, column=1, sticky="we", padx=5, pady=3)
tk.Button(frame_add, text="添加规则", command=add_rule_ui, font=FONT_BOLD, bg="#67C23A", fg="white").grid(row=2, column=1, sticky="e", padx=5)
frame_add.columnconfigure(1, weight=1)

# 结果区域
text_result = scrolledtext.ScrolledText(root, font=("微软雅黑", 10), wrap=tk.WORD, padx=10, pady=8)
text_result.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

root.mainloop()