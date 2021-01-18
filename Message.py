from datetime import datetime
import json
import jinja2
class Message:
    def __init__(self,id,timestamp,text,mtype,json_content):
        self.timestamp = timestamp
        self.text = text
        self.json_content = json_content
        self.mtype = mtype
        self.id = id
    
    def getHTMLMessage(self):
        templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
        templateEnv = jinja2.Environment(loader=templateLoader)
        if self.mtype == "text":
            template = templateEnv.get_template('text_message_template.html')
            return template.render(msg = self)
        if self.mtype == "libacars":
            template = templateEnv.get_template('json_message_template.html')
            return template.render(msg = self)

        if self.mtype == 'route':
            template = templateEnv.get_template('route_message_template.html')
            return template.render(msg = self)
        return "TODO"

    def get_text(self):
        return self.text

    def getJson(self):
        return json.dumps(self.json_content)

    def getType(self):
        return self.mtype

    def get_timestamp(self):
        return datetime.fromtimestamp(self.timestamp).strftime("%d-%m-%y %H:%M:%S")