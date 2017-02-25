Facebook Event Info Emailer
==============
Simple Python command line script for checking Facebook page event participants.

Requirements
------------
`dateutil <https://pypi.python.org/pypi/python-dateutil>`_,
`facepy <https://pypi.python.org/pypi/facepy>`_,
`requests <https://pypi.python.org/pypi/requests>`_ (required by facepy)

Obtaining access tokens
-----------------------
*Only user token allows to post events on behalf of the user*

App token:

1. Go to: https://developers.facebook.com/apps
2. Click: "Create New App"
3. Provide an app name, then click "Continue"
4. Token is available at: https://developers.facebook.com/tools/access_token/

Extended user token (complete above before proceeding):

1. Go to: https://developers.facebook.com/tools/explorer
2. Select your application and click: "Get Access Token"
3. Check: "user_events" (in "User Data Permissions") and "create_event" (in "Extended Permissions")
4. Click: "Get Access Token"

This is short-lived token (which expires in about 2 hours).
To extend it (to about 2 months) you need facebook-extend-access-token.py script together with the
just generated short-lived token, app id and app secret (https://developers.facebook.com/apps):

.. code-block:: bash

    $ ./facebook-extend-access-token.py --appid 'App ID' --appsecret 'App Secret' --token 'User Token'

For more details, please go to:
`<https://developers.facebook.com/docs/facebook-login/access-tokens>`

Command examples
----------------
*All examples assume you have already setup your access token in config.json!*

.. code-block:: bash

    $ ./facebook-event.py -h --id 331218348435 --email test@gmail.com --password testPassword
