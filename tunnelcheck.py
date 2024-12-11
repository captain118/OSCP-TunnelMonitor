import argparse                           
import os           
import platform
import subprocess                     
import time
import socket                                        
 
def is_system_online(host):
    """                                                                                                          
    Checks if a system is online by pinging the host.                                                            
    """                   
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", host]
    try:                                            
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True                                                                                              
    except subprocess.CalledProcessError:                                                                        
        return False
 
def is_port_open(host, port):
    """                               
    Checks if a specific TCP port is open on the host.
    """                                    
    try:     
        with socket.create_connection((host, port), timeout=5):     
            return True                             
    except (socket.timeout, socket.error):
        return False                                                                                             
 
def send_notification(title, message):
    """                                                                                                          
    Sends a desktop notification using 'notify-send'.                                                            
    """
    try:                                                                                                         
        message = "<span fg='#ff0000' color='#57dafd' font='26px'><b>" + message + "</b></span>"
        subprocess.run(["notify-send", "-u", "critical", "-t", "30000", title, message], check=True)                                                                                                                              
    except Exception as e:     
        print(f"Failed to send notification: {e}")                                                               
 
def check_system_status(host, retries=2, port=None):
    """                                                                                                          
    Checks the system status and retries if offline or the port is closed.                    
    Sends a notification if the system or port remains unavailable after retries.                    
    """                       
    online = False
    port_status = False                               
    for attempt in range(retries + 1):
        if port == None:
            online = is_system_online(host)
        else:
            port_status = is_port_open(host, port) if port else True
#        print(f"ICMP {online}, PORT {port_status}")
        if online or port_status:         
            print(f"The system '{host}' is online{' and port ' + str(port) + ' is open' if port else ''}.")      
            return                                      
        else:                         
            print(f"Attempt {attempt + 1}: The system '{host}' is offline or port {port} is closed.")            
            time.sleep(5)  # Wait for 5 seconds before retrying                                                  
 
    # If still offline or port closed after retries, send a notification                                         
    notification_title = "PROXY FAILURE"                                                                         
    notification_message = f"The system '{host}' is offline or port {port} is closed after {retries + 1} attempts."                                                                                                               
    print(notification_message)
    send_notification(notification_title, notification_message)                                                  
 
if __name__ == "__main__":                          
    parser = argparse.ArgumentParser(description="Monitor a system and optionally a specific TCP port.")         
    parser.add_argument("--host", help="The hostname or IP address of the system to monitor.")
    parser.add_argument("--port", type=int, help="The TCP port to monitor (optional).", default=None)
    args = parser.parse_args()
    while True:   
        check_system_status(args.host, port=args.port)
        time.sleep(30) 
