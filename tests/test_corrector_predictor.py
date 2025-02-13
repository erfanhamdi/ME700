import pytest
import numpy as np
from src.corrector_predictor import ElastoPlastic, InputStrain, Isotropic_EP, Kinematic_EP, main_loop

def test_eps_profile():
    eps = [0, 1, -1]
    load_step_list = [1, 1]
    input_strain = InputStrain(eps, load_step_list)
    eps_array = input_strain.strain_profile()
    assert eps_array.shape[0] == sum(load_step_list) + 1
    assert eps_array[-1] == eps[-1]
    assert np.allclose(eps_array, [0, 1, -1])

def test_isotropic_hardening():
    eps_array = np.array([0, 0, 0.0075, 0.03, 0.05, 0.0])
    mat = Isotropic_EP(E = 1000, E_t = 100, Y_0 = 10)
    sigma_list, eps_p_list = main_loop(mat, eps_array)
    print(sigma_list)
    assert np.allclose(sigma_list, [0, 0, 7.5, 12, 14, -16.2])

def test_kinematic_hardening():
    eps_array = np.array([0, 0, 0.0075, 0.03, 0.05, 0.0])
    mat = Kinematic_EP(E = 1000, E_t = 100, Y_0 = 10)
    sigma_list, eps_p_list = main_loop(mat, eps_array)
    print(sigma_list)
    assert np.allclose(sigma_list, [0, 0, 7.5, 12, 14, -9])

def test_mat_input():
    with pytest.raises(ValueError):
        mat = ElastoPlastic(E = -1000, Y_0= 100)
    with pytest.raises(ValueError):
        mat = ElastoPlastic(E = [1000], H = -100, Y_0= [100])
    with pytest.raises(ValueError):
        mat = ElastoPlastic(E = 10, H = '100', Y_0= 100)
    with pytest.raises(ValueError):
        mat = ElastoPlastic(E = 1000, H = -100, Y_0= -100)
    # check if raise valueerror if E < 0
    with pytest.raises(ValueError):
        mat = Isotropic_EP(E = -1000, E_t = 100, Y_0 = 10)
    # check if raise valueerror if E_t < 0
    with pytest.raises(ValueError):
        mat = Isotropic_EP(E = 1000, E_t = -100, Y_0 = 10)
    with pytest.raises(ValueError):
        mat = Isotropic_EP(E = 1000, E_t = '100', Y_0 = 10.0)
    with pytest.raises(ValueError):
        mat = Isotropic_EP(E = 1000, E_t = 100, Y_0 = -10)
    with pytest.raises(ValueError):
        mat = Isotropic_EP(E = 1000, E_t = 100, Y_0 = '10')

def test_init_none_for_one_argument():
    mat = ElastoPlastic(E=100, H=None, E_t=900, Y_0=10)
    assert mat.H == pytest.approx(np.abs((1/100 - 1/900)**-1))

    mat = ElastoPlastic(E=None, H=50, E_t=900, Y_0=10)
    assert mat.E == pytest.approx(np.abs((1/50 - 1/900)**-1))

    mat = ElastoPlastic(E=100, H=50, E_t=None, Y_0=10)
    assert mat.E_t == pytest.approx(np.abs((1/100 + 1/50)**-1))

def test_no_yield_stress_given():
    # check if raise valueerror if Y_0 is not given
    with pytest.raises(ValueError):
        mat = Isotropic_EP(E = 1000, E_t = 100)

def test_d_eps_p_positive_phi():
    mat = ElastoPlastic(E=1000, H=100, E_t=900, Y_0=10)
    phi_trial = 50
    expected = 50 / (1000 + 100)
    assert mat.d_eps_p(phi_trial) == pytest.approx(expected)

def test_y_new():
    mat = ElastoPlastic(E=1000, H=100, E_t=900, Y_0=10)
    mat.y_new(0.2)
    assert mat.Y == pytest.approx(10 + 100 * 0.2)

def test_sigma_trial():
    mat = ElastoPlastic(E=1000, H=50, E_t=900, Y_0=10)
    sigma_old = 20
    d_eps = 0.01
    sigma_trial = mat.sigma_trial(sigma_old, d_eps)
    assert sigma_trial == pytest.approx(20 + 1000 * 0.01)

def test_check_state_elastic():
    mat = ElastoPlastic(E=1000, H=50, E_t=900, Y_0=100)
    phi, state = mat.check_state(80)
    assert phi == pytest.approx(abs(80) - 100)
    assert bool(state) is True

def test_check_state_plastic():
    mat = ElastoPlastic(E=1000, H=50, E_t=900, Y_0=50)
    phi, state = mat.check_state(60)
    assert phi == pytest.approx(10)
    assert bool(state) is False


