'''
Created on Mar 27, 2016

@author: Alex
'''

import click
from geometry import Point
import json
from coordination import run_traclus
import os


def main(input_object, 
         #output_file,
         partitioned_trajectories_output_file_name=None,
         clusters_output_file_name=None):
    result = parse_input_and_run_traclus(input_object,
                                         partitioned_trajectories_output_file_name, 
                                         clusters_output_file_name) 
    
    dict_result = map(lambda traj: map(lambda pt: pt.as_dict(), traj), result)
    
    
    return dict_result
    
    

def parse_input_and_run_traclus(input_object,
         partitioned_trajectories_output_file_name=None,
         clusters_output_file_name=None):
    parsed_input = input_object  #or  None
    

        
    for required_param in ['trajectories',
                           'epsilon',
                           'min_neighbors',
                           'min_num_trajectories_in_cluster',
                            'min_vertical_lines',
                            'min_prev_dist']:
        assert parsed_input[required_param], "missing param: " + str(required_param)    
    
    trajs = map(lambda traj: map(lambda pt: Point(**pt), traj), parsed_input['trajectories'])
            
    partitioned_traj_hook = \
    get_dump_partitioned_trajectories_hook(partitioned_trajectories_output_file_name)
        
    clusters_hook = get_dump_clusters_hook(clusters_output_file_name)
        
            
    return run_traclus(point_iterable_list=trajs,
                      epsilon=parsed_input['epsilon'],
                      min_neighbors=parsed_input['min_neighbors'],
                      min_num_trajectories_in_cluster=parsed_input['min_num_trajectories_in_cluster'],
                      min_vertical_lines=parsed_input['min_vertical_lines'],
                      min_prev_dist=parsed_input['min_prev_dist'],
                      partitioned_points_hook=partitioned_traj_hook,
                      clusters_hook=clusters_hook)
    
def get_dump_partitioned_trajectories_hook(file_name):
    if not file_name:
        return None
    
    def func(partitioned_stage_output):
        dict_trajs = map(lambda traj_line_seg: traj_line_seg.line_segment.as_dict(), 
                         partitioned_stage_output)
        with open(get_correct_path_to_file(file_name), 'w') as output:
            output.write(json.dumps(dict_trajs))
    return func

def get_dump_clusters_hook(file_name):
    if not file_name:
        return None
    
    def func(clusters):
        all_cluster_line_segs = []
        for clust in clusters:
            line_segs = clust.get_trajectory_line_segments()
            dict_output = map(lambda traj_line_seg: traj_line_seg.line_segment.as_dict(), 
                              line_segs)
            all_cluster_line_segs.append(dict_output)
            
        with open(get_correct_path_to_file(file_name), 'w') as output:
            output.write(json.dumps(all_cluster_line_segs))
    return func
            
def get_correct_path_to_file(file_name):
    return file_name

