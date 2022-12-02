from application import app_init

if __name__ == '__main__':
    dev_app = app_init(env='development')
    dev_app.run(port=8000)