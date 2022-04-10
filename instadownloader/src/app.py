import glob
import calendar
import os
import time
import json
import datetime as dt
from datetime import datetime
from flask import Flask
from flask import request
import instaloader

app = Flask(__name__)

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
FILES_DIR = os.getenv('FILES_DIR', 'data')
WAIT_TIME = int(os.getenv('WAIT_TIME', 3))

L = instaloader.Instaloader(download_video_thumbnails=False, save_metadata=False, compress_json=False, download_comments=False, post_metadata_txt_pattern='', max_connection_attempts=1, dirname_pattern=FILES_DIR + '/{target}')

def updateTargetTime(target):
    filename = FILES_DIR + '/followee.json'
    data = {}
    if os.path.isfile(filename):
        file = open(filename, 'r')
        data = json.load(file)
        file.close()
    else:
        file = open(filename, 'x')
        file.close()
    data[target] = calendar.timegm(time.gmtime())

    file = open(filename, 'w')
    file.write(json.dumps(data))
    file.close()

@app.route('/login')
def login():
    try:
        L.load_session_from_file(USERNAME)
        return 'SUCCESS'
    except Exception as e1:
        print('e1', str(e1))
        try:
            L.login(USERNAME, PASSWORD)
            L.save_session_to_file()
            return 'SUCCESS'
        except Exception as e2:
            print('e2', str(e2))
            return str(e2)

@app.route('/download')
def download():
    target = request.args.get('target')
    print('[INFO] fetching target<{target}>'.format(target = target))
    fileList = glob.glob(FILES_DIR + '/' + target + '/*.*')
    fileList.sort()
    earliestDate = None
    latestDate = None
    if len(fileList) > 0:
        earliestDateStr = fileList[0].split('/')[-1]
        earliestDate = datetime(int(earliestDateStr[0:4]), int(earliestDateStr[5:7]), int(earliestDateStr[8:10]))
        earliestDate += dt.timedelta(days = 1)
        latestDateStr = fileList[-1].split('/')[-1]
        latestDate = datetime(int(latestDateStr[0:4]), int(latestDateStr[5:7]), int(latestDateStr[8:10]))
    try:
        profile = instaloader.Profile.from_username(L.context, target)
        posts = instaloader.Profile.get_posts(profile)
        for post in posts:
            if (earliestDate and (post.date_utc < earliestDate)) or (latestDate and (post.date_utc > latestDate)) or ((not earliestDate) and (not latestDate)):
                L.download_post(post, target)
                time.sleep(3)
        updateTargetTime(target)
        return 'SUCCESS'
    except Exception as e:
        print(str(e))
        return str(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
