# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, make_response, redirect, session
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic

from config import CONFIG

app = Flask(__name__)
app.config.from_object('patw.default_settings')

# Instantiate Authomatic.
authomatic = Authomatic(CONFIG, 'patw!@#$%^', session = session, report_errors=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/<provider_name>/', methods=['GET', 'POST'])
def login(provider_name):
    response = make_response()
    try:
        result = authomatic.login(WerkzeugAdapter(request, response), provider_name)
    except:
        return redirect("/")

    if result:
        if result.user:
            result.user.update()

            if result.user.credentials:
                if result.provider.name == 'fb':
                  url = 'https://graph.facebook.com/v2.0/me/friends'
                  response = result.provider.access(url)
                  if response.status == 200:
                      friends = response.data.get("data", {})


                if result.provider.name == 'tw':
                   url = 'https://api.twitter.com/1.1/friends/list.json'
                   response = result.provider.access(url)
                   if response.status == 200:
                        friends = response.data.get("users", {})


                if result.provider.name == 'google':
                    start = 1
                    data = None
                    friends = []

                    while start == 1 or 'entry' in data['feed']:
                        url = 'https://www.google.com/m8/feeds/contacts/default/full?alt=json&max-results=50&start-index=%s'
                        response = result.provider.access(url % start)
                        if response.status == 200:

                            data = response.data
                            contacts = response.data.get('feed', {}).get('entry', [])
                            error = response.data.get('error', {})

                            if error:
                                print u'Damn that error: {}!'.format(error)
                            elif contacts:
                                for contact in contacts:

                                    if u'gd$phoneNumber' in contact:
                                        name = contact.get('title', {'$t': ''}).get('$t', '')
                                        email = contact.get('gd$email', [{'address': ''}])[0].get('address', '')
                                        phone = contact.get('gd$phoneNumber', [{'$t': ''}])[0].get('$t', '')
                                        friends.append({'name': name, 'email': email, 'phone': phone})

                        else:
                            print 'error!'
                            print u'Status: {}'.format(response.status)

                        start += 50

        return render_template("welcome.html", user = result.user, friends = friends)

    return response
