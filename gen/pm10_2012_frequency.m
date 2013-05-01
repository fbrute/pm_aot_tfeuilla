data = load('aot_pm_daily_2012.txt') ; %Load data
y =data(:,5);
xcenters = 0:5:95;
[n,xout] = hist(y,20,xcenters); %Use 20 bins for the histogram
figure,bar(xout,n/sum(n)); %relative frequency is n/sum(n)
xlabel('Bin locations')
ylabel('Relative frequency')