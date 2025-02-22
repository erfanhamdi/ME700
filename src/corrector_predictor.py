import numpy as np
import matplotlib.pyplot as plt

class InputStrain:
    """
    This class is used to generate strain profile for the material model.
    """
    def __init__(self, eps: list, load_step_list: list) -> None:
        """
        input:
            eps: list of strain values
            load_step_list: list of number of load steps between each strain value
        output:
            strain profile: np.array of strain values
        """
        self.eps = eps
        self.load_step_list = load_step_list
    def strain_profile(self):
        eps_list = []
        t_list = []
        eps_start = self.eps[0]
        for i in range(1, len(self.eps)):
            eps_ = self.eps[i]
            eps_list.append(np.linspace(eps_start, eps_, self.load_step_list[i-1], endpoint=False))
            eps_start = self.eps[i]
        eps_list.append(np.array([self.eps[-1]]))
        return np.concatenate(eps_list)

class ElastoPlastic:
    """
    This is the base class for elasto-plastic material model.
    """
    def __init__(self, **kwargs):
        required_keys = {"E", "H", "E_t"}
        provided_inputs = required_keys.intersection(kwargs.keys())
        if len(provided_inputs) < 2:
            raise ValueError("At least two of (E, H, E_t) is required.")
        # Young's modulus
        self.E = kwargs.get("E")
        # Hardening modulus
        self.H = kwargs.get("H")
        # Tangent modulus
        self.E_t = kwargs.get("E_t")
        # Yield stress
        self.Y = kwargs.get("Y_0")
        self.Y_0 = kwargs.get("Y_0")
        # check dtype for each input raise error if not float
        if self.E is not None:
            if not isinstance(self.E, (int, float)):
                raise ValueError("E must be a number.")
            if self.E <= 0:
                raise ValueError("E must be positive.")
        
        if self.H is not None:
            if not isinstance(self.H, (int, float)):
                raise ValueError("H must be a number.")
            if self.H <= 0:
                raise ValueError("H must be positive.")

        if self.E_t is not None:
            if not isinstance(self.E_t, (int, float)):
                raise ValueError("E_t must be a number.")
            if self.E_t <= 0:
                raise ValueError("E_t must be positive.")

        if self.Y is not None:
            if not isinstance(self.Y, (int, float)):
                raise ValueError("Yield stress must be a number.")
            if self.Y <= 0:
                raise ValueError("Yield stress must be positive.")

        if self.H is None:
            self.H = np.abs((1/self.E - 1/self.E_t)**-1)
        elif self.E_t is None:
            self.E_t = np.abs((1/self.E + 1/self.H)**-1)
        elif self.E is None:
            self.E = np.abs((1/self.H - 1/self.E_t)**-1)
        if self.Y is None:
            raise ValueError("Yield stress must be provided.")
        self.phi = 0
    
    def y_new(self, eps_p: float):
        """
        This function updates the yield stress.
        """
        self.Y = self.Y_0 + self.H * eps_p
    
    def sigma_trial(self, sigma_old: float, d_eps: float):
        return sigma_old + self.E * d_eps

    def check_state(self, sigma_trial: float):
        """
        This function checks if the material is in elastic or plastic state.
        """
        self.phi = np.abs(sigma_trial) - self.Y
        return self.phi, self.phi <= 0

    def d_eps_p(self, phi_trial: float):
        return phi_trial / (self.E + self.H)

class Kinematic_EP(ElastoPlastic):
    """
    This class is used to implement the kinematic hardening model.
    """
    def update_state(self, d_eps: float, sigma: float, eps_p: float, alpha: float):
        """
        This function updates the state of the material model.

        input:
            d_eps: float, strain increment
            sigma: float, stress at the start of the step
            eps_p: float, plastic strain at the start of the step
            alpha: float, alpha at the start of the step
        output:
            sigma_n: float, stress at the end of the step
            eps_p_n: float, plastic strain at the end of the step
            alpha_n: float, alpha at the end of the step
        """
        sigma_trial = self.sigma_trial(sigma, d_eps)
        alpha_trial = alpha
        eta_trial = sigma_trial - alpha_trial
        phi_trial, state = self.check_state(eta_trial)
        if state:
            sigma_n = sigma_trial
            alpha_n = alpha_trial
            eps_p_n = eps_p
        else:
            d_eps_p = self.d_eps_p(phi_trial)
            sigma_n = sigma_trial - np.sign(eta_trial) * self.E * d_eps_p
            alpha_n = alpha + np.sign(eta_trial) * self.H * d_eps_p
            eps_p_n = eps_p + d_eps_p
        return sigma_n,  eps_p_n, alpha_n

class Isotropic_EP(ElastoPlastic):
    """
    This class is used to implement the isotropic hardening model.
    """
    def update_state(self, d_eps: float, sigma: float, eps_p: float, alpha = 0):
        """
        This function updates the state of the material model.
        alpha is set to zero in this material model.
        """
        sigma_trial = self.sigma_trial(sigma, d_eps)
        phi_trial, state = self.check_state(sigma_trial)
        if state:
            sigma_n = sigma_trial
            eps_p_n = eps_p
        else:
            d_eps_p = self.d_eps_p(phi_trial)
            sigma_n = sigma_trial - np.sign(sigma_trial) * self.E * d_eps_p
            eps_p_n = eps_p + d_eps_p
        self.y_new(eps_p_n)
        return sigma_n, eps_p_n, 0
            
def main_loop(mat, eps_profile: np.array):
    """
    This function is used to run the main loop of the material model.

    input:
        mat: material model object
        eps_profile: np.array of strain values
    output:
        sigma_list: list of stress values
        eps_p_list: list of plastic strain values
    """
    sigma = 0
    eps_p = 0
    alpha = 0
    eps_p_list = [eps_p]
    d_eps_p = 0
    sigma_list = [sigma]
    d_eps_arr = (eps_profile[1:] - eps_profile[:-1])
    for i, d_eps in enumerate(d_eps_arr):
        eps_ = eps_profile[i+1]
        sigma_n, eps_p_n, alpha_n = mat.update_state(d_eps, sigma, eps_p, alpha)
        sigma_list.append(sigma_n)
        eps_p_list.append(eps_p_n)
        sigma = sigma_n
        eps_p = eps_p_n
        alpha = alpha_n
    return sigma_list, eps_p_list