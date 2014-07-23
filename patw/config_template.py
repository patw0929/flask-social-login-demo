from authomatic.providers import oauth2, oauth1

CONFIG = {

    'tw': { # Your internal provider name

        # Provider class
        'class_': oauth1.Twitter,

        # Twitter is an AuthorizationProvider so we need to set several other properties too:
        'consumer_key': '########################',
        'consumer_secret': '######################################',
    },

    'fb': {

        'class_': oauth2.Facebook,

        'consumer_key': '##############',
        'consumer_secret': '########################',

        # But it is also an OAuth 2.0 provider and it needs scope.
        'scope': ['user_friends', 'email'],
    },

    'google': {
         'class_': 'authomatic.providers.oauth2.Google', # Can be a fully qualified string path.

         # Provider type specific keyword arguments:
         'short_name': 2, # use authomatic.short_name() to generate this automatically
         'consumer_key': '#################################################################',
         'consumer_secret': '#####################',
         'scope': ['https://www.googleapis.com/auth/plus.login',
                   'https://www.googleapis.com/auth/plus.profile.emails.read',
                   'https://www.google.com/m8/feeds/']
    }
}
