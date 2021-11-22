import time
from .cascade import Cascade

class BasicEstimator:
    def __init__(self) -> None:
        pass
    def predict(self, X):
        return [1]

class Predictor:
    
    def __init__(self, producer, producer_log) -> None:
        # Kafka Producer
        self.producer = producer
        # Kafka Log Producer
        self.producer_log = producer_log
        # All the trained RF
        self.predictors_collection = {}
        # Time windows
        self.time_windows = {}  


    def handle_model_msg(self, time_window, value):
        # Update the Random Forest
        self.predictors_collection[time_window] = value
        # Send log INFO : RF has been updated
        self.producer_log.send(
            topic='logs',
            value={
                't': time.time(),
                'level': 'INFO',
                'source': 'predictor',
                'message': f'RF has been updated -> {"{"}Time window : {time_window : >5}{"}"}'
            }
        )

    def handle_properties_msg(self, time_window, value):
        # Create the cascade object in specific time window
        try:
            if value['cid'] not in self.time_windows[time_window]:
                self.time_windows[time_window][value['cid']] = Cascade(cid=value['cid'], producer_log=self.producer_log)
        except KeyError:
            self.time_windows[time_window] = {value['cid']: Cascade(cid=value['cid'], producer_log=self.producer_log)}
        
        # Manage Hawkes Estimator messages
        if value['type'] == 'parameters':
            self.time_windows[time_window][value['cid']].handle_parameters_type_msg(
                time_window=time_window,
                msg=value
            )
            # Predict tweet popularity
            self.time_windows[time_window][value['cid']].predict(
                model=self.predictors_collection.get(time_window, BasicEstimator())
            )
            # Publish msg on alert topic
            self.time_windows[time_window][value['cid']].publish_alert(producer=self.producer, time_window=time_window)
            
            # Send log DEBUG : msg send to alert
            self.producer_log.send(
                topic='logs',
                value={
                    't': time.time(),
                    'level': 'DEBUG',
                    'source': 'predictor',
                    'message': f'Alert sent -> {"{"}Time window : {time_window : >5}; Cascade : {value["cid"] : >4}{"}"}'
                }
            )


        # Manage Tweet Collector messages  
        elif value['type'] == 'size':
            self.time_windows[time_window][value['cid']].handle_size_type_msg(
                msg=value
                )

        if self.time_windows[time_window][value['cid']].clean_memory():
            # Publish msg_s on sample and stat topics
            self.time_windows[time_window][value['cid']].publish_sample_and_stat(producer=self.producer)

            # Send log DEBUG : msg send to sample
            self.producer_log.send(
                topic='logs', 
                value={
                    't': time.time(),
                    'level': 'DEBUG',
                    'source': 'predictor',
                    'message': f'Sample sent -> {"{"}Time window : {self.time_windows[time_window][value["cid"]].time_window}; Cascade : {value["cid"] : >4}{"}"}'
                }
            )

            # Send log DEBUG : msg send to stat
            self.producer_log.send(
                topic='logs', 
                value={
                    't': time.time(),
                    'level': 'DEBUG',
                    'source': 'predictor',
                    'message': f'Stat sent -> {"{"}Time window : {self.time_windows[time_window][value["cid"]].time_window}; Cascade : {value["cid"] : >4}{"}"}'
                }
            )

            # Free memory by deleting the cascade
            del self.time_windows[time_window][value["cid"]]
