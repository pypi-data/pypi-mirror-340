import numpy as np
from ...models.microstructure_models import MicroStructModel
from .functions.scipy_sandix import (sandix_signal_from_vector,
                                                                sandix_jacobian_from_vector,
                                                                sandix_optimized_mse_jacobian)


class Sandix(MicroStructModel):
    """Soma And Neurite Density Imaging model with Exchange for diffusion MRI."""

    # Class attributes
    n_params = 6
    param_names = ["t_ex", "Di", "De", "f", "rs", "fs"]
    classic_limits = np.array([[1, 150], [0.1, 3.5], [0.1, 3.5], [0.05, 0.95], [1, 30], [0.05, 0.5]])
    grid_search_nb_points = [7, 5, 5, 5, 5, 5]  # Optimal would be [12, 8, 5, 5, 5, 5], but it will depends on how much time your machine takes
    has_noise_correction = False

    def __init__(self, param_lim=classic_limits):
        super().__init__(name='SANDIX')
        self.param_lim = param_lim
        self.constraints = [self.constr_on_diffusivities]

    @staticmethod
    def constr_on_diffusivities(param):
        if np.array(param).ndim == 1:
            # Put Di>De
            if param[1] < param[2]:
                # exchange them
                param[1], param[2] = param[2], param[1]
        elif np.array(param).ndim == 2:
            # Put Di>De
            for iset in range(len(param)):
                # if Di < De of the set iset
                if param[iset, 1] < param[iset, 2]:
                    # exchange them
                    param[iset, 1], param[iset, 2] = param[iset, 2], param[iset, 1]
        else:
            raise ValueError('Wrong dimension of parameters')
        return param

    def set_param_lim(self, param_lim):
        self.param_lim = param_lim

    @classmethod
    def get_signal(cls, parameters, acq_parameters):
        """Get signal from single Ground Truth."""
        return sandix_signal_from_vector(parameters, acq_parameters.b, acq_parameters.delta, acq_parameters.small_delta)

    @classmethod
    def get_jacobian(cls, parameters, acq_parameters):
        """Get jacobian from single Ground Truth."""
        return sandix_jacobian_from_vector(parameters, acq_parameters.b, acq_parameters.delta, acq_parameters.small_delta)

    @classmethod
    def get_hessian(cls, parameters, acq_parameters):
        return None

    # Optimized methods for Non-linear Least Squares
    @classmethod
    def get_mse_jacobian(cls, parameters, acq_parameters, signal_gt):
        """Get jacobian of Mean Square Error from single Ground Truth."""
        return sandix_optimized_mse_jacobian(parameters, acq_parameters.b, acq_parameters.delta, acq_parameters.small_delta, 
                                             signal_gt, acq_parameters.ndim)
