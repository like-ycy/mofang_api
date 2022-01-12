from application import init_app, Flask

app: Flask = init_app()

if __name__ == '__main__':
    app.run()
