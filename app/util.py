'''
CS 145 NetRank
Shubhi Jain and Ricky Galliani
This is a library of functions for the app
'''
import subprocess
import json
import os
import boto
import csv
import urllib2

from uuid import uuid4
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    '''
    This function checks whether the file is the proper filetype.
    '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def s3_upload(source_file, upload_dir='data/', acl='public-read'):
    ''' Uploads WTForm File Object to Amazon S3
        Expects following app.config attributes to be set:
            AWS_ACCESS_KEY      :   S3 API Key
            AWS_SECRET_KEY      :   S3 Secret Key
            S3_BUCKET           :   What bucket to upload to
            S3_UPLOAD_DIRECTORY :   Which S3 Directory.
        The default sets the access rights on the uploaded file to
        public-read.  It also generates a unique filename via
        the uuid4 function combined with the file extension from
        the source file.pi
        https://github.com/doobeh/Flask-S3-Uploader/blob/master/tools.py
    '''

    source_filename = secure_filename(source_file.filename)
    source_extension = os.path.splitext(source_filename)[1]

    destination_filename = uuid4().hex + source_extension

    # Connect to S3 and upload file.
    conn = boto.connect_s3(os.environ['AWS_ACCESS_KEY'], os.environ['AWS_SECRET_KEY'])
    b = conn.get_bucket(os.environ['S3_BUCKET'])

    sml = b.new_key('/'.join([upload_dir, destination_filename]))
    sml.set_contents_from_string(source_file.read())
    sml.set_acl(acl)

    return destination_filename

def s3_access(source_file, download_dir='rankings/'):
    '''
    Accesses Rankings file from S3 and returns a list of lists
    '''
    if source_file:
        # Connect to S3
        conn = boto.connect_s3(os.environ['AWS_ACCESS_KEY'], os.environ['AWS_SECRET_KEY'])
        b = conn.get_bucket(os.environ['S3_BUCKET'])

        # Get source file
        key = b.get_key(download_dir + source_file)
        key_url = key.generate_url(3600, query_auth=True, force_http=True)

        # read csv and return it
        response = urllib2.urlopen(key_url)
        cr = csv.reader(response)
        return list(cr)
    return None

def get_rankings_as_dicts(rankings):
    '''
    Takes in a list of rankings and returns them as a list of dicts
    with the key as the team name and the value as the rank.
    '''
    midway = {}
    for rank, team in rankings[0]:
        midway[team] = {'rank': rank, 'ranks': [rank]}
    for ranking in rankings[1:]:
        for rank, team in ranking:
            ranks = midway[team]['ranks']
            ranks.append(rank)
            midway[team]['ranks'] = ranks[:]
    result = []
    for team, dic in midway.iteritems():
        result.append({'text': team, 'ranks': dic['ranks'], 'rank': dic['rank']})
    return result
