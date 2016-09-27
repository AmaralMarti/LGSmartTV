# coding=utf-8
import httplib
import xml.etree.ElementTree as Etree
import LGSmartTV


class LGSmartTVQuery:

    def __init__(self, lgsmarttv):
        self.LGSmartTV = lgsmarttv
        self.ip = self.LGSmartTV.ip
        self.port = self.LGSmartTV.port

    def __send_request(self, request):
        if not self.LGSmartTV.paried:
            raise Exception('Unpaired')

        conn = httplib.HTTPConnection(self.ip, port=self.port)
        conn.request('GET', request, '', headers=LGSmartTV.header)
        return conn.getresponse().read()

    def current_channel(self):
        """Obtem os dados do canal atual em que a TV esta."""
        http_response = self.__send_request('/udap/api/data?target=cur_channel')

        result = dict()

        root = Etree.fromstring(http_response)
        data_list = root.find('dataList')
        if data_list:
            if ('name' in data_list.attrib) and (data_list.attrib['name'] == 'Current Channel Info'):
                data = data_list.find('data')
                if data:
                    result['ch_type'] = data.find('chtype').text
                    result['major'] = data.find('major').text
                    result['display_major'] = data.find('displayMajor').text
                    result['minor'] = data.find('minor').text
                    result['display_minor'] = data.find('displayMinor').text
                    result['source_index'] = data.find('sourceIndex').text
                    result['physical_num'] = data.find('physicalNum').text
                    result['ch_name'] = data.find('chname').text
                    result['prog_name'] = data.find('progName').text
                    result['audio_ch'] = data.find('audioCh').text
                    result['input_source_name'] = data.find('inputSourceName').text
                    result['input_source_type'] = data.find('inputSourceType').text
                    result['input_source_index'] = data.find('inputSourceIdx').text
                    result['label_name'] = data.find('labelName').text

        return result

    def channel_list(self):
        """Obtem os dados do canal atual em que a TV esta."""
        http_response = self.__send_request('/udap/api/data?target=channel_list')

        result = list()

        root = Etree.fromstring(http_response)
        data_list = root.find('dataList')
        if data_list:
            if ('name' in data_list.attrib) and (data_list.attrib['name'] == 'Channel List'):
                for data in data_list.findall('data'):
                    channel = dict()
                    channel['ch_type'] = data.find('chtype').text
                    channel['major'] = data.find('major').text
                    channel['minor'] = data.find('minor').text
                    channel['source_index'] = data.find('sourceIndex').text
                    channel['physical_num'] = data.find('physicalNum').text
                    channel['ch_name'] = data.find('chname').text

                    result.append(channel)

        return result

    def volume(self):
        """Obtem os dados do volume em que a TV esta."""
        http_response = self.__send_request('/udap/api/data?target=volume_info')

        result = dict()

        root = Etree.fromstring(http_response)
        data_list = root.find('dataList')
        if data_list:
            if ('name' in data_list.attrib) and (data_list.attrib['name'] == 'Volume Info'):
                data = data_list.find('data')
                if data:
                    result['mute'] = data.find('mute').text
                    result['min_level'] = data.find('minLevel').text
                    result['max_level'] = data.find('maxLevel').text
                    result['level'] = data.find('level').text

        return result

    def screen_capture(self, file_name):
        """Captura a imagem da tela da TV e salva no arquivo indicado."""
        http_response = self.__send_request('/udap/api/data?target=screen_image')

        f = open(file_name, 'wb')
        f.write(http_response)

    def operation_mode(self):
        """Obtem os dados do volume em que a TV esta."""
        http_response = self.__send_request('/udap/api/data?target=context_ui')

        result = dict()

        root = Etree.fromstring(http_response)
        data_list = root.find('dataList')
        if data_list:
            if ('name' in data_list.attrib) and (data_list.attrib['name'] == 'TV UI Mode'):
                data = data_list.find('data')
                if data:
                    result['mode_string'] = data.find('mode').text
                    if result['mode_string'] == 'VolCh':
                        result['mode'] = 0
                    else:
                        result['mode'] = 1
        return result

    def app_list(self):
        """Obtem a lista de Apps instalados na TV."""
        http_response = self.__send_request('/udap/api/data?target=applist_get&type=1&index=1&number=1024')

        result = list()

        root = Etree.fromstring(http_response)
        data_list = root.find('dataList')
        if data_list:
            if ('name' in data_list.attrib) and (data_list.attrib['name'] == 'Max App List'):
                for data in data_list.findall('data'):
                    app = dict()
                    app['auid'] = data.find('auid').text
                    app['name'] = data.find('name').text
                    app['type'] = data.find('type').text
                    app['cpid'] = data.find('cpid').text
                    app['adult'] = data.find('adult').text
                    app['icon_name'] = data.find('icon_name').text

                    result.append(app)
        return result

    def app_icon(self, app_auid, file_name):
        """Salva a icone do App no arquivo indicado. (O arquivo tem que ser PNG)"""
        http_response = self.__send_request('/udap/api/data?target=appicon_get&auid=' + app_auid
                                            + '&appname=URL_Encode()')

        f = open(file_name, 'wb')
        f.write(http_response)

    def app_count(self, app_type):
        """Obtem a contagem dos Apps instalados no TV.
        Type: 1 = All apps
              2 = Premium
              3 = My Apps"""
        http_response = self.__send_request('/udap/api/data?target=appnum_get&type=' + str(app_type))

        result = dict()

        root = Etree.fromstring(http_response)
        data_list = root.find('dataList')
        if data_list:
            if ('name' in data_list.attrib) and (data_list.attrib['name'] == 'App Num'):
                data = data_list.find('data')
                if data:
                    if data.find('type').text == '1':
                        result['type'] = 'All'

                    if data.find('type').text == '2':
                        result['type'] = 'My Apps'

                    if data.find('type').text == '3':
                        result['type'] = 'Premium'

                    result['count'] = data.find('number').text

        return result
