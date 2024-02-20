# NUTPy-Client
This project provides a simple way to shutdown a device based on the information provided by the NUT Server. It supports shutting down the device based on the elapsed time and but also when the battery level crosses a certain threshold. Keep in mind it does NOT wake up the device upon power restore.

## Installation
1. Clone this repository
    ```
    git clone https://github.com/simp16/simple-nut-client.git
    ```
2. Go in to the simple-nut-client folder and modify the configuration file according to your needs:
   ```                                       
    [UPS]
    NUT_HOST = 192.168.1.1 # nut server host
    NUT_PORT = 3493 # nut server port
    NUT_USERNAME = monuser # nut server username
    NUT_PASSWORD = secret # nut server password
    SHUTDOWN_TIME = 600 # shutdown 600 seconds after power loss
    SHUTDOWN_PERCENTAGE = 20 # shutdown after ups battery drops below 20% 
   ```   
3.  After configuration run the installation script with:
    ```
    sudo ./install
    ```
4. Check if the service is running with:
   ```
   sudo systemctl status nutpy-client.service
   ```
## Modifying the configration
You can change the configuration in /etc/nutpy-client/client.conf or by rerunning the installation script. If you modify the script in /etc restart the nutpy-client service with:
```
sudo systemctl restart nutpy-client.service
```
## Removing the nutpy-client
Uninstall the client with this code:
```
sudo ./uninstall
```
