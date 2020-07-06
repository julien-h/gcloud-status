# gcloud-status

A system tray icon to display the state of my instance on Google Compute Engine. The icon changes color based on the state of the instance (see the `data/`) folder.

This code is made for my Windows 10 laptop. The `gcloud` client is configured in WSL so I use `subprocess.run` to call it.
