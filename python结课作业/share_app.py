import subprocess
import time
import sys
from pyngrok import ngrok

def share_streamlit_app(port=8503):
    # 启动Streamlit应用
    streamlit_process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", str(port)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # 等待应用启动
    time.sleep(5)
    
    try:
        # 设置ngrok隧道
        public_url = ngrok.connect(port)
        print("\n🚀 Streamlit应用已启动并通过ngrok分享！")
        print(f"🔗 本地访问地址: http://localhost:{port}")
        print(f"🌐 公共分享地址: {public_url}")
        print("\n📝 分享说明：")
        print("   - 复制上面的公共分享地址发送给你的朋友")
        print("   - 保持此终端窗口打开，应用才能持续运行")
        print("   - 按 Ctrl+C 关闭应用和分享服务")
        print("\n🤝 你的朋友可以通过公共分享地址访问你的应用！")
        
        # 保持程序运行
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 正在关闭应用和分享服务...")
        ngrok.kill()
        streamlit_process.terminate()
        print("✅ 应用和分享服务已关闭")
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        ngrok.kill()
        streamlit_process.terminate()

if __name__ == "__main__":
    share_streamlit_app()