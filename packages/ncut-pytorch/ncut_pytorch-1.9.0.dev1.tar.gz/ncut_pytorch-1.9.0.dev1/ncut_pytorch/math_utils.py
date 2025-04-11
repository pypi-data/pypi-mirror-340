import torch
import math
import numpy as np

def svd_lowrank(mat, q):
    """
    SVD lowrank
    mat: (n, m), n data, m features
    q: int
    return: (n, q), (q,), (q, m)
    """
    _q = min(q+10, mat.shape[1])  # take 10 extra components to reduce the error, because error in svd_lowrank
    u, s, v = torch.svd_lowrank(mat, q=_q)
    u = u[:, :q]
    s = s[:q]
    v = v[:, :q]
    return u, s, v


def pca_lowrank(mat, q):
    """
    PCA lowrank
    mat: (n, m), n data, m features
    q: int
    return: (n, q), (q,), (q, m)
    """
    u, s, v = svd_lowrank(mat, q)
    _n = mat.shape[0]
    s /= math.sqrt(_n)
    return u @ torch.diag(s) 




def check_if_normalized(x, n=1000):
    """check if the input tensor is normalized (unit norm)"""
    n = min(n, x.shape[0])
    random_indices = torch.randperm(x.shape[0])[:n]
    _x = x[random_indices]
    flag = torch.allclose(torch.norm(_x, dim=-1), torch.ones(n, device=x.device))
    return flag


def quantile_min_max(x, q1=0.01, q2=0.99, n_sample=10000):
    if x.shape[0] > n_sample:
        # random sampling to reduce the load of quantile calculation, torch.quantile does not support large tensor
        np.random.seed(0)
        random_idx = np.random.choice(x.shape[0], n_sample, replace=False)
        vmin, vmax = x[random_idx].quantile(q1), x[random_idx].quantile(q2)
    else:
        vmin, vmax = x.quantile(q1), x.quantile(q2)
    return vmin, vmax


def quantile_normalize(x, q=0.95):
    """normalize each dimension of x to [0, 1], take 95-th percentage, this robust to outliers
        </br> 1. sort x
        </br> 2. take q-th quantile
        </br>     min_value -> (1-q)-th quantile
        </br>     max_value -> q-th quantile
        </br> 3. normalize
        </br> x = (x - min_value) / (max_value - min_value)

    Args:
        x (torch.Tensor): input tensor, shape (n_samples, n_features)
            normalize each feature to 0-1 range
        q (float): quantile, default 0.95

    Returns:
        torch.Tensor: quantile normalized tensor
    """
    # normalize x to 0-1 range, max value is q-th quantile
    # quantile makes the normalization robust to outliers
    if isinstance(x, np.ndarray):
        x = torch.tensor(x)
    vmax, vmin = quantile_min_max(x, q, 1 - q)
    x = (x - vmin) / (vmax - vmin)
    x = x.clamp(0, 1)
    return x
