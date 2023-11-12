SAML2_AUTH = {
    # Metadata is required, choose either remote url or local file path
    # In Azure/Entra, find this in the Enterprise Application / Single sign-on / SAML Certificates / Token signing certificate / App Federation Metadata Url
    'METADATA_AUTO_CONF_URL': 'app_federation_metadata_url',

    # Optional settings below
    'DEFAULT_NEXT_URL': '/',  # Custom target redirect URL after the user get logged in. Default to /admin if not set. This setting will be overwritten if you have parameter ?next= specificed in the login URL.
    'CREATE_USER': 'TRUE', # Create a new Django user when a new user logs in. Defaults to True.
    'NEW_USER_PROFILE': {
        'USER_GROUPS': [],  # The default group name when a new user logs in
        'ACTIVE_STATUS': True,  # The default active status for new users
        'STAFF_STATUS': False,  # The staff status for new users
        'SUPERUSER_STATUS': False,  # The superuser status for new users
    },
    'ATTRIBUTES_MAP': {  # Change Email/UserName/FirstName/LastName to corresponding SAML2 userprofile attributes.
        'email': 'emailAddress',
        'username': 'username',
        'first_name': 'givenName',
        'last_name': 'surname',
    },
    'ASSERTION_URL': 'http://localhost:8000', # Custom URL to validate incoming SAML requests against
    'ENTITY_ID': 'http://localhost:8000/saml2_auth/acs/', # Populates the Issuer element in authn request
}
# Need to swap to https to satisfy Entra SAML requirements for SP-initiated SAML.
