T = readtable('data_for_visualization.csv', 'PreserveVariableNames',true);
x = 14:.1:26; % BridgeAxis
y = 0:.1:11; %TrolleyAxis
[X, Y] = meshgrid(x,y); %// all combinations of x, y
Z = 0;
for i = 1:1:height(T)
    mu = [T.BridgePositionMean(i), T.TrolleyPositionMean(i)];
    sigma = [T.BridgePositionSigma(i) 0; 0 T.TrolleyPositionSigma(i)];
    Z = Z + mvnpdf([X(:) Y(:)],mu,sigma)*T.Weight(i); %// compute Gaussian pdf
end
Z = reshape(Z,size(X)); %// put into same size as X, Y
figure(1)
surf(X,Y,Z)
set ( gca, 'ydir', 'reverse' )
xlabel('BridgePosition(m)') 
ylabel('TrolleyPosition(m)')
figure(2)
contour(Y,X,Z,'LevelList',10:10:200), axis equal
xlabel('TrolleyPosition(m)') 
ylabel('BridgePosition(m)')


