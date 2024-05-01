import numpy as np 
import csdl_alpha as csdl

def compute_normal_velocity(velocity, normal_vectors):
    proj = csdl.tensordot(normal_vectors, velocity, ([3], [0]))

    return proj

def compute_induced_velocity(p1, p2, p_eval, gamma=1.):
    r1 = p1-p_eval
    r2 = p2-p_eval
    input_shape = r1.shape
    xyz_dim = len(input_shape) - 1

    r0 = r1-r2
    r1_norm = csdl.norm(r1, axes=(xyz_dim, ))
    r1_norm_exp = csdl.expand(r1_norm, r1.shape, 'ij->ija')
    r2_norm = csdl.norm(r2, axes=(xyz_dim, ))
    r2_norm_exp = csdl.expand(r2_norm, r2.shape, 'ij->ija')

    r1r2_cross = csdl.cross(r1, r2, axis=xyz_dim)
    r1r2_cross_norm = csdl.norm(r1r2_cross, axes=(xyz_dim,))
    r1r2_cross_norm_exp = csdl.expand(r1r2_cross_norm, r1.shape, 'ij->ija')

    term_pre_dot = r0*(r1/r1_norm_exp + r2/r2_norm_exp)

    dot_prod_term = csdl.sum(term_pre_dot, axes=(xyz_dim,))
    dot_prod_term_exp = csdl.expand(dot_prod_term, r0.shape, 'ij->ija')

    induced_vel = gamma/(4*np.pi)*r1r2_cross/(r1r2_cross_norm_exp + 1.e-8)**2 * dot_prod_term_exp


    return induced_vel