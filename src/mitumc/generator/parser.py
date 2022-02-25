import json

class JSONParser(object):
    def toString(seal):
        return json.dumps(seal)

    def toFile(seal, fname):
        with open(fname, 'w') as fp:
            json.dump(seal, fp, indent=4)