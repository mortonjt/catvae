import numpy as np
from skbio.stats.composition import alr_inv
from gneiss.cluster import random_linkage
from scipy.stats import ortho_group
from catvae.utils import ilr_inv


def multinomial_bioms(k, D, N, M, min_sv=0.11, max_sv=5.0, sigma_sq=0.1):
    """ Simulates biom tables from multinomial.

    Parameters
    ----------
    k : int
       Number of latent dimensions.
    D : int
       Number of microbes.
    N : int
       Number of samples.
    M : int
       Average sequencing depth.

    Returns
    -------
    dict of np.array
       Ground truth parameters.
    """
    dims, hdims, total = D, k, N
    eigs = min_sv + (max_sv - min_sv) * np.linspace(0, 1, hdims)
    eigvectors = ortho_group.rvs(dims)[:, :hdims]
    W = np.matmul(eigvectors, np.diag(np.sqrt(eigs - sigma_sq)))
    sigma_sq = sigma_sq
    sigma = np.sqrt(sigma_sq)
    z = np.random.normal(size=(total, hdims))
    eta = np.random.normal(np.matmul(z, W.T), sigma).astype(np.float32)
    tree = random_linkage(D)
    Psi = _balance_basis(tree)[0]
    prob = ilr_inv(eta, Psi)
    depths = np.random.poisson(M, size=N)
    Y = np.vstack([np.random.multinomial(depths[i], prob[i])
                   for i in range(N)])
    return dict(
        sigma=sigma,
        W=W,
        Psi=Psi,
        eta=eta,
        z=z,
        Y=Y,
        depths=depths,
        eigs=eigs,
        eigvectors=eigvectors
    )

def normal_bioms(k, D, N, min_sv=0.11, max_sv=5.0, sigma_sq=0.1):
    """ Simulates biom tables from multivariate gaussian.

    Parameters
    ----------
    k : int
       Number of latent dimensions.
    D : int
       Number of microbes.
    N : int
       Number of samples.

    Returns
    -------
    dict of np.array
       Ground truth parameters.
    """
    dims, hdims, total = D, k, N
    eigs = min_sv + (max_sv - min_sv) * np.linspace(0, 1, hdims)
    eigvectors = ortho_group.rvs(dims)[:, :hdims]
    W = np.matmul(eigvectors, np.diag(np.sqrt(eigs - sigma_sq)))
    sigma_sq = sigma_sq
    sigma = np.sqrt(sigma_sq)
    z = np.random.normal(size=(total, hdims))
    x = np.random.normal(np.matmul(z, W.T), sigma).astype(np.float32)

    return dict(
        sigma=sigma,
        W=W,
        x=x,
        z=z,
        eigs=eigs,
        eigvectors=eigvectors
    )
