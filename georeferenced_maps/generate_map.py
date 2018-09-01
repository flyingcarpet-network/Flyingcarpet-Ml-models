import glob
import json
import requests
import sys
import time

res = requests.post('http://localhost:8000/api/token-auth/',
                    data={'username': 'admin',
                          'password': 'password'}).json()
token = res['token']

res = requests.post('http://localhost:8000/api/projects/',
                    headers={'Authorization': 'JWT {}'.format(token)},
                    data={'name': 'Goat Rock Beach - Sonoma, CA'}).json()

project_id = res['id']

images = map(
    lambda image: ('images', (image.split(
        '/')[-1], open(image, 'rb'), 'image/jpg')),
    glob.glob('./datasets/goat_rock_beach/*.jpg'))

options = json.dumps([
    {'name': "fast-orthophoto", 'value': "true"},
    {'name': "resize-to", 'value': "2048"}
])


res = requests.post('http://localhost:8000/api/projects/{}/tasks/'.format(project_id),
                    headers={'Authorization': 'JWT {}'.format(token)},
                    files=images, data={'options': options}).json()

task_id = res['id']

while True:
    res = requests.get('http://localhost:8000/api/projects/{}/tasks/{}/'.format(project_id, task_id),
                       headers={'Authorization': 'JWT {}'.format(token)}).json()

    if res['status'] == 40:
        print("Task has completed!")
        break
    elif res['status'] == 30:
        print("Task failed: {}".format(res))
        sys.exit(1)
    else:
        print("Processing, hold on...")
        time.sleep(30)

res = requests.get("http://localhost:8000/api/projects/{}/tasks/{}/download/orthophoto.tif".format(project_id, task_id),
                   headers={'Authorization': 'JWT {}'.format(token)},
                   stream=True)

with open("output/orthophoto.tif", 'wb') as f:
    for chunk in res.iter_content(chunk_size=1024):
        if chunk:
            f.write(chunk)

print("Saved ./output/orthophoto.tif")
