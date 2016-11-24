clc;
clear; 
close all;

% simulated directions of arrival
target_doa = [30, 125]; 
% number of sources 
num_targets = size(target_doa);
% length of each snapshot
len_ss = 256;
% overlap size of each snapshot
overlap_size = 32;
% apply Forward-Backward Averaging?
FB = true;
% normalized_spacing
norm_spacing = 0.3;
% number of array elements
num_ant_ele = 8;
% simulate antenna perturbation?
PERTURB = false;
% pspectrum length
pspectrum_len = 1024;

DoA = doa_testbench_create('estimate_doa_rootmusic', ...
		len_ss, overlap_size, num_ant_ele, FB, ...
		'linear', num_ant_ele, norm_spacing, PERTURB, ...
		target_doa);
		   
fprintf('Displaying the roots obtained for an arbitrary snapshot: %f, %f.\n', DoA(1, 10), DoA(2, 10));