function [data2, pks2, t2_pks] = test002_findpeaks(num_max_vals, vector_len)

pkg load signal; 

t = 2*pi*linspace(0,1,vector_len)';
y = sin(0.25*3.14*t) + 5*sin(6.09*t) + 0.6*cos(1.11*t+1/6) + 2*sin(5.3*t+1/3);

data2 = abs(y);
[all_pks2 all_pks_idx2] = findpeaks(data2);
[pks2_tmp indx2_tmp] = sort(all_pks2,"descend");
pks2 = pks2_tmp(1:num_max_vals);
t2_pks = t(all_pks_idx2(indx2_tmp(1:num_max_vals)));

end