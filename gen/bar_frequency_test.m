 y = randn(10000,1); %Generate large data set
[n,xout] = hist(y,30); %Use 30 bins for the histogram
figure,bar(xout,n/sum(n)); %relative frequency is n/sum(n)
xlabel('Bin locations')
ylabel('Relative frequency')