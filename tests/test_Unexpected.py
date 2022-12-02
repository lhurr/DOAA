import pytest, json,re

@pytest.mark.parametrize('endpoint_list', [
    '/history',
    '/home'
])
def test_unexpected(client, endpoint_list, capsys):
    with capsys.disabled():
        response = client.get(endpoint_list)
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'text/html; charset=utf-8'