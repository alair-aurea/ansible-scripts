# ansible-scripts

Ansible installation Playbooks for provisioning VDI images for Eng. Faster Team.

# Quickstart

1. Install ansible (version 2.4+);
2. Clone this repository;
3. Create a new `.inventory` file or add the connection parameters to `base.inventory` in the project's root directory (see bellow);
4. Execute `ansible-playbook -i base.inventory -e HOST=vdi-alair base.yml` or use the `.inventory` file you created. Use the appropriate value
in the `HOST` variable to select the intended host definition.

## Example of inventory file for linux target machine

```
[vdi-alair]
vbox_host ansible_ssh_host=192.168.56.101 vbox_host_alias=vbox_host

[vdi-alair:vars]
ansible_ssh_user=root
ansible_connection=ssh 
```

There are two entries for each target machine. First, the host (target) connection definitions, like its IP address. Then, the variables, which
define how to setup the connection. The above example uses a SSH key to connect. If password is required, include the variable `ansible_ssh_pass`
providing the appropriate password.


