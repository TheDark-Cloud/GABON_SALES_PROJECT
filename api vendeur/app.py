from config import app, create_app, create_tables



if __name__ == '__main__':
    app = create_app(app)
    create_tables(app)
    app.run()
