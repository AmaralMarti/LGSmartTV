# coding=utf-8
import httplib
import socket
import xml.etree.ElementTree as Etree
import urllib
from LGSmartTVQuery import LGSmartTVQuery

header = {"Content-Type": "application/atom+xml", "USER-AGENT": "UDAP/2.0"}


class LGSmartTV:
    """
    Classe para interface com SmartTV LG via ethernet
    """

    @classmethod
    def search(cls):
        request = 'M-SEARCH * HTTP/1.1' + '\r\n' + \
                  'HOST: 239.255.255.250:1900' + '\r\n' + \
                  'MAN: "ssdp:discover"' + '\r\n' + \
                  'MX: 3' + '\r\n' + \
                  'ST: udap:rootservice' + '\r\n' + \
                  'USER-AGENT: UDAP/2.0' + '\r\n' + '\r\n'

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(3)
        sock.sendto(request, ('239.255.255.250', 1900))
        try:
            text_response, _ = sock.recvfrom(512)
        except socket.timeout:
            return None
        text_response = urllib.unquote(text_response)
        text_response = text_response.split('\r\n')

        url_xml = ''
        for line in text_response:
            if line.split(' ')[0] == 'LOCATION:':
                url_xml = line.split(' ')[1]
                break

        if url_xml == '':
            return None

        ip = url_xml.split('://')[1]
        ip = ip.split(':')[0]

        port = url_xml.split('://')[1]
        port = port.split(':')[1]
        port = port.split('/')[0]

        url = url_xml.split(port)[1]

        conn = httplib.HTTPConnection(ip, port=port)
        conn.request('GET', url, '', headers=header)

        tv_lg = False

        xml = Etree.fromstring(conn.getresponse().read())
        device = xml.find('device')
        if device:
            manufacturer = device.find('manufacturer')
            device_type = device.find('deviceType')
            if ('LG' in manufacturer.text) and ('TV' in device_type.text):
                tv_lg = True

        if tv_lg:
            return {'ip': ip, 'port': port}
        else:
            return None

    def __init__(self, connection_parameters):
        self.ip = connection_parameters['ip']
        self.port = connection_parameters['port']
        self.pairing_key = 0
        self.paried = False
        self.id_session = 0
        self.query = LGSmartTVQuery(self)

    def __send_request(self, command):
        conn = httplib.HTTPConnection(self.ip, port=self.port)
        conn.request('POST', '/udap/api/pairing', command, headers=header)
        http_response = conn.getresponse()
        return http_response.reason == 'OK'

    def pairing_connect(self, pairing_key):
        """Se conecta com a TV"""
        command = '<?xml version = "1.0" encoding = "utf-8"?>' + \
                  '<envelope>' + \
                  '    <api type = "pairing">' + \
                  '        <name>hello</name>' + \
                  '        <value>' + str(pairing_key) + '</value>' + \
                  '        <port>' + str(self.port) + '</port>' + \
                  '    </api>' + \
                  '</envelope>'

        self.paried = self.__send_request(command)

        if self.paried:
            self.pairing_key = pairing_key

        return self.paried

    def pairing_disconnect(self):
        """Se desconecta da TV"""
        command = '<?xml version = "1.0" encoding = "utf-8"?>' + \
                  '<envelope>' + \
                  '    <api type = "pairing">' + \
                  '        <name>byebye</name>' + \
                  '        <port>' + str(self.port) + '</port>' + \
                  '    </api>' + \
                  '</envelope>'

        self.paried = not self.__send_request(command)
        return not self.paried

    def display_pairing_key(self):
        """Mosta a pairing key na tela da TV."""
        command = '<?xml version = "1.0" encoding = "utf-8"?>' + \
                  '<envelope>' + \
                  '    <api type = "pairing">' + \
                  '        <name>showKey</name>' + \
                  '    </api>' + \
                  '</envelope>'

        return self.__send_request(command)
