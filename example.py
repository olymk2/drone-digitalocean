#!/usr/bin/pythonclean_name(row.get('name'))
import os
import sys
import requests


DIGITALOCEAN_TOKEN = os.environ.get('TOKEN')
DIGITALOCEAN_URL = 'https://api.digitalocean.com/v2/'
DIGITALOCEAN_DROPLETS_URL = '%sdroplets/' % DIGITALOCEAN_URL

MODE = 'LAUNCH'

DO_NAME = os.environ.get("DO_NAME", "ubuntu-16-04-x64")
DO_REGION = os.environ.get("DO_REGION", "LON1")
DO_MEM = os.environ.get("DO_MEM", "1gb")
DO_IMAGE = os.environ.get("DO_IMAGE", "ubuntu-16-04-x64")
DO_SSHKEYS = os.environ.get("DO_SSH", None)
DO_TAGS = os.environ.get("DO_TAGS", '').split(',')

headers ={
    'Authorization': 'Bearer %s' % DIGITALOCEAN_TOKEN,
    'Content-Type': 'application/json'
}

# sanity checks
if DIGITALOCEAN_TOKEN is None:
    sys.exit('Panic no digitalocean TOKEN supplied')
if DO_NAME is None:
    sys.exit('Panic no name specified')
if DO_IMAGE is None:
    sys.exit('Panic no name specified')


data = {
    "name": DO_NAME,
    "region": DO_REGION,
    "size": DO_MEM,
    "image": DO_IMAGE,
    "tags": ["drone"],
    "ssh": []
}


#optional options
if DO_SSHKEYS:
    for ssh_key in DO_SSHKEYS:
        data["ssh"].append(ssh_key)
if DO_TAGS:
    for tag in DO_TAGS:
        data["tags"].append(tag)

# request = requests.post(DIGITALOCEAN_URL, headers=headers, json=data)
# print(request.content)





clean = {
    'tag_name': 'drone',
}

#Remove old droplets tagged with drone, that do not have the current hash
obsolete_droplets = []
request = requests.get(DIGITALOCEAN_DROPLETS_URL, headers=headers, params=clean)
print("Removing obsolete droplets")
for droplet in request.json()['droplets']:
    if 'drone' in droplet['tags']:
        print(droplet['name'])
        print(droplet['tags'])
        if 'drone' not in droplet['tags']:
            continue
        # if droplet == DRONE_COMMIT:
        #     continue
        print('Flagged to destroy %s - %s - %s' % (droplet['id'], droplet['name'], ', '.join(droplet['tags'])))
        obsolete_droplets.append(droplet['id'])


for droplet in obsolete_droplets:
    print('destroying %d' % (droplet))
    url = '%s%s' % (DIGITALOCEAN_DROPLETS_URL, droplet)
    request = requests.delete(url, headers=headers)
    if request.status_code == 204:
        print('Droplet successfully destroyed')
        continue

    sys.exit('Failed to delete droplet %d bailing' % droplet)


