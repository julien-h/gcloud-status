import pystray
from PIL import Image, ImageDraw
from pathlib import Path
import time
import subprocess
import signal
import os
import sys

# Icons made by <a href="https://www.flaticon.com/free-icon/server_957923" title="Kiranshastry">Kiranshastry</a> from <a href="https://www.flaticon.com/" title="Flaticon"> www.flaticon.com</a>

class Instance:
    possible_states = [
        'PROVISIONING',
        'STAGING',
        'RUNNING',
        'STOPPING',
        'REPAIRING',
        'TERMINATED',
        'UNKNOWN'
    ]

    def __init__(self):
        self.state_ = 'UNKNOWN'

    @property
    def state(self):
        return self.state_

    @state.setter
    def state(self, value):
        if not value in Instance.possible_states:
            raise ValueError(f'Unknown state: "{value}"')
        self.state_ = value

    def query_state(self):
        cmd = r'C:/Windows/Sysnative/bash.exe -c "/home/julien/bin/w-gcloud-status.sh"'
        p = subprocess.run(cmd.split(), capture_output=True)
        print(p)
        try:
            response = p.stdout.decode('utf8')
            self.state = response.strip().split()[-1]
        except ValueError:
            print('Unknown response from gcloud:')
            print(p.stdout)
            self.state = 'UNKNOWN'

    def start(self):
        p = subprocess.run(r'C:/Windows/Sysnative/bash.exe -c "/home/julien/bin/w-gcloud.sh"'.split())
        return p

    def stop(self):
        p = subprocess.run(r'C:/Windows/Sysnative/bash.exe -c "/home/julien/bin/w-gcloud-stop.sh"'.split())
        return p


class Icon:
    def __init__(self):
        self.data_dir = Path(__file__).parent / 'data'
        self.instance = Instance()
        self.remaining_secs = 0
        self.icon = pystray.Icon(
            'gcloud status',
            menu = pystray.Menu(
                pystray.MenuItem(
                    lambda _: f'{self.instance.state}',
                    action = None,
                    enabled = False,
                    visible = True,
                ),
                pystray.MenuItem(
                    'start instance',
                    action=self.start_instance,
                    enabled=lambda _: self.instance.state == 'TERMINATED',
                    ),
                pystray.MenuItem(
                    'stop instance', 
                    action=self.stop_instance,
                    enabled=lambda _: self.instance.state not in ['STOPPING', 'TERMINATED'],
                    ),
                pystray.MenuItem(
                    lambda _: f'update icon ({self.remaining_secs//60}mn{self.remaining_secs%60}s)',
                    action=self.update,
                    default=True,
                )
            ),
        )
        self.update_icon('UNKNOWN')

    def image_path(self, instance_state = 'UNKNOWN'):
        path = self.data_dir / f'{instance_state}.png'
        if path.is_file():
            return path
        else:
            return self.data_dir / 'UNKNOWN.png'

    def run(self):
        try:
            self.icon.visible = True
            self.icon.run(self.status_loop)
        except KeyboardInterrupt:
            print("-- run: keyboard interrupt --")
        except Exception as e:
            print("-- run: exception --")
            print(e)
            print()
        finally:
            icon.stop()
            sys.exit(0)

    def stop(self):
        self.icon.stop()
        sys.exit(0)

    def status_loop(self, icon):
        try:
            print('-- starting status_loop --')
            while True:
                print('-- status_loop: updating icon --')
                self.update()
                #
                self.remaining_secs = 60*60
                self.icon.update_menu()
                while self.remaining_secs > 0:
                    print(f'-- remaining secs: {self.remaining_secs}')
                    time.sleep(60)
                    self.remaining_secs -= 60
                    self.icon.update_menu()
                    
        except Exception as e:
            print('-- exception in status_loop --')
            print(type(e), e)
            print('---')
        finally:
            icon.stop()
            sys.exit(1)

    def update(self):
        self.instance.query_state()
        self.update_icon(self.instance.state)

    def update_icon(self, instance_state):
        path = self.image_path(instance_state)
        self.icon.icon = Image.open(path)
        self.icon.update_menu()
    
    def start_instance(self):
        self.update_icon('UNKNOWN')
        self.instance.start()

    def stop_instance(self):
        self.update_icon('UNKNOWN')
        self.instance.stop()

if __name__=='__main__':
    icon = Icon()
    icon.run()