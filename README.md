# gcloud-status

A system tray icon to display the state of my instance on Google Compute Engine. The icon changes color based on the state of the instance (see the `data/`) folder.

<img src="https://raw.githubusercontent.com/julien-h/gcloud-status/master/data/PROVISIONING.png" width="40px" /> => <img src="https://raw.githubusercontent.com/julien-h/gcloud-status/master/data/RUNNING.png" width="40px" /> => <img src="https://raw.githubusercontent.com/julien-h/gcloud-status/master/data/STOPPING.png" width="40px" /> => <img src="https://raw.githubusercontent.com/julien-h/gcloud-status/master/data/TERMINATED.png" width="40px" style="background:black; background-color:black;"/> (last one is white)

This code is made for my Windows 10 laptop. The `gcloud` client is configured in WSL so I use `subprocess.run` to call it.
