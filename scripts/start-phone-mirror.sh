#Configure wireless
#adb tcpip 5555
#adb connect 192.168.0.107:5555 #(ip address of phone and adb service port)
#scrcpy --bit-rate 2M --max-size 800
snap run scrcpy
#adb usb #switch back to usb mode