import os

class Template(object):
    def __init__(self):
        self.template = ''
        self.template_file = ''
        self.context = ''

    def load_from_file(self, template_file):
        if not os.path.isfile(template_file):
            return

        self.template_file = template_file
        f = open(template_file, 'r')
        self.context = ''
        for line in f.readlines():
            self.context += line.strip()

    def render(self, _id, name):
        return self.context.format(ID = _id, NAME =  name)

if __name__ == '__main__':
    t = Template()
    t.load_from_file('web/template/table.template')
    print(t.render(_id = 'HFBFT33', _name = '她说'))
