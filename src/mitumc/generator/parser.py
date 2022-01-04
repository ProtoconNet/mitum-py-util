import json

class JSONParser(object):
    def toJSONString(seal):
        return json.dumps(seal)

    def generateFile(seal, fname):
        with open(fname, 'w') as fp:
            json.dump(seal, fp, indent=4)