import streamlit as st
import re

# 頁面配置
st.set_page_config(page_title="Universal Converter", page_icon="⚖️")

# --- 語系設定 ---
if 'lang' not in st.session_state:
    st.session_state.lang = '中文'

def toggle_lang():
    st.session_state.lang = 'English' if st.session_state.lang == '中文' else '中文'

st.sidebar.button("🌐 Switch Language / 切換語言", on_click=toggle_lang)

# 翻譯字典
texts = {
    '中文': {
        'title': "⚖️ 超強全單位轉換器",
        'desc': "輸入格式：`數字+單位\\目標單位` (例如：100kg\\lb)",
        'input_label': "請輸入轉換指令：",
        'btn': "立即轉換",
        'err_format': "⚠️ 格式錯誤！請參考範例。",
        'err_parse': "❌ 無法解析內容",
        'err_notfound': "❓ 找不到對應單位",
        'weight_label': "⚖️ 重量轉換",
        'length_label': "📏 長度轉換",
        'temp_label': "🌡️ 溫度轉換"
    },
    'English': {
        'title': "⚖️ Universal Unit Converter",
        'desc': "Format: `value+unit\\target` (e.g., 100kg\\lb)",
        'input_label': "Enter conversion command:",
        'btn': "Convert",
        'err_format': "⚠️ Format error! Use the backslash.",
        'err_parse': "❌ Parse failed",
        'err_notfound': "❓ Units not found",
        'weight_label': "⚖️ Weight",
        'length_label': "📏 Length",
        'temp_label': "🌡️ Temperature"
    }
}

curr = texts[st.session_state.lang]

# --- 核心邏輯 ---
def universal_converter(input_str):
    weight_data = {
        "g": 1, "克": 1, "公克": 1, "kg": 1000, "公斤": 1000,
        "lb": 453.592, "磅": 453.592, "oz": 28.3495, "盎司": 28.3495,
        "台斤": 600, "斤": 500, "市斤": 500, "克拉": 0.2
    }
    length_data = {
        "cm": 1, "公分": 1, "m": 100, "公尺": 100, "km": 100000, "公里": 100000,
        "in": 2.54, "英寸": 2.54, "ft": 30.48, "英尺": 30.48,
        "yd": 91.44, "碼": 91.44, "mi": 160934.4, "英里": 160934.4
    }

    if "\\" not in input_str:
        return curr['err_format']
    
    try:
        source_part, target_unit = input_str.split("\\")
        target_unit = target_unit.strip().lower()
        match = re.match(r"([0-9.]+)\s*([^\s]+)", source_part.strip())
        if not match: return curr['err_parse']
        
        val = float(match.group(1))
        source_unit = match.group(2).lower()

        # 重量
        if source_unit in weight_data and target_unit in weight_data:
            res = (val * weight_data[source_unit]) / weight_data[target_unit]
            return f"{curr['weight_label']}: {val:,} {source_unit} ➡ {res:,.4f} {target_unit}"
        
        # 長度
        if source_unit in length_data and target_unit in length_data:
            res = (val * length_data[source_unit]) / length_data[target_unit]
            return f"{curr['length_label']}: {val:,} {source_unit} ➡ {res:,.4f} {target_unit}"
            
        # 溫度
        if source_unit in ["f", "華氏", "farenheit"] and target_unit in ["c", "攝氏", "celsius"]:
            return f"{curr['temp_label']}: {val}°F ➡ {(val-32)*5/9:.2f}°C"
        if source_unit in ["c", "攝氏", "celsius"] and target_unit in ["f", "華氏", "farenheit"]:
            return f"{curr['temp_label']}: {val}°C ➡ {(val*9/5)+32:.2f}°F"

        return curr['err_notfound']
    except:
        return curr['err_parse']

# --- UI 渲染 ---
st.title(curr['title'])
st.info(curr['desc'])

user_input = st.text_input(curr['input_label'], key="input_field")

if st.button(curr['btn']):
    if user_input:
        result = universal_converter(user_input)
        if "⚖️" in result or "📏" in result or "🌡️" in result:
            st.success(result)
        else:
            st.error(result)
