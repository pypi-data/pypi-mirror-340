import numpy as np
from ...models.microstructure_models import MicroStructModel
from .nexi_dot import NexiDot
from .functions.scipy_nexi_dot import nexi_dot_signal_from_vector, \
    nexi_dot_jacobian_concatenated_from_vector, nexi_dot_optimized_mse_jacobian
from ...models.noise.rice_mean import rice_mean, rice_mean_and_jacobian, broad6


class NexiDotRiceMean(MicroStructModel):
    """Neurite Exchange Imaging model ( Narrow Pulse approximation) with an additional dot compartment for diffusion MRI. Corrected for Rician noise."""

    # Class attributes
    n_params = 6
    param_names = ["t_ex", "Di", "De", "f", "f_dot", "sigma"]
    classic_limits = np.array([[1, 150], [0.1, 3.5], [0.1, 3.5], [0.1, 0.9], [0.0, 0.3], [0, 100]])
    grid_search_nb_points = [15, 12, 8, 8, 6]
    has_noise_correction = True
    non_corrected_model = NexiDot()

    def __init__(self, param_lim=classic_limits):
        super().__init__(name='Nexi_Dot_Rice_Mean')
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
        return rice_mean(nexi_dot_signal_from_vector(parameters[:-1], acq_parameters.b, acq_parameters.td), parameters[-1])

    @classmethod
    def get_jacobian(cls, parameters, acq_parameters):
        """Get jacobian from single Ground Truth."""
        nexi_dot_vec_jac_concatenation = nexi_dot_jacobian_concatenated_from_vector(parameters[:-1], acq_parameters.b, acq_parameters.td)
        nexi_dot_signal_vec = nexi_dot_vec_jac_concatenation[..., 0]
        nexi_dot_vec_jac = nexi_dot_vec_jac_concatenation[..., 1:]
        # Turn last parameter jacobian to 0 to avoid updates
        _, nexi_dot_rm_vec_jac = rice_mean_and_jacobian(nexi_dot_signal_vec, parameters[-1], dnu=nexi_dot_vec_jac)
        return nexi_dot_rm_vec_jac

    @classmethod
    def get_hessian(cls, parameters, acq_parameters):
        """Get hessian from single Ground Truth."""
        return None  # KM_dot_vec_hess(parameters, acq_parameters.b, acq_parameters.td)

    # Optimized methods for Non-linear Least Squares
    @classmethod
    def get_mse_jacobian(cls, parameters, acq_parameters, signal_gt):
        """Get jacobian of Mean Square Error from single Ground Truth."""
        nexi_dot_vec_jac_concatenation = nexi_dot_jacobian_concatenated_from_vector(parameters[:-1], acq_parameters.b, acq_parameters.td)
        nexi_dot_signal_vec = nexi_dot_vec_jac_concatenation[..., 0]
        nexi_dot_vec_jac = nexi_dot_vec_jac_concatenation[..., 1:]
        nexi_dot_rm_signal_vec, nexi_dot_rm_vec_jac = rice_mean_and_jacobian(nexi_dot_signal_vec, parameters[-1], dnu=nexi_dot_vec_jac)
        if acq_parameters.ndim == 1:
            mse_jacobian = np.sum(2 * nexi_dot_rm_vec_jac * broad6(nexi_dot_rm_signal_vec - signal_gt), axis=0)
        elif acq_parameters.ndim == 2:
            mse_jacobian = np.sum(2 * nexi_dot_rm_vec_jac * broad6(nexi_dot_rm_signal_vec - signal_gt), axis=(0, 1))
        else:
            raise NotImplementedError
        # Turn last parameter jacobian to 0 to avoid updates
        mse_jacobian[..., -1] = np.zeros_like(mse_jacobian[..., -1])
        return mse_jacobian
