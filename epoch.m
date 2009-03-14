function epochs = epoch(data, triggers, channels)

stimulus_pre  = 100;
stimulus_post = 500;
epoch_length = stimulus_pre + 1 + stimulus_post; % + 1 for the actually stimulus, which occurs at 0

for condition = 1:8,
    epochs{condition} = zeros(epoch_length, 160, 200);  % Preallocate memory. 160 = num. of channels, 200 = num of trials
end

for channel = (channels + 1),
    disp(['Epoching channel ' num2str(channel-1) ' ...'])
    for condition = 1:8, % TODO remove hardcoded 8
        for t = 1:size(triggers(:,condition),1),
            epoch_start = triggers(t,condition)-stimulus_pre;
            epoch_end   = triggers(t,condition)+stimulus_post;
            
            the_epoch = data{channel}(epoch_start:epoch_end);
            
            epochs{condition}(:,channel,t) = the_epoch;
        end
    end
end