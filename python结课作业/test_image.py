import streamlit as st
import requests

# 测试图片URL
test_urls = [
    "https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2873330697.jpg",  # 怪奇物语
    "https://img1.doubanio.com/view/photo/s_ratio_poster/public/p2554699049.jpg",  # 权力的游戏
    "https://picsum.photos/seed/test1/300/450",  # Picsum测试图片
    "https://via.placeholder.com/300x450",  # Placeholder测试图片
]

st.title("图片加载测试")

for i, url in enumerate(test_urls):
    st.subheader(f"测试图片 {i+1}: {url}")
    
    # 检查URL是否可访问
    try:
        response = requests.get(url, timeout=5)
        st.info(f"URL状态码: {response.status_code}")
        st.info(f"Content-Type: {response.headers.get('content-type')}")
        
        # 尝试在Streamlit中显示图片
        try:
            st.image(url, width='stretch', caption=f"测试图片 {i+1}")
            st.success("图片显示成功!")
        except Exception as e:
            st.error(f"Streamlit图片显示失败: {e}")
            
            # 尝试保存图片到本地并显示
            try:
                with open(f"test_image_{i+1}.jpg", "wb") as f:
                    f.write(response.content)
                st.image(f"test_image_{i+1}.jpg", width='stretch', caption=f"本地保存的图片 {i+1}")
                st.success("本地图片显示成功!")
            except Exception as e2:
                st.error(f"本地图片显示失败: {e2}")
                
    except Exception as e:
        st.error(f"URL访问失败: {e}")
    
    st.divider()