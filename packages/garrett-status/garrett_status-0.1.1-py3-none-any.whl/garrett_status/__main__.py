from .app import app

def main():
    app.run(host='0.0.0.0', port=9090)
