#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, redirect, render_template, request, jsonify
from flask import send_from_directory
from random import seed, randint
from datetime import datetime, date
from sqlalchemy.dialects.postgresql import JSON
from flask_heroku import Heroku
import config

import os
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

application = Flask(__name__)
app = application

# app.config.from_object(os.environ['APP_SETTINGS'])

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgres://vfjglauvifljcv:574bf440fa22be02088c0cacd71e2bfe3f8c560f8aa3d06f6097afdd0d9db3dc@ec2-54-165-36-134.compute-1.amazonaws.com:5432/dfa196a8t1murm'

db = SQLAlchemy(app)
heroku = Heroku(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class URLMap(db.Model):

    __tablename__ = 'url_map'

    short_url = db.Column(db.String(50), primary_key=True)
    long_url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime())
    expiry = db.Column(db.Integer())
    visit_count = db.Column(db.Integer())

    def __init__(
        self,
        short_url,
        long_url,
        created_at,
        expiry,
        visit_count,
        ):

        self.short_url = short_url
        self.long_url = long_url
        self.created_at = created_at
        self.expiry = expiry
        self.visit_count = visit_count

    def __repr__(self):
        return '<short_url {}>'.format(self.short_url)

    def serialize(self):
        return {
            'short_url': self.short_url,
            'long_url': self.long_url,
            'created_at': self.created_at,
            'expiry': self.expiry,
            'visit_count': self.visit_count,
            }


# db.init_app(app)

@app.route('/<short_url>')
def redirect_to_url(short_url):
    link = URLMap.query.filter_by(short_url=short_url).first_or_404()

    link.visit_count = link.visit_count + 1
    db.session.commit()
    s = link.long_url
    if s is not None:
        if s.find('http://') != 0 and s.find('https://') != 0:
            s = 'http://' + s
    return redirect(s)

    return redirect('https://' + link.long_url)


@app.route('/')
def home():

    return render_template('index.html')


@app.route('/add', methods=['GET'])
def add():

    print("entered")
    long_url = request.args.get('long_url')
    print('long_url ' + long_url)
    
    
    seedval = randint(100, 999)
    seed(seedval)
    num = randint(100000000000, 999999999999)
    #print seed
    print (num)
    s = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    hash_str = ''
    while num >= 1:
        index = num % 62
        print (int(index))
        hash_str = s[int(index)] + hash_str
        num = num / 62
    
    key = URLMap.query.filter_by(short_url=hash_str).first()

    while key is not None:
        hash_str = ''
        seedval = randint(100, 999)
        seed(seedval)
        num = randint(100000000000, 999999999999)
        #print seed
        print (num)

        while num >= 1:
            index = num % 62
            print (int(index))
            hash_str = s[int(index)] + hash_str
            num = num / 62
        key = URLMap.query.filter_by(short_url=hash_str).first()


    if request.method == 'GET':
        pf = URLMap(hash_str, long_url, datetime.now(),
                    int(date.today().year) + 3, 0)
        db.session.add(pf)
        db.session.commit()
    return jsonify({'hash_str': hash_str})

        # return redirect(url_for('view_posts'))
    # return render_template('post_form.html', postform=postform)
    # return "<a href = http://0.0.0.0:5000/" + hash_str +">http://0.0.0.0.:5000/" + hash_str + "</a>"

    


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static',
                               'images'), 'favicon.ico',
                               mimetype='image/png')


@app.errorhandler(404)
def page_not_found(e):
    return (render_template('404.html'), 404)

if __name__ == '__main__':
    manager.run()
