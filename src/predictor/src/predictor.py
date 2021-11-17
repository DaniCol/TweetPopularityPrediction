from time import time
from .cascade import Cascade

class BasicEstimator:
    def __init__(self) -> None:
        pass
    def predict(self, X):
        return [1]

class Predictor:
    
    def __init__(self, producer) -> None:
        # Kafka Producer
        self.producer = producer
        # All the trained RF
        self.predictors_collection = {}
        # Cascades 
        self.cascades = {}      


    def handle_model_msg(self, time_window, value):
        # Update the Random Forest
        self.predictors_collection[time_window] = value

    def handle_properties_msg(self, time_window, value):
        # Create the cascade object 
        if value['cid'] not in self.cascades.keys():
            self.cascades[value['cid']] = Cascade(cid=value['cid'])
        
        # Manage Hawkes Estimator messages
        if value['type'] == 'parameters':
            self.cascades[value['cid']].handle_parameters_type_msg(
                time_window=time_window,
                msg=value
            )
            
            self.cascades[value['cid']].predict(
                time_window=time_window,
                model=self.predictors_collection.get(time_window, BasicEstimator())
            )

            alert_msg = self.cascades[value['cid']].generate_alert_msg(time_window=time_window)
            self.producer.send('alert', key = str(time_window), value = alert_msg)

        # Manage Tweet Collector messages  
        elif value['type'] == 'size':
            self.cascades[value['cid']].handle_size_type_msg(
                time_window=time_window,
                msg=value
                )

            sample_msg = self.cascades[value['cid']].generate_sample_msg(time_window=time_window)
            self.producer.send('samples', key = str(time_window), value = sample_msg)

            stat_msg = self.cascades[value['cid']].generate_stat_msg(time_window=time_window)
            self.producer.send('stat', key = str(time_window), value = stat_msg)

            # Check if the cascade is over
            is_finished = True
            for time_window in self.cascades[value['cid']].windows.keys():
                is_finished = is_finished and bool(self.cascades[value['cid']].windows[time_window]['size'])
            
            if is_finished:
                del self.cascades[value['cid']]
