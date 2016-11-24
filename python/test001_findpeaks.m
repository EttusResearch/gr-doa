function [data1, pks1, t1_pks] = test001_findpeaks(num_max_vals, vector_len)

pkg load signal; 

t = 2*pi*linspace(0,1,vector_len)';
y = sin(3.14*t) + 0.5*cos(6.09*t) + 0.1*sin(10.11*t+1/6) + 0.1*sin(15.3*t+1/3);

data1 = abs(y); 
[all_pks1 all_pks_idx1] = findpeaks(data1);
[pks1_tmp indx1_tmp] = sort(all_pks1,"descend");
pks1 = pks1_tmp(1:num_max_vals);
t1_pks = t(all_pks_idx1(indx1_tmp(1:num_max_vals)));

end
