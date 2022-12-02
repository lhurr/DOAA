import json,pytest, datetime


# Store predictions API
@pytest.mark.parametrize('sample_list', [
        [
            55, #Age
            156, #Height
            88, # Weight            
            0,  # Diabetes
            1,  # blood pressure
            1,  # any transplants
            0,  # chronic
            1,  # allergy
            1, # cancer
            0, # surgeries
            23.9, #BMI
            488.9,  # Prediction
            3,
        ],
        
])
def test_post_prediction_api(client, sample_list, capsys):
    with capsys.disabled():
        data = json.dumps(dict(
            age= sample_list[0],
            height=sample_list[1],
            weight = sample_list[2],
            diabetes = sample_list[3],
            bloodpressure = sample_list[4],
            anytransplant = sample_list[5],
            chronic = sample_list[6],
            allergies = sample_list[7],
            cancer = sample_list[8], surgery = sample_list[9], bmi = sample_list[10], prediction = sample_list[11], user_ID = sample_list[12]
        ))

        response = client.post('/api/predict/add' , data=json.dumps(data),content_type="application/json")
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        result = json.loads(response.get_data(as_text=True))
        assert result['result'] == sample_list[12]


@pytest.mark.usefixtures('add_user')
@pytest.mark.xfail(reason="User does not exist", strict=True)
@pytest.mark.parametrize(
    "sample_list",
    [
               [
            55, #Age
            156, #Height
            88, # Weight            
            0,  # Diabetes
            1,  # blood pressure
            1,  # any transplants
            0,  # chronic
            1,  # allergy
            1, # cancer
            0, # surgeries
            23.9, #BMI
            488.9,  # Prediction
            1000,
        ],

    ],
)
def test_add_entry_invalid_user_id(client, sample_list, capsys):
    test_post_prediction_api(client, sample_list, capsys)


        

