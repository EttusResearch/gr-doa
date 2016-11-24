function [S_x, varargout] = music_test_input_gen(doa_obj, varargin)
% music_test_input_gen is a method belonging to wpi_twinrx_doa_testbench 
% class that generates simulated data to be provided as input to 
% MUSIC algorithm for DoA estimation.
% 
% Optional: 
% --------
% snr              -    Signal-to-Noise Ratio
%
% Authors:              Srikanth Pagadarai <srikanth.pagadarai@gmail.com>
%                       Travis F. Collins <travisfcollins@gmail.com>

	narginchk(1, 2);
	optargs = {1000};
	if ~isempty(varargin)
		optargs = varargin; 
	end
	snr = optargs{1};  
    
	num_ss = doa_obj.autocorrelate_params.num_ss;
	len_ss = doa_obj.autocorrelate_params.len_ss;
	overlap_size = doa_obj.autocorrelate_params.overlap_size;
	N = doa_obj.array_params.num_ant_ele;
	PERTURB = doa_obj.array_params.PERTURB; 
	num_targets = doa_obj.target_params.num_targets;
	doas = doa_obj.target_params.doas; 
	amv = doa_obj.manifold_params.amv;	
    
	nonoverlap_size = len_ss-overlap_size;
	% length of the signal
	len_input = nonoverlap_size*num_ss+overlap_size;

	% direction of arrival
	D = doas./180*pi; 
	% digital frequency
	denom = randperm(prod(N));
	w = pi./denom(1:num_targets);
	w = w.';
	
	if PERTURB
		% unknown antenna perturbations to be calibrated
		ant_gain = rand(prod(N), 1);
		ant_phase = exp(-1i*pi*rand(prod(N), 1));
		% reference element
		ant_gain(1) = 1;
		ant_phase(1) = 1;
		ant_pert_vec = ant_gain.*ant_phase;
		ant_pert_mat = diag(ant_pert_vec);

	        % known pilot DoA
        	pilot_doa = 30/180*pi;
	        V_true_pilot = amv(pilot_doa);
		V_pilot = ant_pert_mat*V_true_pilot;
        
        	% pilot's digital frequency
	        w_pilot = pi/3;
        	x_pilot = (V_pilot*exp(1i*w_pilot*(1:len_input))).'; 
	        [S_x_pilot, ~] = autocorrelate(doa_obj, x_pilot);
        	S_x_pilot = reshape(S_x_pilot, prod(N), length(S_x_pilot)/prod(N));
        
	        % This approach is based on 
        	% V. C. Soon, L. Tong, Y. F. Huang and R. Liu, 
	        % "A Subspace Method for Estimating Sensor Gains and Phases," 
        	% in IEEE Transactions on Signal Processing, 
	        % vol. 42, no. 4, pp. 973-976, Apr 1994.
        	ant_pert_est = zeros(prod(N), 1);
	        for kk = 1:num_ss
			% eigenvalues and eigenvectors of S_x
			[eig_vec, ~] = eig(S_x_pilot(:, (kk-1)*prod(N)+(1:prod(N)))); 
			% signal subspace
            		U_S = eig_vec(:,end); 
			U_S_sq = U_S*U_S'; 
            
			W = diag(V_true_pilot)'*U_S_sq*diag(V_true_pilot);
            		[W_eig_vec, W_eig_val] = eig(W);
			[~,I] = sort(diag(W_eig_val));
			W_eig_vec = W_eig_vec(:, I);   
			ant_pert_est = ant_pert_est+W_eig_vec(:, end);
	        end
        	ant_pert_est = ant_pert_est/num_ss;
        
	        fprintf('After antenna calibration, the array coefficients are: \n');
        	disp(ant_pert_vec./ant_pert_est);
	        fprintf('\n');
	end
    
	V_true_targets = zeros(prod(N), length(D)); 
	for k = 1:length(D)
		V_true_targets(:, k) = amv(D(k));
	end    
    
	if PERTURB
		V_targets = ant_pert_mat*V_true_targets;
	        x = (V_targets*exp(1i*w*(1:len_input))).'; 
        	xx = x*diag(1./ant_pert_est);
	else
        	xx = (V_true_targets*exp(1i*w*(1:len_input))).'; 
	end	
    
	% add noise
	SNR_lin = 10^(snr/10);
	sig_En = sum(abs(xx).^2)/len_input;
	N0 = sig_En/SNR_lin;
	N_Sigma = sqrt(N0/2);
	n1 = (randn(len_input, prod(N))+1i*randn(len_input, prod(N)))*diag(N_Sigma);
	xxx1 = xx+n1;
	[S_x, ~] = autocorrelate(doa_obj, xxx1);	

	if PERTURB
		n2 = (randn(len_input, prod(N))+1i*randn(len_input, prod(N)))*diag(N_Sigma);
		xxx2 = x+n2;
        	[S_x_uncalibrated, ~] = autocorrelate(doa_obj, xxx2);	
		varargout{1} = S_x_uncalibrated;
		varargout{2} = ant_pert_vec;
	end

end
