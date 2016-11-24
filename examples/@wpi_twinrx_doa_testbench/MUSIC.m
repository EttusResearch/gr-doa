function [Q_music, theta] = MUSIC(doa_obj, S_x)
% MUSIC is a method belonging to wpi_twinrx_doa_testbench 
% class that implements MUSIC algorithm for DoA estimation. 
% 
% Arguments:
% 
% Required: 
% --------
% S_x           -       Correlation matrix needed for 
%                       MUSIC-based DoA estimation.
% 
% Authors:              Srikanth Pagadarai <srikanth.pagadarai@gmail.com>
%                       Travis F. Collins <travisfcollins@gmail.com>

	num_ss = doa_obj.autocorrelate_params.num_ss;
	geometry = doa_obj.array_params.geometry;
	N = prod(doa_obj.array_params.num_ant_ele);
	num_targets = doa_obj.target_params.num_targets;
	pspectrum_len = doa_obj.pspectrum_len;
	
	if strcmpi(geometry, 'linear')
		theta = 0:180/pspectrum_len:180-180/pspectrum_len;		
	end
	theta = theta*pi/180;
    
	v_ii = zeros(N, pspectrum_len);
	for ii=1:length(theta)     
        	v_ii(:, ii) = doa_obj.manifold_params.amv(theta(ii));    
	end
		
	Q = zeros(pspectrum_len, 1);
	Q_music = zeros(length(theta),num_ss);
	S_x = reshape(S_x, N, num_ss*N);
	for kk = 1:num_ss
		
		% eigenvalues and eigenvectors of S_x
		[eig_vec, ~] = eig(S_x(:, (kk-1)*N+(1:N))); 
		% noise subspace
		U_N = eig_vec(:,1:N-num_targets); 
		U_N_sq = (U_N*U_N');			
        
		for ii=1:length(theta)     
			% v_ii = doa_obj.manifold_params.amv(theta(ii));    
			Q_temp=v_ii(:, ii)'*U_N_sq*v_ii(:, ii);
			
			% (inverse of) null spectrum
			Q(ii)=1/Q_temp; 
		end 
		Q_music(:, kk)=10*log10(Q/max(Q));
	end
end
