function trigger = find_trigger(filename, channels)
% trigger = find_trigger(filename, channels)
% to find trigger for the input channels
% Input: sqd filename and channels
% Output: triggers for each channels as sample index
% 
% Trigger is from LOW to HIGH.
% 
% example
%       filename= 'C:\awang\MEG\RawData\R0292 ModBand (1.30.04)\R0292.ModBand.1.30.04.Run2.sqd';
%       trigger = find_trigger(filename, [160:171])  

[data, info] = sqdread(filename,'Channels',channels);

threshold = (25-1) / info.InputGain *2;

for iTrigger = 1:length(channels)
    
    % low to high
    trigger(:,iTrigger) = find(diff(data(:,iTrigger)) >  threshold);
    
end