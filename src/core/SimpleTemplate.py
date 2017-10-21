import os
from jinja2 import Template

class SimpleTemplate(object):
    def __init__(self):
        self.template = Template('')
        self.context = ''

    def load_from_file(self, template):
        if not os.path.isfile(template):
            return

        f = open(template, 'r')
        self.context = ''
        for line in f.readlines():
            self.context += line
        self.template = Template(self.context)
        f.close()

    def render(self, varibales):
        return self.template.render(varibales)


if __name__ == '__main__':
    t = SimpleTemplate()

    t.load_from_file('../site/template/player.jinja2')
    var = {
        'SONG_NAME'    : '1',
        'SINGER'       : '2',
        'DOWNLOAD_URL' : '3',
        'SONG_IMAGE'   : '4'}

    txt = t.render(var)
    print(txt)
