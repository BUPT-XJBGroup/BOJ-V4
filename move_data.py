import os
import sys

import requests


if __name__ == '__main__':
    sess = requests.session()
    data = {
        'username': 'root',
        'password': '123456',
    }
    multiple_files = [
        ('file', ('submission.json', open('submission.json', 'r'), 'txt')),   # could only upload one file once
    ]
    resp = sess.post('http://localhost:8000/accounts/login/', data=data)
    rep = sess.post('http://localhost:8000/problem/2/files/', files=multiple_files)
    print resp
    print "========="
    print rep

