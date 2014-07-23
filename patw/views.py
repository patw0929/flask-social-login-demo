# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, make_response, redirect, session
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic

from config import CONFIG

app = Flask(__name__)
app.config.from_object('patw.default_settings')

# Instantiate Authomatic.
authomatic = Authomatic(CONFIG, 'patw!@#$%^', report_errors=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/<provider_name>/', methods=['GET', 'POST'])
def login(provider_name):
    response = make_response()
    result = authomatic.login(WerkzeugAdapter(request, response), provider_name)

    session["user"] = ""
    session["friends"] = ""

    if result:
        if result.user:
            result.user.update()

            session["user"] = { "name": result.user.name, "id": result.user.id, "email": result.user.email }

            if result.user.credentials:
                if result.provider.name == 'fb':
                  url = 'https://graph.facebook.com/v2.0/me/friends'
                  response = result.provider.access(url)
                  if response.status == 200:
                      print "ok"
                      friends = response.data.get("data", {})

                      session["friends"] = friends


                if result.provider.name == 'tw':
                   url = 'https://api.twitter.com/1.1/friends/list.json'
                   response = result.provider.access(url)
                   if response.status == 200:
                        friends = response.data.get("users", {})

                        session["friends"] = friends

                        if friends:
                            for friend in friends:
                                print friend.get("name", {}) #profile_image_url


                if result.provider.name == 'google':
                    url = 'https://www.google.com/m8/feeds/contacts/default/full?alt=json'
                    response = result.provider.access(url)
                    if response.status == 200:

                        contacts = response.data.get('feed', {}).get('entry', [])
                        error = response.data.get('error', {})

                        if error:
                            print u'Damn that error: {}!'.format(error)
                        elif contacts:
                            friends = []
                            for contact in contacts:

                                name = contact.get('title', {}).get('$t', '')
                                email = contact.get('gd$email', {})[0].get('address', '')

                                if name != '':
                                    friends.append({'name': name, 'email': email})

                            session["friends"] = friends
                            print friends

                    else:
                        print 'error!'
                        print u'Status: {}'.format(response.status)

        return redirect("welcome")

    return response

@app.route("/welcome")
def welcome():
    user = session["user"]
    friends = session["friends"]

    return render_template("welcome.html", user = user, friends = friends)
