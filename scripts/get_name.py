from docker import Client
import os

hostname = os.environ['HOSTNAME']

cli = Client(base_url='unix://var/run/docker.sock')
data = cli.containers()

for d in data:
    container_id = d['Id'][:12]
    names = d['Names']
    if container_id == hostname:
        print(names[0])
        quit()

print(hostname)
