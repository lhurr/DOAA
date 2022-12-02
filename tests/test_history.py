from application.model.pred_history import PredictionHistory
from datetime import datetime
import pytest

# Prediction history testing
@pytest.mark.parametrize(
    "sample_list",
    [
        [
            1,  # User_id (does not check fk constraints, so user with id 1 does not need to exist)
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
            400.9,  # Prediction
        ],
        [
            1, 
            33, #Age
            166, #Height
            99, # Weight            
            0,  # Diabetes
            1,  # blood pressure
            1,  # any transplants
            1,  # chronic
            0,  # allergy
            1, # cancer
            1, # surgeries
            23.9, #BMI
            450.6,  # Prediction
        ],
    ],
)
def test_History_Class(sample_list, capsys):
    with capsys.disabled():
        created_time = datetime.utcnow()
        new_entry = PredictionHistory(
            user_ID=sample_list[0],
            age=sample_list[1],
            height=sample_list[2],
            weight=sample_list[3],
            diabetes=sample_list[4],
            bloodpressure=sample_list[5],
            anytransplant=sample_list[6],
            chronic=sample_list[7],
            allergy=sample_list[8],
            cancer=sample_list[9],
            surgery=sample_list[10],
            bmi=sample_list[11],
            prediction=sample_list[12],
            created_time=created_time 
        )

        assert new_entry.user_ID == sample_list[0]
        assert new_entry.age == sample_list[1]
        assert new_entry.height == sample_list[2]
        assert new_entry.weight == sample_list[3]
        assert new_entry.diabetes == sample_list[4]
        assert new_entry.bloodpressure == sample_list[5]
        assert new_entry.anytransplant == sample_list[6]
        assert new_entry.chronic == sample_list[7]
        assert new_entry.allergy == sample_list[8]
        assert new_entry.cancer == sample_list[9]
        assert new_entry.surgery == sample_list[10]
        assert new_entry.bmi == sample_list[11]
        assert new_entry.prediction == sample_list[12]
        assert new_entry.created_time == created_time


# Expected testing
# Missing inputs
@pytest.mark.xfail(strict=True, reason='Missing Inputs')
@pytest.mark.parametrize(
    "sample_list",
    [
        [],
        [
            1,  # User_id (does not check fk constraints, so user with id 1 does not need to exist)
            None, #Age
            None, #Height
            78, # Weight            
            1,  # Diabetes
            0,  # blood pressure
            # 1,  # any transplants
            0,  # chronic
            1,  # allergy
            None, # cancer
            0, # surgeries
            None, #BMI
            400.9,  # Prediction
        ],
        
        [
            1, 
            33, #Age
            159, #Height
            99, # Weight            
            0,  # Diabetes
            1,  # blood pressure
            1,  # any transplants
            1,  # chronic
            None,  # allergy
            1, # cancer
            None, # surgeries
            23.9, #BMI
            450.6,  # Prediction
        ],
    ],
)
def test_History_Class_Missing(sample_list, capsys):
    test_History_Class(sample_list=sample_list, capsys=capsys)





# Inputs out of range
@pytest.mark.xfail(strict=True, reason='Input out of range')
@pytest.mark.parametrize(
    "sample_list",
    [
        [
            1,  # User_id 
            -20, #Age cant be -ve
            149, #Height
            67, # Weight            
            1,  # Diabetes (1 or 0)
            1,  # blood pressure(1 or 0)
            0,  # any transplants
            0,  # chronic
            1,  # allergy
            1, # cancer
            0, # surgeries
            23.3, #BMI
            400.9,  # Prediction
        ],
        
        [
            1,  # User_id 
            25, #Age
            -149, #Height cant be -ve
            67, # Weight            
            1,  # Diabetes (1 or 0)
            1,  # blood pressure(1 or 0)
            0,  # any transplants
            0,  # chronic
            1,  # allergy
            1, # cancer
            0, # surgeries
            24.3, #BMI
            400.9,  # Prediction
        ],
        [
            1,  # User_id 
            26, #Age 
            149, #Height
            0, # Weight cant be 0            
            1,  # Diabetes (1 or 0)
            1,  # blood pressure(1 or 0)
            0,  # any transplants
            0,  # chronic
            1,  # allergy
            1, # cancer
            0, # surgeries
            23.3, #BMI
            400.9,  # Prediction
        ],
        [
            1,  # User_id 
            29, #Age 
            149, #Height
            67, # Weight            
            3,  # Diabetes cannot be beyond (1 or 0)
            1,  # blood pressure(1 or 0)
            0,  # any transplants
            0,  # chronic
            1,  # allergy
            1, # cancer
            0, # surgeries
            23.3, #BMI
            400.9,  # Prediction
        ],
            [
            1,  # User_id 
            20, #Age 
            149, #Height
            67, # Weight            
            1,  # Diabetes (1 or 0)
            45,  # blood pressure must only be 0 or 1
            0,  # any transplants
            0,  # chronic
            1,  # allergy
            1, # cancer
            0, # surgeries
            23.3, #BMI
            400.9,  # Prediction
        ],
        [
            1,  # User_id 
            20, #Age 
            149, #Height
            67, # Weight            
            1,  # Diabetes (1 or 0)
            0,  # blood pressure 
            -1,  # any transplants (only 0 or 1)
            0,  # chronic
            1,  # allergy
            1, # cancer
            0, # surgeries
            23.3, #BMI
            400.9,  # Prediction
        ],
            [
            1,  # User_id 
            20, #Age 
            149, #Height
            67, # Weight            
            1,  # Diabetes 
            0,  # blood pressure 
            1,  # any transplants 
            -2,  # chronic (only 0 or 1)
            1,  # allergy
            1, # cancer
            0, # surgeries
            23.3, #BMI
            400.9,  # Prediction
        ],
                [
            1,  # User_id 
            20, #Age 
            149, #Height
            67, # Weight            
            1,  # Diabetes 
            0,  # blood pressure 
            0,  # any transplants 
            0,  # chronic
            -2,  # allergy (only 0 or 1)
            1, # cancer
            0, # surgeries
            23.3, #BMI
            400.9,  # Prediction
        ],
                        [
            1,  # User_id 
            20, #Age 
            149, #Height
            67, # Weight            
            1,  # Diabetes 
            0,  # blood pressure 
            0,  # any transplants 
            0,  # chronic
            1,  # allergy 
            -1, # cancer (only 0 or 1)
            0, # surgeries
            23.3, #BMI
            400.9,  # Prediction
        ],
                                [
            1,  # User_id 
            20, #Age 
            149, #Height
            67, # Weight            
            1,  # Diabetes 
            0,  # blood pressure 
            0,  # any transplants 
            0,  # chronic
            1,  # allergy 
            1, # cancer 
            -3, # surgeries (Must be iwthin 0 to 3, due to intrapolation)
            23.3, #BMI
            400.9,  # Prediction
        ],
        [
            1,  # User_id 
            20, #Age 
            149, #Height
            67, # Weight            
            1,  # Diabetes 
            0,  # blood pressure 
            0,  # any transplants 
            0,  # chronic
            1,  # allergy 
            1, # cancer 
            0, # surgeries
            -23.3, #BMI cannot be -ve
            400.9,  # Prediction
        ],
                                [
            1,  # User_id 
            20, #Age 
            149, #Height
            67, # Weight            
            1,  # Diabetes 
            0,  # blood pressure 
            0,  # any transplants 
            0,  # chronic
            1,  # allergy 
            0, # cancer (only 0 or 1)
            0, # surgeries
            23.3, #BMI
            -400.9,  # Prediction cant be -ve
        ],
    ],
)
def test_History_Class_Invalid(sample_list, capsys):
    test_History_Class(sample_list=sample_list, capsys=capsys)






# Wrong data type
@pytest.mark.xfail(strict=True, reason='Wrong data type')
@pytest.mark.parametrize(
    "sample_list",
    [
        [
            1,  # User_id 
            '29', #Age cannot be string
            149, #Height
            67, # Weight            
            1,  # Diabetes (1 or 0)
            1,  # blood pressure(1 or 0)
            0,  # any transplants
            0,  # chronic
            1,  # allergy
            1, # cancer
            0, # surgeries
            23.3, #BMI
            400.9,  # Prediction
        ],

    [
            1,  # User_id 
            29, #Age 
            True, #Height cant be boolean
            67, # Weight            
            1,  # Diabetes (1 or 0)
            1,  # blood pressure(1 or 0)
            0,  # any transplants
            0,  # chronic
            1,  # allergy
            1, # cancer
            0, # surgeries
            23.3, #BMI
            400.9,  # Prediction
        ],
        [
            1,  # User_id 
            29, #Age 
            149, #Height 

            '67', # Weight cant be string          
            1,  # Diabetes (1 or 0)
            1,  # blood pressure(1 or 0)
            0,  # any transplants
            0,  # chronic
            1,  # allergy
            1, # cancer
            0, # surgeries
            23.3, #BMI
            400.9,  # Prediction
        ],

        [
            1,  # User_id 
            29, #Age 
            156, #Height 
            67, # Weight            
            1.5,  # Diabetes cannot be float
            1,  # blood pressure(1 or 0)
            0,  # any transplants
            0,  # chronic
            1,  # allergy
            1, # cancer
            0, # surgeries
            23.3, #BMI
            400.9,  # Prediction
        ],

        [
            1,  # User_id 
            29, #Age 
            156, #Height 
            67, # Weight            
            1,  # Diabetes
            '1',  # blood pressure cant be string
            0,  # any transplants
            0,  # chronic
            1,  # allergy
            1, # cancer
            0, # surgeries
            23.3, #BMI
            400.9,  # Prediction
        ],

                [
            1,  # User_id 
            29, #Age 
            156, #Height 
            67, # Weight            
            1,  # Diabetes
            1,  # blood pressure 
            0.9,  # any transplants cant be float
            0,  # chronic
            1,  # allergy
            1, # cancer
            0, # surgeries
            23.3, #BMI
            400.9,  # Prediction
        ],
        [
            1,  # User_id 
            29, #Age 
            156, #Height 
            67, # Weight            
            1,  # Diabetes
            1,  # blood pressure 
            0,  # any transplants 
            0.3,  # chronic cant be float
            1,  # allergy
            1, # cancer
            0, # surgeries
            23.3, #BMI
            400.9,  # Prediction
        ],
        [
            1,  # User_id 
            29, #Age 
            156, #Height 
            67, # Weight            
            1,  # Diabetes
            1,  # blood pressure 
            0,  # any transplants 
            0,  # chronic
            '1',  # allergy cant be str
            1, # cancer
            0, # surgeries
            23.3, #BMI
            400.9,  # Prediction
        ],

                [
            1,  # User_id 
            29, #Age 
            156, #Height 
            67, # Weight            
            1,  # Diabetes
            1,  # blood pressure 
            0,  # any transplants 
            0,  # chronic
            1,  # allergy 
            '1', # cancer cant be str
            0, # surgeries
            23.3, #BMI
            400.9,  # Prediction
        ],
                [
            1,  # User_id 
            29, #Age 
            156, #Height 
            67, # Weight            
            1,  # Diabetes
            1,  # blood pressure 
            0,  # any transplants 
            0,  # chronic
            1,  # allergy
            '1', # cancer cant be str
            0, # surgeries
            23.3, #BMI
            400.9,  # Prediction
        ],
                        [
            1,  # User_id 
            29, #Age 
            156, #Height 
            67, # Weight            
            1,  # Diabetes
            1,  # blood pressure 
            0,  # any transplants 
            0,  # chronic
            1,  # allergy
            0, # cancer 
            'three', # surgeries cant be str
            23.3, #BMI
            400.9,  # Prediction
        ],

                                [
            1,  # User_id 
            29, #Age 
            156, #Height 
            67, # Weight            
            1,  # Diabetes
            1,  # blood pressure 
            0,  # any transplants 
            0,  # chronic
            1,  # allergy
            0, # cancer 
            2, # surgeries
            True, #BMI cant be boolean
            400.9,  # Prediction
        ],
        
                                [
            1,  # User_id 
            29, #Age 
            156, #Height 
            67, # Weight            
            1,  # Diabetes
            1,  # blood pressure 
            0,  # any transplants 
            0,  # chronic
            1,  # allergy
            0, # cancer 
            2, # surgeries
            23.3, #BMI 
            False,  # Prediction cant be bool
        ],
    ],
)
def test_History_Class_Wrong_Dtype(sample_list, capsys):
    test_History_Class(sample_list=sample_list, capsys=capsys)



