#! /usr/bin/python
# -*- coding: utf-8 -*-
import requests
from flask import g, current_app as app, session
import psycopg2
import logging
import dateutil.parser
from math import sin, cos, asin, sqrt, radians

logging.getLogger().setLevel(logging.DEBUG)


def addLocation( location ):
    loc_in_sql = '''INSERT INTO locations (fb_id, name, city, country, position) VALUES ( %s, %s,
        %s, %s, POINT(%s,%s))'''
    loc_get_sql = '''SELECT TRUE FROM locations WHERE fb_id = %s'''
    if not query(loc_get_sql, ( location['id'], ), fetch_one = True):
        #location doesn't exist in the database, add it.
        qargs = ( location['id'], location['name'],location['location'].get('city'),
        location['location'].get('country'),
        location['location']['longitude'],location['location']['latitude'])
        query(loc_in_sql, qargs)


def hometownLocation(inputs, fb_token = None):
    dig_deeper = ('hometown', 'location')
    outputs = []
    for key in dig_deeper:
        if key in inputs:
            outputs.append(scrapeFacebook(fb_token if fb_token else g.fb_token,
                    inputs[key]['id'], ['name','location']))
    logging.debug( '*'*80+'\n{}\n'.format(outputs)+'*'*80 )
    return outputs

#Mutha fuckin' maths!
def distanceBetweenTwoPoints( point1, point2 ):
    R = 6378137 #earth's MEAN radius in meters
    #because psycopg2 is giving points as string...
    point1 = point1.strip('(').strip(')').split(',')
    point2 = point2.strip('(').strip(')').split(',')
    lon1, lat1, lon2, lat2 = map(radians,[ float(point1[0]), float(point1[1]),
            float(point2[0]), float(point2[1]) ])
    #BEGIN THE MATHS
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return c * R


def updateHometownLocation( results, locations ):
    success = 0
    dig_deeper = ('hometown', 'location')
    loc_in_sql = '''INSERT INTO locations (fb_id, name, city, country, position) VALUES ( %s, %s,
        %s, %s, POINT(%s,%s))'''
    loc_get_sql = '''SELECT TRUE FROM locations WHERE fb_id = %s'''
    mem_loc_in_sql = '''INSERT INTO member_locations ( member_id, location_id,
        visit_date ) VALUES ( %%s, %%s, %s);'''
    if not results or not isinstance(results, dict) or not { x : y for x, y in
            results.iteritems() if x in dig_deeper }:
        return False
    for location in locations:
        qry, args = None, None
        if location['id'] == results.get(dig_deeper[0],{}).get('id'):
            #it's our hometown.
            qry = mem_loc_in_sql % "'-infinity'::TIMESTAMPTZ"
            args = ( session['id'], location['id'])
        if location['id'] == results.get(dig_deeper[1],{}).get('id'):
            #it's there current_location
            qry = mem_loc_in_sql % "'infinity'::timestamptz"
            args = ( session['id'], location['id'] )
        addLocation( location )
        #do the actual member_location insert
        success += query( qry, args ).rowcount
    return success > 0


def getFacebookAccess():
    url='https://graph.facebook.com/oauth/access_token?client_id={0}&client_secret={1}&grant_type=client_credentials'
    url = url.format(app.config['FACEBOOK_APPID'], app.config['FACEBOOK_APPSECRET'])
    resp = requests.get(url)
    if resp.text:
        access_token = resp.text.split('=')[1]
        return access_token
    return ''


"""
fields : first_name, id, hometown, location, timezone
tagged_places
"""
def scrapeFacebook(app_token, fb_id = None, fields = []):
    fv = ''
    for field in fields:
        if fields.index(field) != 0:
            fv += '%2C'
        fv += field
    url = 'https://graph.facebook.com/v2.5/{}?'.format(fb_id if fb_id else 'me?')
    resp = requests.get(url + "fields=%s&debug=all&access_token=%s" % (fv, str(app_token)))
    s = resp.json()
    logging.debug( s )
    return s


def nextFacebook( url ):
    resp = requests.get( url )
    s = resp.json()
    logging.debug( s )
    return s


def getMember(id):
    qry = '''SELECT *,
to_char(departure, 'DD ')||trim(to_char(departure,'Month'))|| to_char(departure,', YYYY') as startdate,
to_char(departure, 'HH24:MI') as starttime FROM member WHERE id = %s'''
    return query( qry, ( id,), True)


def updateMember( vals, id = None ):
    qry ='''UPDATE MEMBER SET ( %s ) = ( %s ) WHERE id = %%s'''
    qargs = ()
    for key, val in vals.iteritems():
        qargs += ( val, )
    qargs += ( session['id'] if id is None else id, )
    qry = qry % ( ','.join(vals.keys()), ','.join([ '%s' for k in vals.keys() ]) )
    return query( qry, qargs )


def query( qry, args = None, fetch_row = False, fetch_one = False ):
    if not g.conn or g.conn.closed:
        g.conn = psycopg2(app.config['DB_CONN'],
                cursor_factory = psycopg2.extras.DictCursor)
        g.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = g.conn.cursor()
    logging.debug( cursor.mogrify(qry, args ) )
    cursor.execute( qry, args )
    if fetch_row or fetch_one:
        r = cursor.fetchone()
        return r if fetch_row else (r[0] if r and len(r) > 0 else None)
    return cursor

