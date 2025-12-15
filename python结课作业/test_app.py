import streamlit as st

st.title("简单测试应用")
st.write("这是一个简单的 Streamlit 应用，用于测试 Python 3.13.7 和 Streamlit 1.52.1 的兼容性。")

# 添加一个简单的交互元素
name = st.text_input("请输入您的名字")
if name:
    st.write(f"您好，{name}！")