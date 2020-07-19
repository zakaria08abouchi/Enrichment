def convertToTraj(result_1 , result_2):
    input_objet={"epsilon":0.00016,
                 "min_neighbors":3,
                 "min_num_trajectories_in_cluster":2,
                 "min_vertical_lines":2,
                 "min_prev_dist":0.0002}
    input_objet['trajectories']=[]
    
    traj_1=[]
    traj_2=[]
    for obj in result_1 :
        traj_1.append({'x':obj[3] , 'y':obj[2]})
    for obj in result_2 :
        traj_2.append({'x':obj[3] , 'y':obj[2]})
    
    input_objet['trajectories'].append(traj_1)
    input_objet['trajectories'].append(traj_2)
    return input_objet

