#! /usr/bin/env python3
import argparse, base64, common, glob, os, platform, re, subprocess, sys, urllib.request, zipfile

def log_errors(name):
  def wrap(f):
    def result(*args, **kwargs):
      try:
        f(*args, **kwargs)
      except Exception as e:
        print(f"{name}: Failed {e}")
    return result
  return wrap

def package(version):
  zip = f"ReFira_Code_v{version}.zip"

  print('Package:', zip)
  with zipfile.ZipFile(zip, 'w', compression = zipfile.ZIP_DEFLATED, compresslevel = 9) as archive:
    for f in glob.glob("distr/**", recursive = True):
      arcname = f[len("distr/"):]
      if arcname and not os.path.basename(arcname).startswith("."):
        archive.write(f, arcname)

def github_headers():
  if os.environ.get('GITHUB_BASIC'):
    auth = 'Basic ' + base64.b64encode(os.environ.get('GITHUB_BASIC').encode('utf-8')).decode('utf-8')
  else:
    auth = 'token ' + os.environ.get('API_TOKEN')
  return {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': auth
  }

@log_errors("github_release")
def github_release(version):
  zip = f"ReFira_Code_v{version}.zip"

  data = '{"tag_name":"' + version + '","name":"' + version + '"}'
  headers = github_headers()
  resp = urllib.request.urlopen(urllib.request.Request('https://api.github.com/repos/remapgie/FiraCode/releases', data=data.encode('utf-8'), headers=headers)).read()
  upload_url = re.match('https://.*/assets', json.loads(resp.decode('utf-8'))['upload_url']).group(0)

  print('github_release: Uploading', zip, 'to', upload_url)
  headers['Content-Type'] = 'application/zip'
  headers['Content-Length'] = os.path.getsize(zip)
  with open(zip, 'rb') as data:
    urllib.request.urlopen(urllib.request.Request(upload_url + '?name=' + zip, data=data, headers=headers))

if __name__ == '__main__':
  os.chdir(common.root)
  version = common.version()
  package(version)
  github_release(version)
  sys.exit(0)
