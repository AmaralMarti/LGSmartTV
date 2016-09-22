# coding=utf-8
import httplib
import socket
import xml.etree.ElementTree as Etree
import urllib
from LGSmartTVQuery import LGSmartTVQuery


class LGSmartTV:
    """
    Classe para interface com SmartTV LG via ethernet
    """

    _header = {"Content-Type": "application/atom+xml"}

    @classmethod
    def search(cls):
        request = 'M-SEARCH * HTTP/1.1' + '\r\n' + \
                  'HOST: 239.255.255.250:1900' + '\r\n' + \
                  'MAN: "ssdp:discover"' + '\r\n' + \
                  'MX: 3' + '\r\n' + \
                  'ST: urn:schemas-udap:service:netrcu:1' + '\r\n' + \
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

        xml = ''
        for line in text_response:
            if line.split(' ')[0] == 'LOCATION:':
                xml = line.split(' ')[1]
                break

        ip = xml.split('://')[1]
        ip = ip.split(':')[0]

        port = xml.split('://')[1]
        port = port.split(':')[1]
        port = port.split('/')[0]

        return {'ip': ip, 'port': port, 'xml': xml}

    def __init__(self, connection_parameters):
        self.ip = connection_parameters['ip']
        self.port = connection_parameters['port']
        self.xml = connection_parameters['xml']
        self.pairing_key = 0
        self.paried = False
        self.id_session = 0
        self.query = LGSmartTVQuery(self)

    def pairing(self, pairing_key):
        conn = httplib.HTTPConnection(self.ip, port=self.port)
        command = '<?xml version="1.0" encoding="utf-8"?>' + \
                  '<auth>' + \
                  '    <type>AuthReq</type>' + \
                  '    <value>' + str(pairing_key) + '</value>' + \
                  '</auth>'
        conn.request('POST', '/roap/api/auth', command, headers=self._header)
        http_response = conn.getresponse()

        root = Etree.fromstring(http_response.read())

        self.id_session = 0
        for data in root.findall('session'):
            self.id_session = data.text

        self.paried = http_response.reason == 'OK'

        if self.paried:
            self.pairing_key = pairing_key

        return self.paried

    def display_pairing_key(self):
        conn = httplib.HTTPConnection(self.ip, port=self.port)
        command = '<?xml version="1.0" encoding="utf-8"?>' + \
                  '<auth>' + \
                  '    <type>AuthKeyReq</type>' + \
                  '</auth>'
        conn.request('POST', '/roap/api/auth', command, headers=self._header)
        http_response = conn.getresponse()
        return http_response.reason == 'OK'
