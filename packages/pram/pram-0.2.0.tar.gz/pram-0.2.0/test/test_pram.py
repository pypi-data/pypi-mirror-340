from pram import Pram, pram
import numpy as np
import pandas as pd


def test_get_transition_matrix_equal():
    data = ['Male', 'Female', 'Male', 'Female']
    matrix = Pram.__get_transition_matrix__(data)
    assert(((matrix.values[0] == 0.5) & (matrix.values[1] == 0.5)).all())


def test_get_transition_matrix_majority():
    data = ['Male', 'Male', 'Male', 'Female']
    m = Pram.__get_transition_matrix__(data)
    assert(m._get_value('Male', 'Male') == 0.75)
    assert(m._get_value('Female', 'Female') == 0.25)
    assert (m._get_value('Male', 'Female') == 0.75)
    assert (m._get_value('Female', 'Male') == 0.25)


def test_get_transition_matrix_same():
    data = ['Male', 'Male', 'Male', 'Male']
    matrix = Pram.__get_transition_matrix__(data)
    assert((matrix.values[0] == 1).all())


def test_get_weighted_transition_matrix_equal():
    data = ['Male', 'Female', 'Male', 'Female']
    matrix = Pram.__get_weighted_transition_matrix__(data, 0.8, 0.5)
    assert_matrix_is_valid(matrix)
    assert(matrix.values[0, 0] + matrix.values[1, 1] >= 1.6)
    assert (matrix.values[0, 1] + matrix.values[1, 0] <= 0.4)
    assert (matrix.values[0, 0] == matrix.values[1, 1])
    assert (matrix.values[0, 1] == matrix.values[1, 0])


def test_get_weighted_transition_matrix_majority():
    data = ['Male', 'Female', 'Male', 'Male']
    matrix = Pram.__get_weighted_transition_matrix__(data, 0.8, 0.5)
    assert_matrix_is_valid(matrix)
    assert(matrix._get_value('Female', 'Male') < matrix._get_value('Male', 'Female'))


def test_get_weighted_transition_matrix_majority_opposite():
    data = ['Male', 'Female', 'Female', 'Female']
    matrix = Pram.__get_weighted_transition_matrix__(data, 0.8, 0.5)
    assert_matrix_is_valid(matrix)
    assert(matrix._get_value('Male', 'Female') < matrix._get_value('Female', 'Male'))


def test_get_weighted_transition_matrix_majority_no_mods():
    data = ['Male', 'Male', 'Male', 'Female']
    matrix = Pram.__get_weighted_transition_matrix__(data, 0.0, 1.0)
    assert_matrix_is_valid(matrix)
    assert(matrix._get_value('Female', 'Male') < matrix._get_value('Male', 'Female'))
    assert (matrix._get_value('Female', 'Male') == 0.25)
    assert (matrix._get_value('Male', 'Female') == 0.75)


def test_get_weighted_transition_matrix_majority_identity():
    data = ['Male', 'Male', 'Male', 'Female']
    matrix = Pram.__get_weighted_transition_matrix__(data, 0.0, 0)
    assert_matrix_is_valid(matrix)
    assert(matrix.values[0, 0] == matrix.values[1, 1])
    assert(matrix.values[0, 1] == matrix.values[1, 0])
    assert (matrix.values[0, 0] == 1)
    assert (matrix.values[1, 1] == 1)


def test_get_weighted_transition_matrix_majority_50_alpha():
    data = ['Male', 'Male', 'Male', 'Female']
    matrix = Pram.__get_weighted_transition_matrix__(data, 0.0, 0.5)
    assert_matrix_is_valid(matrix)
    assert(matrix._get_value('Female', 'Male') < matrix._get_value('Male', 'Female'))
    assert (matrix._get_value('Female', 'Female') == 0.625)
    assert (matrix._get_value('Male', 'Male') == 0.875)


def test_replace_identity():
    data = ['Male', 'Male', 'Male', 'Female']
    matrix = Pram.__get_weighted_transition_matrix__(data, 0.0, 0)
    values = ['Male', 'Male', 'Male', 'Male']
    new_values = []
    for value in values:
        new_values.append(Pram.__pram_replace__(matrix, value))
    assert(new_values == values)


def test_pram():
    np.random.seed(1000)
    data = [
        {'gender': 'male', 'education': 'low'},
        {'gender': 'male', 'education': 'low'},
        {'gender': 'male', 'education': 'low'},
        {'gender': 'male', 'education': 'low'},
        {'gender': 'male', 'education': 'high'},
        {'gender': 'female', 'education': 'low'},
        {'gender': 'female', 'education': 'high'},
        {'gender': 'female', 'education': 'high'},
        {'gender': 'female', 'education': 'high'},
        {'gender': 'female', 'education': 'high'}
    ]
    df = pd.DataFrame(data)
    out = pram(df, m=0.0, alpha=1.0)
    male = out[(df.gender == 'male')].values.__len__()
    female = out[(df.gender == 'female')].values.__len__()
    high_education_male = out[(df.gender == 'male') & (df.education == 'high')].values.__len__()
    high_education_female = out[(df.gender == 'female') & (df.education == 'high')].values.__len__()
    assert(high_education_male == 1)
    assert(high_education_female == 4)
    assert(male == 5)
    assert(female == 5)

def test_stratification():
    data = [
        {'gender': 'male', 'education': 'low'},
        {'gender': 'male', 'education': 'low'},
        {'gender': 'male', 'education': 'low'},
        {'gender': 'male', 'education': 'low'},
        {'gender': 'male', 'education': 'high'},
        {'gender': 'female', 'education': 'low'},
        {'gender': 'female', 'education': 'high'},
        {'gender': 'female', 'education': 'high'},
        {'gender': 'female', 'education': 'high'},
        {'gender': 'female', 'education': 'high'}
    ]
    df = pd.DataFrame(data)

    for i in range(0, 10):
        out = pram(df, strata='gender')
        male = out[(df.gender == 'male')].values.__len__()
        female = out[(df.gender == 'female')].values.__len__()
        # None of the genders should change
        assert(male == 5)
        assert(female == 5)


def assert_matrix_is_valid(matrix):
    """
    Check that a matrix sums to 1 in each column
    :param matrix: the matrix to test
    :return: None
    """
    assert(matrix.values[0, 0] + matrix.values[1, 0] == 1)
    assert(matrix.values[0, 1] + matrix.values[1, 1] == 1)