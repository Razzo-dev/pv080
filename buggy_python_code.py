# contains bunch of buggy examples, taken from:
# https://hackernoon.com/10-common-security-gotchas-in-python-and-how-to-avoid-them-e19fbe265e03
import subprocess
import pickle
import base64
import flask

app = flask(__name__)

# Input injection
def transcode_file(request, filename):
    command = 'ffmpeg -i "{source}" output_file.mpg'.format(source=filename)
    subprocess.call(command, shell=True)  # a bad idea!


# Assert statements
def is_admin(request, user):
    assert user.is_admin, 'user does not have access'
    # secure code...


# Pickles
class RunBinSh(object):
    def __reduce__(self):
        return (subprocess.Popen, (('/bin/sh',),))

def import_urlib_version(version):
    exec("import urllib%s as urllib" % version)

@app.route('/')
def index():
    module = flask.request.args.get("module")
    import_urlib_version(module)


print(base64.b64encode(pickle.dumps(RunBinSh())))

if __name__ == "__main__":
    malicious = "\nprint('IT WORKS')\nimport urllib "
    import_urlib_version(malicious)
    malicious2 = "\nprint('IT WORKS TWO') #"
    import_urlib_version(malicious2)