classdef wpi_twinrx_doa_testbench 
% wpi_twinrx_doa_testbench contains the class definition 
% for GNU Octave based simulation of the modules developed 
% for wpi-twinrx-doa project.
% 
% Authors:              Srikanth Pagadarai <srikanth.pagadarai@gmail.com>
%                       Travis F. Collins <travisfcollins@gmail.com>

	properties (Constant = true)
		        
        	% pspectrum_len         length of the Pspeudo-Spectrum
	        pspectrum_len = 1024;
	end

	properties (GetAccess = 'public', SetAccess = 'public')    
        
        	% structure containing autocorrelate parameters. Members:    
	        % num_ss                number of snapshots used in computing 
        	%                       the input's autocorrelation matrix
	        % len_ss                length of each snapshot
        	% overlap_size          length of overlap between successive snapshots
		% num_inputs            number of input streams
	        % FB                    apply Forward-Backward averaging?
        	autocorrelate_params;  
        
	        % structure containing antenna array parameters. Members:      
        	% geometry              linear
	        % num_ant_ele           number of antenna elements
        	% norm_spacing          normalized spacing
	        % PERTURB               simulate array perturbation?
        	array_params;          
        
	        % structure containing target parameters. Members
        	% num_targets        number of targets
	        % doas               directions-of-arrival
        	target_params;
        
	        % structure containing array-manifold parameters. Members
        	% array_loc          array element locations
	        % amv                array-manifold vector        
        	manifold_params;        
        
	end
    
	methods
        	%% constructor for wpi_twinrx_doa_testbench
	        function doa_obj = wpi_twinrx_doa_testbench(autocorrelate_params, array_params, target_params)                   
            
			% autocorrelate_params structure 
			doa_obj.autocorrelate_params = autocorrelate_params;
				
			% array_params structure
			doa_obj.array_params = array_params;
				
			% target_params structure
			doa_obj.target_params = target_params;
		    
			if strcmpi(array_params.geometry, 'linear')
				% Uniform Linear Array
				doa_obj.manifold_params.array_loc = ...
					array_params.norm_spacing*( (array_params.num_ant_ele-1)/2:-1:-(array_params.num_ant_ele-1)/2 )';

				% array-manifold vector
				doa_obj.manifold_params.amv = @(theta) exp(-1i*2*pi*cos(theta)*doa_obj.manifold_params.array_loc);
	
			end	
		end
            
        end        
end
