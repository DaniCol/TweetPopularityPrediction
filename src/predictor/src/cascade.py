import numpy as np


class Cascade:
    
    def __init__(self, cid, time_windows) -> None:
        self.cid = cid
        self.time_windows_list = time_windows

        self.tweet_msg = ''

        self.windows = {}
        self.status = 1  # 1 every thing alright / 0 waiting for partial cascade

    def add_new_window(self, time_window):
        if time_window not in self.windows.keys():
            self.windows[time_window] = {
                'parameters' : {},
                'size': {}
            }

    def compute_w_reel(self, time_window):
        n_star = self.windows[time_window]['parameters']['params']['n_star']
        G1 = self.windows[time_window]['parameters']['params']['G1']
        n_obs = self.windows[time_window]['parameters']['n_obs']
        n_tot = self.windows[time_window]['size']['n_tot']
        if G1==0:
            print("WARNING G1 equals to 0 -> set to 1")
            G1 = 1
        return (n_tot - n_obs) * (1 - n_star) / G1

    def generate_sample_msg(self, time_window):
        msg = {
            'type': 'sample',
            'cid': self.cid,
            'X' : [
                self.windows[time_window]['parameters']['params']['beta'],
                self.windows[time_window]['parameters']['params']['n_star'],
                self.windows[time_window]['parameters']['params']['G1']
            ],
            'W': self.windows[time_window]['size']['W']
        }
        return msg

    def generate_alert_msg(self, time_window):
        msg = {
            'type': 'alert',
            'cid': self.cid,
            'msg': self.tweet_msg,
            'T_obs': time_window,
            'n_tot': self.windows[time_window]['parameters']['n_supp']
        }
        return msg
    
    def generate_stat_msg(self, time_window):
        are = abs(self.windows[time_window]['parameters']['n_supp']-self.windows[time_window]['size']['n_tot']) / \
            self.windows[time_window]['size']['n_tot']
        msg = {
            'type': 'stat',
            'cid': self.cid,
            'T_obs': time_window,
            'ARE': are
        }
        return msg

    def predict(self, time_window, model):
        X = [
                self.windows[time_window]['parameters']['params']['beta'],
                self.windows[time_window]['parameters']['params']['n_star'],
                self.windows[time_window]['parameters']['params']['G1']
            ]
        n_supp = self.windows[time_window]['parameters']['n_obs'] +                 \
                 model.predict(X=np.array(X).reshape(1, -1))[0] *                   \
                 self.windows[time_window]['parameters']['params']['G1'] /          \
                 (1 - self.windows[time_window]['parameters']['params']['n_star'])
        
        self.windows[time_window]['parameters']['n_supp'] = n_supp

    def handle_parameters_type_msg(self, time_window, msg):
        # Add new time window if doesn't exist
        self.add_new_window(time_window=time_window)

        self.windows[time_window]['parameters'] = {
            'n_obs': msg['n_obs'],
            'params': {
                'beta': msg['params'][0],
                'n_star': msg['params'][1],
                'G1': msg['params'][2]
            }
        }

        self.tweet_msg=msg['msg']
    
    def handle_size_type_msg(self, time_window, msg):
        self.add_new_window(time_window=time_window)
        
        self.windows[time_window]['size'] = {
            'n_tot': msg['n_tot'],
            't_end': msg['t_end']
        }

    def publish_sample_and_stat(self, producer):
        for time_window in self.windows.keys():

            self.windows[time_window]['size']['W'] = self.compute_w_reel(time_window)

            sample_msg = self.generate_sample_msg(time_window=time_window)
            producer.send('samples', key = str(time_window), value = sample_msg)

            stat_msg = self.generate_stat_msg(time_window=time_window)
            producer.send('stat', key = str(time_window), value = stat_msg)
    
    def publish_alert(self, producer, time_window):
        alert_msg = self.generate_alert_msg(time_window=time_window)
        producer.send('alert', key = str(time_window), value = alert_msg)

    def clean_memory(self):
        # Check if the cascade is over
        is_finished = True
        for time_window in self.time_windows_list:
            if not (bool(self.windows.get(time_window, {}).get('size', False)) and bool(self.windows.get(time_window, {}).get('parameters', False))):
                is_finished = False
                break
        return is_finished

