# A suite of integrations tests for the Tapis Python SDK.
# Build the test docker image: docker build -t tapis/pysdk-tests -f Dockerfile-tests .
# Run these tests using the built docker image: docker run -it --rm  tapis/pysdk-tests
import os
import time
import subprocess
import pytest
from tapipy.tapis import Tapis, TapisResult


BASE_URL = os.getenv("base_url", "https://tacc.develop.tapis.io")
USERNAME = os.environ["username"]
PASSWORD = os.environ["password"]


@pytest.fixture
def client():
    t = Tapis(base_url=BASE_URL,
              username=USERNAME,
              password=PASSWORD)
    t.get_tokens()
    return t

# -----------------------------------------------------
# Tests to check parsing of different result structures -
# -----------------------------------------------------
def test_tapisresult_list_simple():
    result = ['a',  1, 'b', True, None, 3.14159, b'some bytes']
    tr = TapisResult(result)
    r = tr.result
    assert len(r) == 7
    assert r[0] == 'a'
    assert r[1] == 1
    assert r[2] == 'b'
    assert r[3] == True
    assert r[4] == None
    assert r[5] == 3.14159
    assert r[6] == b'some bytes'

def test_tapisresult_dict():
    result = {'a': 1, 'b': 'bee', 'c': b'bytes', 'd': True, 'e': 3.14159, 'f': None}
    tr = TapisResult(**result)
    assert tr.a == 1
    assert tr.b == 'bee'
    assert tr.c == b'bytes'
    assert tr.d is True
    assert tr.e == 3.14159
    assert tr.f is None

def test_tapisresult_list_o_dict():
    result = [{'a': 1, 'b': 'bee', 'c': b'bytes', 'd': True, 'e': 3.14159, 'f': None},
              {'a': 10, 'b': 'foo', 'c': b'bytes', 'd': False, 'e': 3.14159, 'f': None},
              ]
    tr_list = [TapisResult(**r) for r in result]
    assert len(tr_list) == 2
    # first item -
    tr_1 = tr_list[0]
    assert tr_1.a == 1
    assert tr_1.b == 'bee'
    assert tr_1.c == b'bytes'
    assert tr_1.d is True
    assert tr_1.e == 3.14159
    assert tr_1.f is None
    # 2nd item -
    tr_2 = tr_list[1]
    assert tr_2.a == 10
    assert tr_2.b == 'foo'
    assert tr_2.c == b'bytes'
    assert tr_2.d is False
    assert tr_2.e == 3.14159
    assert tr_2.f is None

def test_tapisresult_nested_dicts():
    result = [{'a': [{'bb': 10, 'cc': True}, {'dd': 5}],
               'b': [{'ee': b'bytes'}] },
              {'time_1': [{'x_0': 'abc', 'x_1': 'def'}, {'y_0': 0, 'y_1': 3.14}]}
              ]
    tr_list = [TapisResult(**r) for r in result]
    assert len(tr_list) == 2
    # first item -
    tr_1 = tr_list[0]
    assert type(tr_1.a) == list
    assert tr_1.a[0].bb == 10
    assert tr_1.a[0].cc is True
    assert tr_1.a[1].dd == 5

    # 2nd item -
    tr_2 = tr_list[1]
    assert type(tr_2.time_1) == list
    assert tr_2.time_1[0].x_0 == 'abc'
    assert tr_2.time_1[0].x_1 == 'def'
    assert tr_2.time_1[1].y_0 == 0
    assert tr_2.time_1[1].y_1 == 3.14

def test_tapisresult_self_in_response():
    result = [{"self": "use 'self' in the response and you know you're foobar.",
               "a_key": "a_value"}]
    tr_list = [TapisResult(r) for r in result]
    assert len(tr_list) == 1

# ----------------
# tokens API tests -
# ----------------

def test_client_has_tokens(client):
    # the fixture should have already created tokens on the client.
    # the access token object
    assert hasattr(client, 'access_token')
    access_token = client.access_token
    # the actual JWT
    assert hasattr(access_token, 'access_token')
    # the expiry fields
    assert hasattr(access_token, 'expires_at')
    assert hasattr(access_token, 'expires_in')

    # the refresh token object - Users refresh_token obj should be empty.
    assert hasattr(client, 'refresh_token')


def test_create_token(client):
    toks = client.tokens.create_token(token_username=client.username,
                                      token_tenant_id=client.tenant_id,
                                      account_type="user",
                                      access_token_ttl=14400,
                                      generate_refresh_token=True,
                                      target_site_id='tacc',
                                      refresh_token_ttl=9999999)
    assert hasattr(toks, 'access_token')
    access_token= toks.access_token
    assert hasattr(access_token, 'access_token')
    assert hasattr(access_token, 'expires_at')
    assert hasattr(access_token, 'expires_in')

    assert hasattr(toks, 'refresh_token')
    refresh_token= toks.refresh_token
    assert hasattr(refresh_token, 'refresh_token')
    assert hasattr(refresh_token, 'expires_at')
    assert hasattr(refresh_token, 'expires_in')


# -----------------------------------------------
# client + refresh token + refresh_tokens() tests -
# -----------------------------------------------

def test_refresh_tokens(client):
    auth_clients = client.authenticator.list_clients()
    if auth_clients:
        testing_client = auth_clients[0]
    if not auth_clients:
        testing_client = client.authenticator.create_client()
    
    k = Tapis(base_url=BASE_URL,
              username=USERNAME,
              password=PASSWORD,
              client_id=testing_client.client_id,
              client_key=testing_client.client_key)

    # k should not have access or refresh until we run k.get_tokens()
    assert hasattr(k, 'access_token')
    access_token= k.access_token
    assert not hasattr(access_token, 'access_token')
    assert not hasattr(access_token, 'expires_at')
    assert not hasattr(access_token, 'expires_in')

    assert hasattr(k, 'refresh_token')
    refresh_token= k.refresh_token
    assert not hasattr(refresh_token, 'refresh_token')
    assert not hasattr(refresh_token, 'expires_at')
    assert not hasattr(refresh_token, 'expires_in')

    # We now run get_tokens(). k should now have access and refresh tokens.
    k.get_tokens()

    assert hasattr(k, 'access_token')
    access_token= k.access_token
    assert hasattr(access_token, 'access_token')
    assert hasattr(access_token, 'expires_at')
    assert hasattr(access_token, 'expires_in')

    assert hasattr(k, 'refresh_token')
    refresh_token= k.refresh_token
    assert hasattr(refresh_token, 'refresh_token')
    assert hasattr(refresh_token, 'expires_at')
    assert hasattr(refresh_token, 'expires_in')

    # Now we should be able to run refresh_tokens() with no problems and
    # still have access and refresh tokens after the fact.
    k.refresh_tokens()

    assert hasattr(k, 'access_token')
    access_token= k.access_token
    assert hasattr(access_token, 'access_token')
    assert hasattr(access_token, 'expires_at')
    assert hasattr(access_token, 'expires_in')

    assert hasattr(k, 'refresh_token')
    refresh_token= k.refresh_token
    assert hasattr(refresh_token, 'refresh_token')
    assert hasattr(refresh_token, 'expires_at')
    assert hasattr(refresh_token, 'expires_in')


# ---------------------------------------------------
# Instantiate Tapipy with only client + refresh_token
# ---------------------------------------------------

def test_init_with_only_client_and_refresh_token(client):
    auth_clients = client.authenticator.list_clients()
    if auth_clients:
        testing_client = auth_clients[0]
    if not auth_clients:
        testing_client = client.authenticator.create_client()
    
    # Need to first get refresh_tokens(using another Tapis client in this case)
    t2 = Tapis(base_url=BASE_URL,
                username=USERNAME,
                password=PASSWORD,
                client_id=testing_client.client_id,
                client_key=testing_client.client_key)

    t2.get_tokens()

    # Now only use client + refresh_token
    k = Tapis(base_url=BASE_URL,
              client_id=testing_client.client_id,
              client_key=testing_client.client_key,
              refresh_token=t2.refresh_token)

    # Test that everything works.
    k.get_tokens()

    assert hasattr(k, 'access_token')
    access_token= k.access_token
    assert hasattr(access_token, 'access_token')
    assert hasattr(access_token, 'expires_at')
    assert hasattr(access_token, 'expires_in')

    assert hasattr(k, 'refresh_token')
    refresh_token= k.refresh_token
    assert hasattr(refresh_token, 'refresh_token')
    assert hasattr(refresh_token, 'expires_at')
    assert hasattr(refresh_token, 'expires_in')



# -----------------
# tenants API tests -
# -----------------

def test_list_tenants(client):
    tenants = client.tenants.list_tenants()
    sites = client.tenants.list_sites()
    admin_tenants = set()
    for s in sites:
        admin_tenants.add(s.site_admin_tenant_id)
    for t in tenants:
        assert hasattr(t, 'base_url')
        assert hasattr(t, 'tenant_id')
        assert hasattr(t, 'public_key')
        assert hasattr(t, 'token_service')
        assert hasattr(t, 'security_kernel')
        # Only non-admin tenants require `token_gen_services` key
        if not t.tenant_id in admin_tenants:
            assert hasattr(t, 'token_gen_services')

def test_get_tenant_by_id(client):
    t = client.tenants.get_tenant(tenant_id='dev')
    assert t.base_url == 'https://dev.develop.tapis.io'
    assert t.tenant_id == 'dev'
    assert t.public_key.startswith('-----BEGIN PUBLIC KEY-----')
    assert t.token_service == 'https://dev.develop.tapis.io/v3/tokens'
    assert t.security_kernel == 'https://dev.develop.tapis.io/v3/security'

def test_list_owners(client):
    owners = client.tenants.list_owners()
    for o in owners:
        assert hasattr(o, 'create_time')
        assert hasattr(o, 'email')
        assert hasattr(o, 'last_update_time')
        assert hasattr(o, 'name')

def test_get_owner(client):
    owner = client.tenants.get_owner(email='CICSupport@tacc.utexas.edu')
    assert owner.email == 'CICSupport@tacc.utexas.edu'
    assert owner.name == 'CIC Support'


# ---------------------
# Security Kernel tests -
# ---------------------

def test_list_roles(client):
    roles = client.sk.getRoleNames(tenant=client.tenant_id)
    assert hasattr(roles, 'names')
    assert type(roles.names) == list
    if len(roles.names) > 0:
        assert type(roles.names[0]) == str


# --------------------
# Debug flag tests -
# --------------------

def test_debug_flag_tenants(client):
    result, debug = client.tenants.list_tenants(_tapis_debug=True)
    assert hasattr(debug, 'request')
    assert hasattr(debug, 'response')
    assert hasattr(debug.request, 'url')
    assert hasattr(debug.response, 'content')


# -----------------------
# Tapipy import timing test -
# -----------------------

def test_import_timing():
    start = time.time()
    subprocess.call(['python', '-c', 'from tapipy.tapis import Tapis'])
    import_time = time.time() - start
    assert import_time <= 3


# -----------------------
# Download spec tests -
# -----------------------

def test_download_service_dev_specs():
    t = Tapis(base_url=BASE_URL,
              username=USERNAME,
              password=PASSWORD,
              resource_set="dev")
    t.get_tokens()
    return t
