# /run.py
from app import create_app

# 创建应用实例
app = create_app()

if __name__ == '__main__':
    app.logger.info("Starting FlaskStarterKit service...")
    app.run(host='0.0.0.0', port=5000, debug=True)