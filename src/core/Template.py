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
            self.context += line

    def render_search_html(self, order, song_name, play_url, download_url, source = 'QQ'):
        return self.context.format(ORDER = order,
                                   SONG_NAME =  song_name,
                                   PLAY_URL = play_url,
                                   DOWNLOAD_URL = download_url,
                                   SOURCE = source)

    def render_player_html(self, song_name, song_image, download_url, singer_name):
        return self.context.format(SONG_IMAGE = song_image,
                                   SONG_NAME =  song_name,
                                   DOWNLOAD_URL = download_url,
                                   SINGER = singer_name)

if __name__ == '__main__':
    t = Template()
    t.load_from_file('../site/template/search_result.html')
    print(t.render_search_html(order = 'HFBFT33', song_name = '她说', play_url = 'ddd', download_url = 'dddurl'))

    t.load_from_file('../site/template/player.html')
    print(t.render_player_html(song_name = 'Get it on the floor', song_image = 'https://xxxx',
                               download_url = 'https://yyyy', singer_name = 'VAVA'))
