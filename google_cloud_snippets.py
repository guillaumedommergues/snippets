# Notes for myself on how to use the Google Cloud for web applications
# All this can be found on the Google Cloud documentation. This aims to be a collection of the most necessary and useful snippets 
# Links are provided for more information

########################
# app.yaml file
########################

# This file specifies how the app will run
# https://cloud.google.com/appengine/docs/standard/python/config/appref
# general info
runtime: python27
api_version: 1
threadsafe: yes

# explains where the app object resides
handlers:
- url: .*  # This regex directs all routes to main.app
  script: my_app.app #assuming that you are developing in Flask and the app = Flask(__name__) is in a .py file in the /myapp folder

# libraries that do not use 100% Python need to be imported here 
# list of available libraries here: https://cloud.google.com/appengine/docs/standard/python/tools/built-in-libraries-27
libraries:
- name: numpy
  version: "latest"
- name: MySQLdb
  version: "latest"

# this limits the use of resources so the app runs for free 
# more on quotas at https://cloud.google.com/appengine/quotas#Instances
instance_class: F1
automatic_scaling:
  min_idle_instances: 0
  max_idle_instances: 1  # default value
  min_pending_latency: 100ms  # default value
  max_pending_latency: 100ms
  max_concurrent_requests: 50


############################
# appengine_config.py file
############################

# pure python libraries do not need to be imported in the app.yaml file and usually cannot
# install them in a /lib folder and vedor them in the app with this appengine_config.py file
# https://cloud.google.com/appengine/docs/standard/python/tools/using-libraries-python-27
from google.appengine.ext import vendor
import os
import sys 
on_appengine = os.environ.get('SERVER_SOFTWARE','').startswith('Development')
if on_appengine and os.name == 'nt':
  sys.platform = "Not Windows"
vendor.add('lib')

############################
# using Google Storage
############################

# great to store files, pictures, videos, etc
# uploading files
from google.cloud import storage
def upload_file_to_Google_storage(file,filename,size):
  storage_client = storage.Client('my-project-name') #replace 'my-project-name' with your project name
  bucket = storage_client.get_bucket('my-bucket-name.appspot.com') #replace 'my-bucket-name.appspot.com' with your bucket name
  blob = bucket.blob(filename)
  blob.upload_from_file(file, size=size, content_type ='image/jpg', rewind =True) #replace 'image/jpg' with applicable content type
  blob.make_public() #only to make it publicly accessible
  return blob.public_url, blob.name #the url that can be used the access the file and the file name to delete it

# deleting files
def delete_file_to_Google_storage(blob_name):
  storage_client = storage.Client('my-project-name') #replace 'my-project-name' with your project name
  bucket = storage_client.get_bucket('my-bucket-name.appspot.com') #replace 'my-bucket-name.appspot.com' with your bucket name
  blob = bucket.blob(blob_name)
  blob.delete()

############################
# using the Google Datastore
############################

# great to store non-relational data - free for limited usage 
# data is stored in groups called "kinds"
# each object in the Datastore is called an "entity" and it is uniquely identified by a "key"
# each entity has several fields called "properties" that can be of virtually any type
# not a good choice for relational data - use the Cloud SQL instead

from google.cloud import datastore
from google.appengine.ext import ndb
# https://cloud.google.com/appengine/docs/standard/python/ndb/modelclass

# declaring the model for a specific kind
class marker_kind(ndb.Model):
  markerTitle = ndb.StringProperty()
  markerDescription = ndb.TextProperty()
  markerValue = ndb.FloatProperty()

# creating an entity 
p = marker_kind(markerTitle='my title',markerDescription='my description', markerValue=1)
p.put() 

# updating a value
p.markerDescription='new description'
p.put() 

# getting the key of an entity
k=p.key

# a key consists of a kind and an ID 
# can be useful to send a unique identifier as string from client to server for instance
my_id=p.key.id()
my_kind=p.key.kind()

# listing all entities in a kind
marker_list=marker_kind.query()

# querying a kind with some criteria (here the first 10 entities with the markerTitle 'my title')
my_markers=marker_kind.query(marker_kind.markerTitle =='my title').fetch(10)

# deleting an entity - if you know the key k
k.delete()


##################################
# linking an app to Google Cloud
##################################

# assuming a Flask App connected to a MySQL database in the backend
# create the database, the user name, the password on the console like so
# https://cloud.google.com/sql/docs/mysql/quickstart
# https://cloud.google.com/python/getting-started/using-cloud-sql

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import MySQLdb
app = Flask(__name__)

CLOUDSQL_USER = 'root'
CLOUDSQL_PASSWORD = 'your_password'
CLOUDSQL_DATABASE = 'your_database_name'
CLOUDSQL_CONNECTION_NAME = 'your_connection_name' # something like project-name:us-central1:database-name'
LIVE_SQLALCHEMY_DATABASE_URI = (
    'mysql://{user}:{password}@localhost/{database}'
    '?unix_socket=/cloudsql/{connection_name}').format(
        user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
        database=CLOUDSQL_DATABASE, connection_name=CLOUDSQL_CONNECTION_NAME)
app.config['SQLALCHEMY_DATABASE_URI'] = LIVE_SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)
