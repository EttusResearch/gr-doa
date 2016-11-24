function DoA = rMUSIC(doa_obj, S_x)
% rMUSIC is a method belonging to wpi_twinrx_doa_testbench 
% class that implements Root-MUSIC algorithm for DoA estimation. 
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
	norm_spacing = doa_obj.array_params.norm_spacing;
	N = prod(doa_obj.array_params.num_ant_ele);
	num_targets = doa_obj.target_params.num_targets;	
	
	S_x = reshape(S_x, N, num_ss*N);
	DoA = zeros(num_targets, num_ss);
	for kk = 1:num_ss
		
		% eigenvalues and eigenvectors of S_x
		[eig_vec, ~] = eig(S_x(:, (kk-1)*N+(1:N))); 
		% noise subspace
		U_N = eig_vec(:,1:N-num_targets); 
		U_N_sq = (U_N*U_N');			
		
		% polynomial vector
		u = zeros(2*(N-1), 1);
		for l = -N+1:1:N-1
			u(l+N) = sum(diag(U_N_sq, l));        
		end
		u = flipud(u);
		
		% roots of the polynomial generated from U_N_sq
		u = u/u(1);
		roots_A = roots(u);
		
		% distance of the roots w.r.t the unit circle
		dist = 1-abs(roots_A);
		
		% find roots which are inside the unit circle     
		ind_outside_unit_circle = find(dist<0);
		roots_A(ind_outside_unit_circle) = [];
		dist(ind_outside_unit_circle) = [];
		
		% of the remaining, find the roots that are closest to the unit circle
		psi_vec = zeros(num_targets, 1);
		for dd = 1:num_targets
			[~, index] = min(dist);
			psi_vec(dd) = roots_A(index);
			roots_A(index) = [];
			dist(index) = [];
		end

		% convert psi to theta and return
		DoA(:, kk) = acos(angle(psi_vec)/(2*pi*norm_spacing))*180/pi;
	end
end
