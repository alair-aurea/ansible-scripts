# ansible-scripts

This automates the process of provisioning remote development environments for the Eng. Faster Team.

## Requirements

### Local Machine / Control Machine

1. Ansible (Version 2.4+);
1. SSH client
1. Git

### Remote Machine / Managed Node

1. SSH (linux)
1. Python 2 (version 2.6 or later) or Python 3 (version 3.5 or later)

For windows managed nodes, please check [here](#windows-setup).

## Installation on Control Machines

### Ubuntu 16.04

Run the following commands to install on your home folder.

```
$ sudo apt update
$ sudo apt install ansible openssh-client git python-pip
$ cd ~
$ git clone https://github.com/alair-aurea/ansible-scripts.git
$ cd ~/ansible-scripts
$ pip install -r requirements.txt
```
### Windows

T.B.D.

## Quickstart

The tool have a user interface that guides the user through the configuration process. To run it, just got to the repository root directory and run the python script `run.py`.

After running you should see the following menu:

![Create new Host Menu](figures/create_new_host.png)

To create a new host, just follow the prompts. Check [this video](link) to see an example.

## Example of inventory file

```
[ubuntu-vdi]
10.66.97.200

[ubuntu-vdi:vars]
ansible_connection=ssh 
ansible_ssh_user=ubuntu
ansible_ssh_private_key_file="{{inventory_dir}}/ubuntu-vdi.pem"
ansible_python_interpreter=/usr/bin/python3

[windows-vdi]
10.66.97.49

[windows-vdi:vars]
ansible_connection=winrm 
ansible_winrm_transport=ntlm
ansible_ssh_user=administrator
ansible_winrm_server_cert_validation=ignore
ansible_ssh_pass=ppuROilu&IK=?JgaQFxZ%3OboIUiTHk5

[all:vars]
yourkit_version=2018.04
yourkit_minor=b81

```

There are two entries for each target machine. First, the host (target) connection definitions, like its IP address. Then, the variables, which
define how to setup the connection. If the connection is secured by a SSH key to connect the variable `ansible_ssh_pass` is not required.


## OS Specific Playbooks

For each OS name and major distribution, there are three optional files that may be created:

* `{os-name}\[-major-version\]-pre-tasks.yml`

* `{os-name}\[-major-version\]-packages.yml`

* `{os-name}\[-major-version\]-post-tasks.yml`

Both the `os-version` and `major-version` are printed at the begining of `base.yml` play. Check if the required files exist in the `playbooks` directory.
If they don't exist, they will be skipped as no one is individually required. The major version of the file is optional. Therefore, both 
`Ubuntu-18.04-packages.yml` and `Ubuntu-packages.yml` are valid package list files for the Ubuntu distro. The former takes precedence on the later. 

`*-pre-tasks.yml` provides a list of tasks that must run at the begining of the play and `*-post-tasks.yml` lists define the tasks that must run at the end. They
may include every structure allowed in Playbook tasks. `*-packages.yml` is a list of packages available on the distro repository. The name of the packages may
be different depending on the distro. 

# Current Directory Structure

Currently the project structure has three directories: `files`, `inventory` and `playbooks`. The `files` directory is intended to store the files required to install the tools. It aims at reducing the dependency of external links (see [this](https://github.com/alair-aurea/ansible-scripts/issues/2) issue). The `playbooks` directory holds the playbooks. There are some general playbooks (like `base.yml`) and OS specifc playbooks (like `Ubuntu-packages.yml`). These files define the steps to be reproduced on the host machine. The `inventory` directory holds the inventory files that define the connection information. It also stores some project specific vars. Ideally, the files in these directory are the only that have to be updated when you connect to a new instance, as long as the vdi image and the required tools do not change. The tree bellow shows an example of directory structure.

```
.
├── files
│   └── YourKit-linux
├── inventories
│   ├── amazon-vdi.pem
│   ├── base.inventory
│   └── ubuntu-vdi.pem
├── playbooks
│   ├── Amazon-packages.yml
│   ├── Amazon-post-tasks.yml
│   ├── Amazon-pre-tasks.yml
│   ├── base.yml
│   ├── linux-base.yml
│   ├── Ubuntu-packages.yml
│   ├── Ubuntu-post-tasks.yml
│   ├── Ubuntu-pre-tasks.yml
│   └── windows-base.yml
└── README.md
```

This structure is not following yet the [Ansible Best Practices Guide](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html). This issue will be addressed in the future.

# Windows Setup

In order to a monitor computer to use Ansible for controlling a Windows host, it is necessary to follow some procedures. Mostly of the Windows related
are marked as "not stable interface" on Ansible, which means that Windows host monitoring may break due to updates. 

## Microsoft Windows Prerequisites for Ansible
1) PowerShell 3.0 or newer
2) At least .NET 4.0

    * You can find detailed original post in below link.
      `https://docs.ansible.com/ansible/2.5/user_guide/windows_setup.html`
    * To check your powershell version; `$PSVersionTAble.PSVersion`

3) WinRM listener should be created and activated.

Connect to the VDI Instance and open a PowerShell. Then, execute the following commands:

```
$url = "https://raw.githubusercontent.com/ansible/ansible/devel/examples/scripts/ConfigureRemotingForAnsible.ps1"
$file = "$env:temp\ConfigureRemotingForAnsible.ps1"

(New-Object -TypeName System.Net.WebClient).DownloadFile($url, $file)

powershell.exe -ExecutionPolicy ByPass -File $file
```

After this step ansible can connect to windows machine with not secure `basic` configuration and if more secure connection is preferred you can use example inventory file for `ntlm` connection. Example of inventory files can be seen below.

### Example inventory file for `basic` winrm connection

```
[windows-vdi]
10.66.97.49

[windows-vdi:vars]
ansible_connection=winrm
ansible_winrm_transport=basic
ansible_ssh_user=administrator
ansible_winrm_server_cert_validation=ignore
ansible_ssh_pass=ppuROilu&IK=?JgaQFxZ%3OboIUiTHk5

```
### Example inventory file for `ntlm` winrm connection

```
[windows-vdi]
10.66.97.49

[windows-vdi:vars]
ansible_connection=winrm 
ansible_winrm_transport=ntlm
ansible_ssh_user=administrator
ansible_winrm_server_cert_validation=ignore
ansible_ssh_pass=ppuROilu&IK=?JgaQFxZ%3OboIUiTHk5

```
To get information about the winrm listeners, just run:

```
winrm enumerate winrm/config/Listener
```
