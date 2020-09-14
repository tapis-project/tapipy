# A suite of integrations tests for the Tapis Python SDK.
# Build the test docker image: docker build -t tapis/pysdk-tests -f Dockerfile-tests .
# Run these tests using the built docker image: docker run -it --rm  tapis/pysdk-tests

import pytest

from common.config import conf
from tapipy.tapis import TapisResult, Tapis

@pytest.fixture
def client():
    base_url = getattr(conf, 'base_url', 'https://dev.develop.tapis.io')
    username = getattr(conf, 'username', 'pysdk')
    account_type = getattr(conf, 'account_type', 'service')
    tenant_id = getattr(conf, 'tenant_id', 'master')
    service_password = getattr(conf, 'service_password', None)
    t = Tapis(base_url=base_url,
                 username=username,
                 account_type=account_type,
                 tenant_id=tenant_id,
                 service_password=service_password)
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
    tr_list = [TapisResult(**r) for r in result]
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

    # the refresh token object
    assert hasattr(client, 'refresh_token')
    # the actual JWT -
    refresh_token = client.refresh_token
    # the expiry fields
    assert hasattr(refresh_token, 'expires_at')
    assert hasattr(refresh_token, 'expires_in')


def test_create_token(client):
    toks = client.tokens.create_token(token_username=conf.username,
                                      token_tenant_id='master',
                                      account_type='service',
                                      access_token_ttl=14400,
                                      generate_refresh_token=True,
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


# -----------------
# tenants API tests -
# -----------------

def test_list_tenants(client):
    tenants = client.tenants.list_tenants()
    for t in tenants:
        assert hasattr(t, 'base_url')
        assert hasattr(t, 'tenant_id')
        assert hasattr(t, 'public_key')
        assert hasattr(t, 'is_owned_by_associate_site')
        assert hasattr(t, 'token_service')
        assert hasattr(t, 'security_kernel')

def test_get_tenant_by_id(client):
    t = client.tenants.get_tenant(tenant_id='dev')
    assert t.base_url == 'https://dev.develop.tapis.io'
    assert t.tenant_id == 'dev'
    assert t.public_key.startswith('-----BEGIN PUBLIC KEY-----')
    assert t.is_owned_by_associate_site == False
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
    roles = client.sk.getRoleNames(tenant='master')
    assert hasattr(roles, 'names')
    assert type(roles.names) == list
    if len(roles.names) > 0:
        assert type(roles.names[0]) == str

def test_create_role(client):
    # first, make sure role is not there -
    try:
        client.sk.deleteRoleByName(tenant='master', roleName='pysdk_test_role', user='tenants')
    except:
        pass
    # create the test role -
    role = client.sk.createRole(tenant='master', roleName='pysdk_test_role',
                                description='test role created by pysdk', user='tenants')
    assert hasattr(role, 'url')

def test_role_user_list_initially_empty(client):
    users = client.sk.getUsersWithRole(tenant='master', roleName='pysdk_test_role')
    assert users.names == []

def test_add_user_to_role(client):
    result = client.sk.grantRole(tenant='master', roleName='pysdk_test_role', user='tenants')
    assert hasattr(result, 'changes')
    assert result.changes == 1

def test_user_has_role(client):
    roles = client.sk.getUserRoles(tenant='master', user='tenants')
    assert hasattr(roles, 'names')
    assert type(roles.names) == list
    assert 'pysdk_test_role' in roles.names

def test_user_in_role_user_list(client):
    users = client.sk.getUsersWithRole(tenant='master', roleName='pysdk_test_role')
    assert hasattr(users, 'names')
    assert type(users.names) == list
    assert 'tenants' in users.names

def test_revoke_user_from_role(client):
    result = client.sk.revokeUserRole(tenant='master', roleName='pysdk_test_role', user='tenants')
    assert hasattr(result, 'changes')
    assert result.changes == 1

def test_user_no_longer_in_role(client):
    roles = client.sk.getUserRoles(tenant='master', user='tenants')
    assert hasattr(roles, 'names')
    assert type(roles.names) == list
    assert 'tenants' not in roles.names

def test_delete_role(client):
    result = client.sk.deleteRoleByName(tenant='master', roleName='pysdk_test_role', user='tenants')
    assert hasattr(result, 'changes')
    assert result.changes == 1


# --------------------
# Debug flag tests -
# --------------------

def test_debug_flag_tenants(client):
    result, debug = client.tenants.list_tenants(_tapis_debug=True)
    assert hasattr(debug, 'request')
    assert hasattr(debug, 'response')
    assert hasattr(debug.request, 'url')
    assert hasattr(debug.response, 'content')


# ---------------------
# Metadata tests -
# ---------------------
def test_create_coll(client):
    result,debug = client.meta.createCollection(db='testdb', collection='testcoll',_tapis_debug=True)
    assert debug.response.status_code == 201

def test_get_coll_names(client):
    result = client.meta.listCollectionNames(db='testdb')
    assert 'testcoll' in str(result)

#delete collection cannot be exercised as it needs additional header If-Match

#def test_create_doc(client):
 #   result = client.meta.createDocument(db='testdb', collection='testcoll')
 #   assert str(result)!= ''

#def test_get_doc_(client):
 #   result = client.meta.getDocument(db='testdb', collection='testcoll', docId='5e45b2cca93eebf39fbe1043')
 #   assert 'testdoc' in str(result)



