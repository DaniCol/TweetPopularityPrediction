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
        # Cascades 
        self.cascades = {}      


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
        # Create the cascade object 
        if value['cid'] not in self.cascades.keys():
            self.cascades[value['cid']] = Cascade(cid=value['cid'], producer_log=self.producer_log)
        
        # Manage Hawkes Estimator messages
        if value['type'] == 'parameters':
            self.cascades[value['cid']].handle_parameters_type_msg(
                time_window=time_window,
                msg=value
            )
            # Predict tweet popularity
            self.cascades[value['cid']].predict(
                time_window=time_window,
                model=self.predictors_collection.get(time_window, BasicEstimator())
            )
            # Publish msg on alert topic
            self.cascades[value['cid']].publish_alert(producer=self.producer, time_window=time_window)
            
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
            self.cascades[value['cid']].handle_size_type_msg(
                time_window=time_window,
                msg=value
                )

        if self.cascades[value['cid']].time_windows_list and self.cascades[value['cid']].clean_memory():
            print(self.cascades[value['cid']].time_windows_list)
            # Publish msg_s on sample and stat topics
            self.cascades[value['cid']].publish_sample_and_stat(producer=self.producer)

            # Send log DEBUG : msg send to sample
            self.producer_log.send(
                topic='logs', 
                value={
                    't': time.time(),
                    'level': 'DEBUG',
                    'source': 'predictor',
                    'message': f'Sample sent -> {"{"}Time window : {self.cascades[value["cid"]].time_windows_list}; Cascade : {value["cid"] : >4}{"}"}'
                }
            )

            # Send log DEBUG : msg send to stat
            self.producer_log.send(
                topic='logs', 
                value={
                    't': time.time(),
                    'level': 'DEBUG',
                    'source': 'predictor',
                    'message': f'Stat sent -> {"{"}Time window : {self.cascades[value["cid"]].time_windows_list}; Cascade : {value["cid"] : >4}{"}"}'
                }
            )

            # Free memory by deleting the cascade
            del self.cascades[value['cid']]
