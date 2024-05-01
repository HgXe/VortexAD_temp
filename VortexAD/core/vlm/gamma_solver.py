import numpy as np 
import csdl_alpha as csdl
from VortexAD.core.vlm.fixed_wake_representation import fixed_wake_representation
from VortexAD.core.vlm.setup_linear_system import setup_linear_system

def gamma_solver(num_nodes, mesh_dict, V_inf, alpha):

    mesh_dict = fixed_wake_representation(mesh_dict, V_inf, num_panels=1)
    # mesh dict now has a 'wake_vortex_mesh' key that is used to compute interactions 

    # we want to solve A*\gamma = b, where b = -dot(V_inf, bd_vortex_normal)
    AIC, RHS = setup_linear_system(num_nodes, mesh_dict, V_inf)

    surface_names = list(mesh_dict.keys())
    print(surface_names)
    num_surfaces = len(surface_names)
    print(num_surfaces)
    num_total_panels = 0
    for key in mesh_dict.keys():
        ns, nc = mesh_dict[key]['ns'], mesh_dict[key]['nc']
        num_total_panels += (ns-1)*(nc-1)
    
    gamma_vec = csdl.Variable(shape=(num_nodes, num_total_panels), value=0.)
    for i in csdl.frange(num_nodes):
        gamma_vec = gamma_vec.set(csdl.slice[i,:], value=csdl.solve_linear(AIC[i,:,:], -RHS[i,:]))
    

    # csdl.get_current_recorder().print_graph_structure()

    
    
    


    return gamma_vec