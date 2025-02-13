import numpy as np
import matplotlib.pyplot as plt

class InputStrain:
    def __init__(self, eps, load_step_list):
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
    def __init__(self, **kwargs):
        required_keys = {"E", "H", "E_t"}
        provided_inputs = required_keys.intersection(kwargs.keys())
        if len(provided_inputs) < 2:
            raise ValueError("At least two of (E, H, E_t) is required.")

        self.E = kwargs.get("E")
        self.H = kwargs.get("H")
        self.E_t = kwargs.get("E_t")
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
    
    def y_new(self, eps_p):
        self.Y = self.Y_0 + self.H * eps_p
    
    def sigma_trial(self, sigma_old, d_eps):
        return sigma_old + self.E * d_eps

    def check_state(self, sigma_trial):
        self.phi = np.abs(sigma_trial) - self.Y
        return self.phi, self.phi <= 0

    def d_eps_p(self, phi_trial):
        return phi_trial / (self.E + self.H)

class Kinematic_EP(ElastoPlastic):
    
    def update_state(self, d_eps, sigma, eps_p, alpha):
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
    def update_state(self, d_eps, sigma, eps_p, alpha = 0):
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
            
def main_loop(mat, eps_profile):
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