# Project Migration: From Claude CLI to Gemini Native

โปรเจกต์นี้ได้รับการปรับปรุงเพื่อลดการพึ่งพา Claude Token โดยการเปลี่ยนระบบ Automation จากการเรียกใช้ `claude` CLI มาเป็นการเรียกใช้ **Gemini 1.5 Flash API** โดยตรง

## 1. ข้อมูล Source ต้นทาง (Original Source)
*   **Original Repository**: [tradermonty/claude-trading-skills](https://github.com/tradermonty/claude-trading-skills)
*   **Original Logic**: 
    *   ใช้คำสั่ง `subprocess.run(["claude", "-p", ...])` ในการรัน AI Agent
    *   พึ่งพาฟีเจอร์ `--allowedTools` ของ Claude CLI (Read, Edit, Write, Grep) เพื่อให้ AI แก้ไขไฟล์ในเครื่องได้อัตโนมัติ
    *   พึ่งพา `--output-format json` ของ Claude เพื่อรับข้อมูลแบบ Structured Data

## 2. แผนการปรับปรุง (Implementation Plan)
เป้าหมายคือการรักษาฟีเจอร์เดิมไว้ทั้งหมด (Full Feature Parity) โดยเปลี่ยนหัวใจการประมวลผล (LLM Engine)

### A. หัวใจหลัก: `scripts/gemini_adapter.py` [NEW]
เนื่องจาก Gemini API ปกติไม่สามารถแก้ไขไฟล์ในเครื่องได้ ผมจึงสร้าง **Gemini Adapter** ขึ้นมาเพื่อทำหน้าที่เป็น "Bridge":
*   **Tool Use (Function Calling)**: นิยามฟังก์ชัน `read_file`, `write_file`, `list_files`, และ `grep_search` ให้ Gemini เรียกใช้
*   **Agent Loop**: ใช้ `model.start_chat(enable_automatic_function_calling=True)` เพื่อให้ Gemini สามารถคิดและลงมือแก้ไขไฟล์ได้หลายขั้นตอนจนกว่างานจะเสร็จ (เลียนแบบ Claude CLI)
*   **JSON Extraction**: ระบบจัดการการดึง JSON ออกจาก Response ของ LLM ให้แม่นยำขึ้น

### B. การปรับปรุงไฟล์ระบบ (Modified Files)

| ไฟล์ที่แก้ไข | การเปลี่ยนแปลงหลัก |
| :--- | :--- |
| `pyproject.toml` | เพิ่ม `google-generativeai` เข้าไปใน dependencies |
| `scripts/run_skill_improvement_loop.py` | เปลี่ยนฟังก์ชัน `run_llm_review` และ `apply_improvement` จากการเรียก `claude` CLI มาเรียก `gemini_adapter.py` |
| `scripts/run_skill_generation_pipeline.py` | เปลี่ยนจุดที่เรียก `design_skill` และ `improve_skill` ให้ผ่าน Gemini Agent |
| `skills/skill-idea-miner/scripts/mine_session_logs.py` | เปลี่ยนฟังก์ชัน `abstract_with_llm` ให้ใช้ Gemini |
| `skills/skill-idea-miner/scripts/score_ideas.py` | เปลี่ยนฟังก์ชัน `score_with_llm` ให้ใช้ Gemini |

## 3. คู่มือการแก้ไข Bug ในอนาคต (Troubleshooting)

### ปัญหาเรื่องความแม่นยำของ JSON
ถ้า Gemini คืนค่า JSON ผิดรูปแบบ ให้ตรวจสอบที่:
*   ฟังก์ชัน `extract_json_from_text` ใน `scripts/gemini_adapter.py`
*   ลองปรับ `temperature` ใน `call_gemini` ให้ต่ำลง (ปัจจุบันตั้งไว้ที่ 0.2)

### ปัญหาเรื่องสิทธิ์การเข้าถึงไฟล์
ถ้า Gemini แจ้งว่าแก้ไขไฟล์ไม่ได้ ให้ดูที่:
*   ฟังก์ชัน `write_file` ใน `scripts/gemini_adapter.py`
*   ตรวจสอบว่า Path ที่ส่งเข้าไปถูกต้อง (ปัจจุบันใช้ Relative Path จาก Root)

### การสลับรุ่น AI
หากต้องการเปลี่ยนรุ่น AI (เช่น เมื่อมีการออกรุ่นใหม่กว่า):
*   แก้ไขที่ parameter `model_name` ในไฟล์ `scripts/run_skill_improvement_loop.py` หรือไฟล์อื่นๆ เป็น `"gemini-3-flash-preview"` หรือรุ่นที่ต้องการ

## 4. สภาพแวดล้อมที่จำเป็น (Environment Variables)
ต้องมีการตั้งค่าตัวแปรเหล่านี้เพื่อให้ระบบทำงานได้:
*   `GEMINI_API_KEY`: API Key จาก [Google AI Studio](https://aistudio.google.com/)
*   `FINVIZ_API_KEY`: (ถ้ามี) สำหรับสแกนหุ้น
*   `FMP_API_KEY`: สำหรับดึงข้อมูลการเงิน
