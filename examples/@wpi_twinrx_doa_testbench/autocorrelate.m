function [S_x, xx] = autocorrelate(doa_obj, varargin)
% autocorrelate is a method belonging to wpi_twinrx_doa_testbench 
% class that generates the autocorrelation matrix needed for 
% subspace-based DoA estimation. If no input signal is provided, 
% a standard normal random complex matrix is used as input data. 
% 
% Arguments:
% 
% Optional: 
% --------
% in_sig_stream    -    input signal streams
% 
% Authors:              Srikanth Pagadarai <srikanth.pagadarai@gmail.com>
%                       Travis F. Collins <travisfcollins@gmail.com>
	
	narginchk(1, 2);        
	num_ss = doa_obj.autocorrelate_params.num_ss;
	len_ss = doa_obj.autocorrelate_params.len_ss;
	overlap_size = doa_obj.autocorrelate_params.overlap_size;
	num_inputs = doa_obj.autocorrelate_params.num_inputs;
	FB = doa_obj.autocorrelate_params.FB;

	nonoverlap_size = len_ss-overlap_size;
	% length of the signal
	len_input = nonoverlap_size*num_ss+overlap_size;

	% autocorrelate input 
	optargs = {single(randn(len_input, num_inputs))+1i*single(randn(len_input, num_inputs))};
	if ~isempty(varargin)
		optargs = varargin; 
	end
	xx = optargs{1};     

	J = fliplr(eye(num_inputs, num_inputs));
	for ii = 1:num_ss
		x = xx( (ii-1)*nonoverlap_size+(1:len_ss), : );    

		% sample spectral matrix
		S_x(:, (ii-1)*num_inputs+(1:num_inputs)) = transpose(x)*conj(x)/len_ss; 

		if FB
		    S_x(:, (ii-1)*num_inputs+(1:num_inputs)) = ...
			0.5*S_x(:, (ii-1)*num_inputs+(1:num_inputs))...
			+0.5*J*conj(S_x(:, (ii-1)*num_inputs+(1:num_inputs)))*J/len_ss;
		end
	end

	S_x = S_x(:);
end
