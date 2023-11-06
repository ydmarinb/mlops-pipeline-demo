
import sys
sys.path.append('../')

from predict import make_prediction



def test_make_prediction(sample_input_data):
    # Given
    expected_prediction_value = 0

    # When
    predictions = make_prediction(input_data=sample_input_data)

    # Then
    assert isinstance(predictions, int)
    assert predictions == expected_prediction_value 