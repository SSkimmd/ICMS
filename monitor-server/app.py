from ..server.app import App

class Monitor:
    def __init__(self, app: App):
        self.app = app
        print(self.app.extensions)


if __name__ == "__main__":
    app = App()
    app.init_extensions()
    app.start()

    monitor = Monitor(app)