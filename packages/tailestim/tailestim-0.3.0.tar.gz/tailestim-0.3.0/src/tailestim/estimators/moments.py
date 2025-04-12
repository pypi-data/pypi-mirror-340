"""Moments estimator implementation for tail index estimation."""
import numpy as np
from typing import Dict, Any, Tuple, Union
from .result import TailEstimatorResult
from numpy.random import BitGenerator, SeedSequence, RandomState, Generator
from .base import BaseTailEstimator
from .tail_methods import moments_estimator as moments_estimate

class MomentsEstimator(BaseTailEstimator):
    """Moments estimator for tail index estimation.
    
    This class implements the Moments estimator with optional double-bootstrap
    for optimal threshold selection.
    
    Parameters
    ----------
    bootstrap : bool, default=True
        Whether to use double-bootstrap for optimal threshold selection.
    t_bootstrap : float, default=0.5
        Parameter controlling the size of the 2nd bootstrap.
        Defined from n2 = n*(t_bootstrap).
    r_bootstrap : int, default=500
        Number of bootstrap resamplings for the 1st and 2nd bootstraps.
    eps_stop : float, default=0.99
        Parameter controlling range of AMSE minimization.
        Defined as the fraction of order statistics to consider
        during the AMSE minimization step.
    verbose : bool, default=False
        Flag controlling bootstrap verbosity.
    diagn_plots : bool, default=False
        Flag to switch on/off generation of AMSE diagnostic plots.
    base_seed: None | SeedSequence | BitGenerator | Generator | RandomState, default=None
        Base random seed for reproducibility of bootstrap.
    """
    
    def __init__(
        self,
        bootstrap: bool = True,
        t_bootstrap: float = 0.5,
        r_bootstrap: int = 500,
        eps_stop: float = 0.99,
        verbose: bool = False,
        diagn_plots: bool = False,
        base_seed: Union[None, SeedSequence, BitGenerator, Generator, RandomState] = None,
        **kwargs
    ):
        super().__init__(bootstrap=bootstrap, base_seed=base_seed, **kwargs)
        self.t_bootstrap = t_bootstrap
        self.r_bootstrap = r_bootstrap
        self.eps_stop = eps_stop
        self.verbose = verbose
        self.diagn_plots = diagn_plots

    def _estimate(self, ordered_data: np.ndarray) -> Tuple:
        """Estimate tail index using the Moments method.
        
        Parameters
        ----------
        ordered_data : np.ndarray
            Data array in decreasing order.
            
        Returns
        -------
        Tuple
            Contains estimation results from moments_estimator.
        """
        return moments_estimate(
            ordered_data,
            bootstrap=self.bootstrap,
            t_bootstrap=self.t_bootstrap,
            r_bootstrap=self.r_bootstrap,
            verbose=self.verbose,
            diagn_plots=self.diagn_plots,
            eps_stop=self.eps_stop,
            base_seed=self.base_seed
        )

    def get_parameters(self) -> TailEstimatorResult:
        """Get the estimated parameters.
        
        Returns
        -------
        Dict[str, Any]
            Dictionary containing:
            - k_arr: Array of order statistics
            - xi_arr: Array of tail index estimates
            - k_star: Optimal order statistic (if bootstrap=True)
            - xi_star: Optimal tail index estimate (if bootstrap=True)
            - gamma: Power law exponent (if bootstrap=True)
            - bootstrap_results: Bootstrap details (if bootstrap=True)
        """
        if self.results is None:
            raise ValueError("Model not fitted yet. Call fit() first.")
        
        k_arr, xi_arr, k_star, xi_star, x1_arr, n1_amse, k1, max_index1, \
        x2_arr, n2_amse, k2, max_index2 = self.results
        
        params = {
            'k_arr': k_arr,
            'xi_arr': xi_arr,
        }
        
        if self.bootstrap and k_star is not None:
            gamma = float('inf') if xi_star <= 0 else 1 + 1./xi_star
            params.update({
                'k_star': k_star,
                'xi_star': xi_star,
                'gamma': gamma,
                'bootstrap_results': {
                    'first_bootstrap': {
                        'x_arr': x1_arr,
                        'amse': n1_amse,
                        'k_min': k1,
                        'max_index': max_index1
                    },
                    'second_bootstrap': {
                        'x_arr': x2_arr,
                        'amse': n2_amse,
                        'k_min': k2,
                        'max_index': max_index2
                    }
                }
            })
        return TailEstimatorResult(params)