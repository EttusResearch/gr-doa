function [varargout] = doa_testbench_create(operation_to_test, varargin)
% doa_testbench_create instantiates an object of 
% wpi_twinrx_doa_testbench class for DoA estimation 
% based on input parameters passed to it.
% 
% Arguments:
% 
% Required:
% --------
% operation_to_test  -  'autocorrelate_test_input_gen' or 
%                       'music_test_input_gen' or 
%                       'estimate_doa_music'
% 
% Optional: 
% --------
% len_ss             -  length of each snapshot
% overlap_size       -  length of overlap between successive snapshots
% num_inputs         -  number of input streams
% FB                 -  apply Forward-Backward averaging?
% geometry           -  'linear'
% num_ant_ele        -  number of antenna elements
% norm_spacing       -  normalized spacing
% PERTURB            -  simulate array perturbation?
% target_doas        -  simulated directions-of-arrival of targets
% 
% Authors:              Srikanth Pagadarai <srikanth.pagadarai@gmail.com>
%                       Travis F. Collins <travisfcollins@gmail.com>

	narginchk(1, 10); 
	numvarargs = length(varargin);   

	if ~ischar(operation_to_test)
		error('Please enter a block name to test');
	end

	if ~( strcmpi(operation_to_test, 'autocorrelate_test_input_gen') || strcmpi(operation_to_test, 'music_test_input_gen') || strcmpi(operation_to_test, 'estimate_doa_music') || strcmpi(operation_to_test, 'estimate_doa_rootmusic'))
		error('Unknown method of wpi_twinrx_doa_testbench class provided!');
	end

	% parameters are:
	% {len_ss, overlap_size, num_inputs, FB, 
	%  ..., geometry, num_ant_ele, norm_spacing, PERTURB, 
	%  ..., target_doas}
	optargs = {2048, 512, 4, false, 'linear', 4, 0.4, true, 143};
	optargs(1:numvarargs) = varargin;
	% default value of num_ant_ele is num_inputs
	if numvarargs < 5
		optargs{6} = optargs{3};
	end
	
	if (strcmpi(operation_to_test, 'estimate_doa_rootmusic') && ~strcmpi(optargs{5}, 'linear'))
		error('Root-MUSIC algorithm has been implemented to support linear array geometry only!');
	end
	
	if optargs{1} <= optargs{2}
		error('Length of the snapshot has to be greater than the overlap size!');
	end

	if ~strcmpi(optargs{5}, 'linear')
		error('The current implementation of DoA estimation algorithms supports linear array geometries only!');
	end

	if length(optargs{6}) > 2
		error('num_ant_ele needs to be a scalar or a 2-element vector!');
	end

	if length(optargs{9}) >= prod(optargs{6})
    		error('Number of DoAs cannot be larger than the number of antenna array elements!');
	end

	if optargs{3} ~= prod(optargs{6})
    		error('Number of inputs to the autocorrelate block needs to be equal to the number of antenna array elements!');
	end

	if optargs{7} > 0.5    
		error('The selected normalized spacing leads to aliasing!');
	end

	% autocorrelate_params structure 
	if ( strcmpi(operation_to_test, 'autocorrelate_test_input_gen') || strcmpi(operation_to_test, 'music_test_input_gen') )
        	autocorrelate_params.num_ss = 1500; 
	elseif ( strcmpi(operation_to_test, 'estimate_doa_music') || strcmpi(operation_to_test, 'estimate_doa_rootmusic') )
        	autocorrelate_params.num_ss = 100; 
	end
	autocorrelate_params.len_ss = optargs{1};
	autocorrelate_params.overlap_size = optargs{2};
	autocorrelate_params.num_inputs = optargs{3};
	autocorrelate_params.FB = optargs{4};

	% array_params structure 
	array_params.geometry = optargs{5};
	array_params.num_ant_ele = optargs{6};
	array_params.norm_spacing = optargs{7};
	array_params.PERTURB = optargs{8};

	% target_params structure 
	target_params.num_targets = length(optargs{9});
	target_params.doas = optargs{9};

	% create wpi_twinrx_doa_testbench object
	doa_obj = wpi_twinrx_doa_testbench(autocorrelate_params, array_params, target_params);

	if strcmpi(operation_to_test, 'autocorrelate_test_input_gen')
		[S_xx, xx] = doa_obj.autocorrelate();
		varargout{1} = S_xx;  
		varargout{2} = xx;  
	end

	if strcmpi(operation_to_test, 'music_test_input_gen') && ~array_params.PERTURB
		S_xx = doa_obj.music_test_input_gen();
		varargout{1} = S_xx;  
	end

	if strcmpi(operation_to_test, 'music_test_input_gen') && array_params.PERTURB
        	[S_xx, S_x_uncalibrated, ant_pert_vec] = doa_obj.music_test_input_gen();	
		varargout{1} = S_xx;  
        	varargout{2} = S_x_uncalibrated;  
		varargout{3} = ant_pert_vec;  
	end
	
	if strcmpi(operation_to_test, 'estimate_doa_music') 
        	snr = 0;
		S_xx = doa_obj.music_test_input_gen(snr);
		[Q_music, theta] = doa_obj.MUSIC(S_xx);
        	varargout{1} = Q_music;  
		varargout{2} = theta;  
	end
	
	if strcmpi(operation_to_test, 'estimate_doa_rootmusic')
        	snr = 0;
		S_xx = doa_obj.music_test_input_gen(snr);
		DoA = doa_obj.rMUSIC(S_xx);
        	varargout{1} = DoA;  
	end	    
end
