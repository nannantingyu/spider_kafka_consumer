# -*- coding: utf-8 -*-
import redis, os, contextlib, urllib2

from Controller import Controller
import json, requests, re, logging

logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='logs/jin10_calendar.log',
                filemode='w')

class FiledownController(Controller):
    def __init__(self, topic="downfile_queue"):
        super(FiledownController, self).__init__(topic)
        # self.post_sn_url = 'http://www.9dfx.com/api/content'

    def run(self):
        for message in self.consumer:
            if message is not None:
                file = message.value
                if file is None:
                    print "no more file to download"
                    continue

                fileinfo = file.split('_____')
                file_url = fileinfo[0]
                file_save_path = fileinfo[1]

                save_dir = os.path.dirname(file_save_path)
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)

                try:
                    with contextlib.closing(urllib2.urlopen(file_url)) as fimg:
                        with open(file_save_path, 'wb') as bfile:
                            bfile.write(fimg.read())
                except Exception, e:
                    with open("file_down_error.log", "a") as fs:
                        fs.write(file)
