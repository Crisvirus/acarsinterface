from datetime import datetime
import json
class Message:
    def __init__(self,timestamp,text,mtype,json_content):
        self.timestamp = timestamp
        self.text = text
        self.json_content = json_content
        self.mtype = mtype
    
    def getHTMLMessage(self):
        return self.text

    def get_text(self):
        return self.text

    def getJson(self):
        return json.dumps(self.json_content)

    def getType(self):
        return self.mtype

    def get_timestamp(self):
        return datetime.fromtimestamp(self.timestamp).strftime("%d-%m-%y %H:%M:%S")