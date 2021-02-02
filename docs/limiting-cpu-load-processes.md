# Limiting the cpu load of processes

```shell
#Limiting the cpu load of services
https://www.tecmint.com/limit-cpu-usage-of-a-process-in-linux-with-cpulimit-tool/
sudo apt install cpulimit

#show processes with htop
top

#20% of a single core max
sudo cpulimit --pid 5087 --limit 20

#Run non-blocking in background
sudo cpulimit --pid 5087 --limit 20 -b

#Kill limiter it if the process dies
sudo cpulimit --pid 17918 --limit 20 --kill --lazy
```
