# ⛪ 河南宗教知识竞赛 · 一键答题脚本

[![Python](https://img.shields.io/badge/Python-≥3.7-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache--2.0-green)](LICENSE)
[![Repo](https://img.shields.io/badge/GitHub-ReligionExamAutoSubmit-orange?logo=github)](https://github.com/CutelyRose/henan_ReligionExam)

---

## 📌 项目简介
- 自动完成 **hnjingsai.cn** 2025 宗教知识竞赛全流程：  
  `验证码识别 → 登录 → 获取试卷 → 自动填答案 → 交卷`
- 本地 OCR，无需打码平台；支持 178 所河南高校；仅供学习与交流。

---

## 🚀 快速开始



### ② 安装依赖
```bash
# 建议使用 3.7~3.10
pip install -r requirements.txt
```

### ③ 运行脚本
```bash
python religion_exam.py
```
按提示输入：
| 字段 | 示例 |
|---|---|
| school | 郑州大学 |
| username | 2025123456 |
| password | 123456 |

---

## 📂 项目结构
```
ReligionExamAutoSubmit/
├── religion_exam.py   # 主程序（直接运行）
├── requirements.txt   # 依赖列表
├── LICENSE            # Apache-2.0
├── README.md          # 本文档
└── .gitignore         # 已排除账号/日志/图片
```

---

## 🔧 依赖列表
```
requests>=2.31
loguru>=0.7
ddddocr>=1.4
```

---

## 🧪 核心原理
1. 请求验证码 → base64 解码 → `ddddocr` 本地识别
2. 学校名称映射内置 `key` → 拼接成登录账号
3. 登录成功返回 `JWT` → 后续接口带 `Authorization: Bearer`
4. 获取试卷接口自带「正确答案」→ 脚本直接打包答案
5. 延迟 300 s 模拟答题 → 调用交卷接口 → 完成

---

## ⚠️ 注意事项
- 仅供**学习 Python 网络/OCR/自动化**用途，禁止商用或恶意刷分
- 若官方接口变动，请在 Issue 区友好交流，欢迎 PR
- 验证码识别率非 100%，失败可重试一次

---

## 📜 许可证
[Apache License 2.0](LICENSE)  
Copyright © 2025 CutelyRose

---

如果帮到你，给个 ⭐ Star 再走~
```
