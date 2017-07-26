import json

import ansible
from twisted.web import static, resource
from ansible.parsing.vault import VaultLib

class Root(static.File):
    isLeaf = False

    def __init__(self, path, defaultType="text/html", ignoredExts=(), registry=None, allowExt=0):
        static.File.__init__(self, path)


class Crypt(resource.Resource):
    isLeaf = True

    # noinspection PyBroadException
    def render(self, request):

        request.setHeader("Content-Type", "application/json; charset=utf-8")

        try:
            body = json.loads(request.content.read())
        except:
            request.setResponseCode(400)
            return json.dumps({"value": "bad input object"})

        if body.get("password"):
            e = VaultLib(body["password"])

            source = body.get("source", "")

            if source.startswith("$ANSIBLE_VAULT"):
                try:
                    response_text = e.decrypt(source)
                except ansible.errors.AnsibleError as e:
                    response_text = e.message
            elif source == "":
                response_text = "trying to encrypt empty string"
                request.setResponseCode(400)
            else:
                try:
                    response_text = e.encrypt(source)
                except ansible.errors.AnsibleError as e:
                    response_text = e.message
        else:
            request.setResponseCode(400)
            response_text = "password not specified"

        return json.dumps({"value": response_text})
