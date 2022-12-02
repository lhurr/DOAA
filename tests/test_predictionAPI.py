import pytest
import json

@pytest.mark.parametrize('sample_list', [
        [
            55, #Age
            148, #Height
            78, # Weight            
            1,  # Diabetes
            0,  # blood pressure
            1,  # any transplants
            0,  # chronic
            1,  # allergy
            1, # cancer
            0, # surgeries
            22.9, #BMI
            # 400.9,  # Prediction
        ],
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
            # 488.9,  # Prediction
        ],
])
def test_prediction_api(client, sample_list, capsys):
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
            cancer = sample_list[8], surgery = sample_list[9], bmi = sample_list[10]
        ))
        response = client.post('/api/predict',
                               data=data,
                               content_type='application/json')


        response_body = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"

        return float(response_body["prediction"])


# CONSISTENCY TESTING CHECK that predictions are consistent
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
            # 488.9,  # Prediction
        ],
        [
            55, #Age
            144, #Height
            77, # Weight            
            1,  # Diabetes
            0,  # blood pressure
            1,  # any transplants
            0,  # chronic
            1,  # allergy
            1, # cancer
            0, # surgeries
            23.9, #BMI
            # 488.9,  # Prediction
        ],
        
    ],
)
def test_predict_api_rangetests(client, sample_list, capsys):
    arr = []
    for _ in range(10):
        pred = test_prediction_api(client, sample_list, capsys) 
        arr.append(pred)
    assert all(x == arr[0] for x in arr), 'Not consistent'