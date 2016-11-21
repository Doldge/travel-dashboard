#! /usr/bin/python
# -*- coding: utf-8 -*-
from flask import current_app as app, Blueprint, json, render_template
from flask import redirect, abort, url_for, g, session, request, flash
from functions import *

import datetime
from pytz import timezone

myAccount = Blueprint('myAccount', __name__, template_folder='templates')

@myAccount.route('/')
def _index():
    if 'id' not in session:
        return redirect(url_for('_login'))
    r = getMember( session['id'] )
    sql = '''SELECT *, position[1] as lat, position[0] as long FROM member_locations LEFT JOIN locations ON (
    member_locations.location_id = locations.fb_id ) WHERE member_id = %s ORDER
    BY visit_date DESC;'''
    cur = query( sql, ( session['id'], ))
    locations = []
    for location in cur.fetchall():
        if location['visit_date'].tzinfo is None:
            location['visit_date'] = location['visit_date'].replace(tzinfo=timezone('UTC'))
        if location['visit_date'] > datetime.datetime.now(timezone('UTC')):
            location['visit_date'] = 'Current Location'
        elif location['visit_date'] < r['departure']:
            location['visit_date'] = 'Hometown'
        locations.append( location )
    return render_template( 'control_panel.html', row = r, display = 'none',
    nav_text_colour = 'black-text', title = 'My Account', locations = locations)


@myAccount.route('/locations/<id>/', methods = ['GET'], endpoint = '_locations_id')
@myAccount.route('/locations/', methods = ['GET'])
def _locations( id = None):
    if id is not None:
        m = getMember( id )
        if not m or not m['ispublic']:
            abort(404)
    elif 'id' not in session:
        abort(404)
    else:
        id = session['id']
    sql = '''SELECT *, position[1] as lat, position[0] as lng FROM member_locations LEFT JOIN locations ON (
    member_locations.location_id = locations.fb_id ) WHERE member_id = %s ORDER
    BY visit_date DESC;'''
    cur = query( sql, ( id, ))
    locs = [ x.copy() for x in cur.fetchall() ]
    return json.jsonify({ 'locations' : locs })


@myAccount.route('/locations/table/<id>/', methods = ['GET'], endpoint =
'_locationsTable_id')
@myAccount.route('/locations/table/', methods = ['GET'])
def _locationsTable( id = None):
    if id is not None:
        m = getMember( id )
        if not m or not m['ispublic']:
            abort(404)
    elif 'id' not in session:
        abort(404)
    else:
        id = session['id']
    m = getMember(id)
    sql = '''SELECT name as "Location", country as "Country", visit_date as "Visit Date" FROM member_locations LEFT JOIN locations ON (
    member_locations.location_id = locations.fb_id ) WHERE member_id = %s ORDER
    BY visit_date DESC;'''
    cur = query( sql, ( id, ))
    locations = []
    for location in cur.fetchall():
        if location['Visit Date'].tzinfo is None:
            location['Visit Date'] = location['Visit Date'].replace(tzinfo=timezone('UTC'))
        if location['Visit Date'] > datetime.datetime.now(timezone('UTC')):
            location['Visit Date'] = 'Current Location'
        elif location['Visit Date'] < m['departure']:
            location['Visit Date'] = 'Hometown'
        locations.append( location )
    locs = [ x.copy().values() for x in locations ]
    headers = locations[0].keys()
    return json.jsonify({ 'rows' : locs, 'headers' : headers })

@myAccount.route('/timesincedeparture/<id>/', methods = ['GET'], endpoint =
'_timeSinceDeparture_id')
@myAccount.route('/timesincedeparture/', methods = ['GET'])
def _timeSinceDeparture( id = None ):
    m = None
    departure = None
    if id is not None:
        m = getMember( id )
        if not m or not m['ispublic']:
            abort(404)
    elif 'id' not in session:
        abort(404)
    else:
        id = session['id']
        m = getMember( id )
    if m['departure']:
        if m['current_tz'].isdigit():
            m['current_tz'] = 'GMT+'+m['current_tz'] if\
                    m['current_tz'] > 0 else 'GMT-'+m['current_tz']
        epoch = datetime.datetime.utcfromtimestamp(0).replace(tzinfo =\
        timezone(m['current_tz']))
        departure = ( m['departure'] - epoch ).total_seconds()
    return json.jsonify({ 'startDate' : departure })


@myAccount.route('/distancefromhome/<id>/', methods = ['GET'], endpoint =
'_distanceFromHome_id')
@myAccount.route('/distancefromhome/', methods = ['GET'])
def _distanceFromHome( id = None ):
    if id is not None:
        m = getMember( id )
        if not m or not m['ispublic']:
            abort(404)
    elif 'id' not in session:
        abort(404)
    else:
        id = session['id']
    sql = '''SELECT * FROM member_locations LEFT JOIN locations ON (
    member_locations.location_id = locations.fb_id ) WHERE member_id = %s AND
    ( visit_date = 'infinity' or visit_date = '-infinity') ORDER BY
    visit_date DESC;'''
    cur = query( sql, (id,))
    locs = cur.fetchall()
    pos1 = locs[0]['position']
    pos2 = locs[1]['position']
    distance = distanceBetweenTwoPoints(pos1, pos2)
    logging.debug('********\nDISTANCE: {}\n***********'.format(distance))
    return json.jsonify({ 'distance' : distance})


@myAccount.route('/totaldistance/<id>/', methods = ['GET'], endpoint =
'_totalDistance_id')
@myAccount.route('/totaldistance/', methods = ['GET'])
def _totalDistance( id = None):
    if id is not None:
        m = getMember( id )
        if not m or not m['ispublic']:
            abort(404)
    elif 'id' not in session:
        abort(404)
    else:
        id = session['id']
    sql = '''SELECT * FROM member_locations LEFT JOIN locations ON (
        member_locations.location_id = locations.fb_id ) WHERE member_id = %s
        ORDER BY visit_date ASC'''
    cur = query( sql, ( id,))
    locs = cur.fetchall()
    distance = 0
    loc_0, loc_1 = None, None
    for loc in locs:
        loc_0 = loc_1
        loc_1 = loc['position']
        if loc_0 and loc_1:
            distance += distanceBetweenTwoPoints( loc_0, loc_1 )
    logging.debug('********\nTOTAL DISTANCE: {}\n***********'.format(distance))
    return json.jsonify({ 'distance' : distance })


@myAccount.route('/friends/<id>/', methods = ['GET'], endpoint = '_friends_id')
@myAccount.route('/friends/', methods = ['GET'])
def _friends( id = None):
    m = None
    if id is not None:
        m = getMember( id )
        if not m or not m['ispublic']:
            abort(404)
    elif 'id' not in session:
        abort(404)
    else:
        id = session['id']
        m = getMember( id )
    sql = '''SELECT current_value - start_value as cnt FROM friends WHERE
    fb_id = %s'''
    count = query(sql, (m['fb_id'], ), fetch_one = True )
    return json.jsonify({'friends' : count or 0, 'name' : m['firstname']})


@myAccount.route('/countrycount/<id>/', methods = ['GET'], defaults = {'id' : None})
def _countryCount(id = None):
    if id is not None:
        m = getMember( id )
        if not m or not m['ispublic']:
            abort(404)
    elif 'id' not in session:
        abort(404)
    else:
        id = session['id']
    sql = '''select count(DISTINCT country) FROM member_locations LEFT JOIN
    locations ON (member_locations.location_id = locations.fb_id) WHERE (country
    is not null OR name not IN (SELECT country FROM member_locations LEFT JOIN
    locations ON (member_locations.location_id = locations.fb_id) WHERE
    member_id = %s)) and member_id = %s'''
    res = query( sql, ( id, id, ), fetch_one = True)
    return json.jsonify({ 'countryCount' : res })


@myAccount.route('/scrapeFacebook/', methods = ['GET','POST'])
def _myFacebook():
    member = getMember(session['id'])
    if not member['departure']:
        flash('You must set your departure date first.')
        if 'frontend' in request.values:
            return redirect(url_for('._index'))
        return json.jsonify({})
    fields = ['first_name','last_name', 'id', 'hometown', 'location', 'timezone']
    qry = '''SELECT access_token FROM facebook WHERE id = (SELECT fb_id FROM
    member WHERE id = %s) AND (created +
    to_char(expires_in,'9999999999')::INTERVAL) < now()'''
    r = query( qry, args = ( session['id'], ), fetch_row = True )
    token = None
    fb_id = None
    if r:
        token = r[0]
    if 'token' in request.values:
        token = request.values['token']
        if '!' in token:
            token = token.split('!')
            fb_id = token[1]
            fb_expires = token[2]
            fb_signedrequest = token[3]
            token = token[0]
            if query('SELECT TRUE from facebook WHERE id = %s',(fb_id,),
                    fetch_row = True ):
                fbqry = '''UPDATE facebook SET ( access_token, expires_in,
                created, signed_request ) = ( %s, %s, now(), %s )
                WHERE id = %s'''
            else:
                fbqry = '''INSERT INTO facebook ( access_token,
                expires_in, signed_request, id ) VALUES ( %s, %s, %s, %s)'''
            query( fbqry, ( token, fb_expires, fb_signedrequest, fb_id ) )

    if not fb_id:
        fb_id = query('SELECT fb_id FROM member WHERE id = %s', ( session['id'],),
            fetch_one = True)

    fb_response = scrapeFacebook( token if token is not None else g.fb_token, fb_id, fields )
    locations = hometownLocation( fb_response, token )
    updateHometownLocation(fb_response, locations)
    update = {}
    update['firstname'] = fb_response['first_name']
    update['surname'] = fb_response['last_name']
    update['current_tz'] = fb_response.get('timezone')
    updateMember( update )

    fields = ['tagged_places']
    res = scrapeFacebook( token if token is not None else g.fb_token, fb_id, fields )
    res = res['tagged_places']
    locations = res['data']
    while res['paging'].get('next'):
        res = nextFacebook( res['paging']['next'] )
        locations += res['data']
    logging.debug( locations )
    qry = '''INSERT INTO member_locations ( member_id, location_id, visit_date
    ) VALUES ( %s, %s, %s )'''
    for visit in locations:
        visit['created_time'] = dateutil.parser.parse(visit['created_time'])
        if visit['created_time'] >= member['departure']:
            addLocation(visit['place'])
            query( qry, ( session['id'], visit['place']['id'], visit['created_time']))

    if 'frontend' in request.values:
        return redirect( url_for('._index') )
    return json.jsonify({})


@myAccount.route('/update/', methods = ['POST'])
def _update():
    update = {}
    for key, val in request.values.iteritems():
        if key == 'start_date':
            update['startdate'] = val
        elif key == 'start_time':
            update['starttime'] = val
        else:
            update[key] = val

    logging.debug( update )
    update.pop('frontend', None)
    if 'startdate' in update:
        update['departure'] = datetime.datetime.strptime(update['startdate'],'%d %B, %Y')
        if 'starttime' in update:
            a = update['starttime'].split(':')
            a+= a[1].split(' ')
            logging.debug( '\nA:{}\n'.format(a) )
            if 'pm' in a[0].lower():
                a[0] = int(a[0])+12
            a.pop(1)
            update['departure'] = update['departure'].replace(hour = int(a[0]),
            minute = int(a[1]))
        m = getMember(session['id'])
        if 'current_tz' in update:
            update['departure'] = update['departure'].replace(tzinfo =
            timezone(update['current_tz']))
        elif m['current_tz']:
            if m['current_tz'].isdigit():
                m['current_tz'] = 'GMT+'+m['current_tz'] if m['current_tz'] > 0 else 'GMT-'+m['current_tz']
            update['departure'] = update['departure'].replace(tzinfo = timezone(m['current_tz']))
    keep = ( 'departure', 'firstname', 'surname', 'current_tz', 'url', 'email',
            'metric', 'ispublic', 'password' )
    for key in dict(update):
        if key not in keep:
            update.pop(key)
    updateMember( update, session['id'] )
    flash('Updated!')
    return redirect( url_for('._index') )

