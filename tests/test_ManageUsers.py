import json, pytest
from werkzeug.security import check_password_hash


# NEW USER 
@pytest.mark.parametrize('sample_list', [
    ['user1@gmail.com', "hiLol123!",1],
    ['user2@gmail.com',  "hiLol123!",2],
    ['user3@gmail.com',  "hiLol123!",3],
    ['user4@gmail.com',  "hiLol123!",4]
])
def test_New_User(client, sample_list, capsys):
    with capsys.disabled():
        # pritn(sample_list[0])
        data = json.dumps({
            'email': sample_list[0],
            'password': sample_list[1]
        })
        response = client.post('/api/user/add',json=data,content_type='application/json')
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'
        result = json.loads(response.get_data(as_text=True))['result']
        assert int(result) == sample_list[2]

@pytest.mark.xfail(strict=True, reason='Invalid inputs')
@pytest.mark.parametrize('sample_list', [
    ['invalidemail', 'hiLol123#', 3],
    ['valid@email.com', 'h11111111', 2],
    ['SP', '1111111', 1]
])
def test_add_new_user_invalid_input(client, sample_list, capsys):
    test_New_User(client, sample_list, capsys)


@pytest.mark.xfail(strict=True, reason='Duplicate email inputs')
@pytest.mark.parametrize('sample_list', [
    ['user1@gmail.com', 'hiLol123#', 2],
    ['user1@gmail.com', 'byeLol123#', 2]
])
def test_add_new_user_dupe_email(client, sample_list, capsys):
    test_New_User(client, sample_list, capsys)


@pytest.mark.xfail(strict=True, reason='Missing inputs')
@pytest.mark.parametrize('sample_list', [
    [None, '12345Abc#', 1],
    ['user4@gmail.com', None, 2]
])
def test_add_new_user_missing(client, sample_list, capsys):
    test_New_User(client, sample_list,capsys)



# @pytest.mark.usefixtures('add_user')
# @pytest.mark.parametrize('sample_list', [
#     # [1,'user1@gmail.com', "hiLol123!"],
#     [2,'user2@gmail.com',  "hiLol123!"],
#     [3,'user3@gmail.com',  "hiLol123!"],
#     [4,'user4@gmail.com',  "hiLol123!"]
# ])
# def test_get_user(client, sample_list, capsys):
#     with capsys.disabled():
#         data = {'email': sample_list[1], 'password': sample_list[2]}
#         response = client.post(f'/api/login', data=json.dumps(data))
#         assert response.status_code == 200
#         assert response.headers['Content-Type'] == 'application/json'
#         user = json.loads(response.get_data(as_text=True))
#         assert user['result'] == sample_list[0]


# @pytest.mark.xfail(strict=True, reason='Non-existent User')
# @pytest.mark.parametrize('sample_list', [
#     [100, 'user100@gmail.com','hiLol123#'],
#     [99, 'user99@gmail.com','hiLol123#']
# ])
# def test_get_user_nontexist(client, sample_list, capsys):
#     test_get_user(client, sample_list, capsys)

