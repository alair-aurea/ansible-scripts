# ansible-scripts

Ansible installation scripts for provisioning VDI images for Eng. Faster Team.

# Quickstart

1. Install ansible (version 2.4+)
2. Clone the repository
3. Create an `.inventory` file
4. Execute `ansible-playbook -i file.inventory base.yml`

## Example of inventory file

```
[vdi]
vbox_host ansible_ssh_host=192.168.56.101 vbox_host_alias=vbox_host

[local]
local_host ansible_ssh_host=127.0.0.1 local_host_alias=local_host

[all:vars]
ansible_connection=ssh 
ansible_ssh_user=root
```
