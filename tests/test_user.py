from application.model.user import User
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
import pytest



@pytest.mark.parametrize("sample_list",[
    ["user1@ichat.com", "passWord1234*^#!"], ["testing@gmail.com", "s3cur3P@ssw0rd"]
])
def test_User_Class(sample_list, capsys):
    with capsys.disabled():
        created_time = dt.utcnow()
        password_hash = generate_password_hash(sample_list[1])
        newUser = User(
            email=sample_list[0],
            password=password_hash,
            created_time=created_time,
        )
        assert newUser.email == sample_list[0]
        assert check_password_hash(newUser.password, sample_list[1])
        assert newUser.created_time == created_time


# Expected failure

@pytest.mark.xfail(strict=True, reason='Missing inputs')
@pytest.mark.parametrize("sample_list", [
    [],
    ['',  '12345!@#Au'],
    ['lim@ichat.org',  None],
    [None,None],
    [None, ],
    [None,  'Password4321!@#$']
])
def test_User_Class_missing(sample_list,capsys):
    test_User_Class(sample_list,capsys)

@pytest.mark.xfail(strict=True, reason='Invalid inputs')
@pytest.mark.parametrize("sample_list", [
    ['invalid_email', '123456!@#Au'],
    # ['email2@gmail.com', '9182911'], # No small letters
    # ['zyx@abc.com', 'Abcde123'], # No special characters
    ["world hello", "s3cur3P@ssw0rd!@"],
    ["hello.ipynb", "s3cur3P@ssw0rd!@"]

    # Removed a few, as model validation cannot check password, because it is already hashed, We also have validated in forms,
])
def test_User_Class_invalid_input(sample_list, capsys):
    test_User_Class(sample_list,capsys)





