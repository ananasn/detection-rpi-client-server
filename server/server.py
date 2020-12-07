#!venv/bin/python

import cherrypy


class Detector(object):
    @cherrypy.expose
    def index(self):
        return 'Detection system based on neural networks'

    @cherrypy.expose
    def detect(self, entity='empty', label='empty'):
        print(f"I'm detect a {entity} with the label {label}. ")
        return


if __name__ == '__main__':
    cherrypy.quickstart(Detector())
