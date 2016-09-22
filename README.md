# LGSmartTV

Classe para fazer interface com a minha Smart TV LG, podendo ler status da TV (volume, canais, aplicativos e status) enviar
comandos (pressionamento de qualquer tecla do controle remoto, trocar de canal, alterar volume, iniciar e fechar aplicativos,
controlar o cursos do mouse na tela e o envio de digitação nos campos de texto).

Essa classe ainda não está completamente pronta, estou desenvolvendo uma solução de automação para minha casa e para essa 
interface estou me baseando nesse manual da API da LG:
[UDAP Specifications](http://developer.lgappstv.com/TV_HELP/index.jsp?topic=%2Flge.tvsdk.references.book%2Fhtml%2FUDAP%2FUDAP%2FLG+UDAP+2+0+Service+Profiles.htm)

## Como usar

Vou providenciar a instalação via PyPi, mas por enquanto você deve fazer assim:

**Baixe o diretório LGSmartTV e coloque dentro do diretóri onde está seu script**

### Exemplo de uso

```python
# coding=utf-8
import os
from LGSmartTV import LGSmartTV

param = LGSmartTV.search()
# "LGSmartTV.search()" retorna um dicionário com a estrutura:
#  {'ip': '10.0.0.1', 'port': 8080, 'xml': 'http://10.0.0.1:8080/udap/api/data?target=netrcu.xml'}
#  ** "xml" é a URL onde se obtém o XML com os detalhes do protocolo. Na minha TV não consigo 
#     obter esse XML, não sei se é um problema da minha TV, precisava testar em outra TV
#
# ** Se não for localizada nenhuma Smart TV LG na rede "LGSmartTV.search()" retornará "None"

if param:
    # Cria o objeto TV passando "param" como parametros
    # ** Se você já tem os parametros da TV pode pular o "LGSmartTV.search()"
    Tv = LGSmartTV(param)     
    
    # Manda a TV exibir na tela a "pairing key" para poder parear com ela
    Tv.display_pairing_key()  
    
    # Faz o pareamento, passando como parametro a "pairing key" vista na tela
    #  -> Se você já tiver a "pairing key" pode pular o "display_pairing_key()"
    Tv.pairing(000000)
    
    # Retorna um dicionário com os detalhes do canal atual da TV
    channel = Tv.query.current_channel()
    
    # Retorna a lista de canais sintinizados na TV
    channel_list = Tv.query.channel_list()
    
    # Retorna um dicionário com os detalhes do volume atual da TV
    Tv.query.volume()

    # Tira um print da tela da TV e salva a imagem no arquivo indicado
    Tv.query.screen_capture(os.path.expanduser('~/tela.jpg')) 

    # Retorna o modo de operação atual da TV
    #   0 => modo controle remoto
    #   1 => modo touchpad 
    Tv.query.operation_mode()

    # Retorna uma lista de dicionários com os dados dos aplicativos instalados na TV
    aplicativos = Tv.query.app_list()  

    # Faz o download do icone do aplicativo passado como parâmetro e salva a imagem no arquivo indicado
    for aplicativo in aplicativos:
        Tv.query.app_icon(aplicativo['auid'], os.path.expanduser('~/' + aplicativo['name'] + '.png'))

    # Retorna o número de aplicativos da categoria passada como parâmetro
    # Categorias :1 = All apps
    #             2 = Premium
    #             3 = My Apps
    Tv.query.app_count(1) 

```
