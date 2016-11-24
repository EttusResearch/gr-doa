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
norm_spacing = 0.4;
% number of array elements
num_ant_ele = 8;
% simulate antenna perturbation?
PERTURB = false;
% pspectrum length
pspectrum_len = 1024;

[Q_music, theta] = doa_testbench_create('estimate_doa_music', ...
		len_ss, overlap_size, num_ant_ele, FB, ...
		'linear', num_ant_ele, norm_spacing, PERTURB, ...
		target_doa);
		   
% plot the Pseudo-Spectrum for an arbitrary snapshot   
graphics_toolkit ('gnuplot');
figure('Position', [100, 100, 1049, 895]);
plot(theta*180/pi, real(Q_music(:, 50)), '-k', 'Linewidth', 4) 
h1 = title('DOA estimation using MUSIC');
set(h1, 'fontSize', 16);
grid on;
xlim([0 theta(end)*180/pi]);
h2 = xlabel('angle (degrees)');
set(h2, 'fontSize', 16);
h3 = ylabel('Pseudo-Spectrum (dB)') ;
set(h3, 'fontSize', 16);
set(gca, 'fontSize', 16);   
