from pymitter import EventEmitter

import morepath


class App(morepath.App):
    signal = EventEmitter()
