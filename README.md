- [Requirements](#requirements)
  * [Local Machine / Control Machine](#local-machine---control-machine)
  * [Remote Machine / Managed Node](#remote-machine---managed-node)
- [Installation on Control Machines](#installation-on-control-machines)
  * [Ubuntu 16.04](#ubuntu-1604)
  * [Windows](#windows)
  * [Run Using Docker](#run-using-docker)
- [Managed Nodes Setup](#managed-nodes-setup)
  * [Windows](#windows-1)
  * [Microsoft Windows Prerequisites for Ansible](#microsoft-windows-prerequisites-for-ansible)
- [Usage](#usage)
  * [Creating Scripts for Managed Nodes](#creating-scripts-for-managed-nodes)
  * [Running the Provisioning Scripts](#running-the-provisioning-scripts)
- [Advanced Topics](#advanced-topics)
  * [Creating Prepared Scripts](#creating-prepared-scripts)
  * [Managing Configuration Files](#managing-configuration-files)
  * [What if...](#what-if)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>



# Requirements

If you will run `ansible-scripts` from docker, the only requirement is docker. See [here](#run-using-docker).

## Local Machine / Control Machine

1. Ansible (Version 2.4+);
1. SSH client
1. Git

## Remote Machine / Managed Node

1. SSH (linux)
1. Python 2 (version 2.6 or later) or Python 3 (version 3.5 or later)

For windows managed nodes, please check [here](#windows-setup).


# Installation on Control Machines

We provide guides to use `ansible-scripts` on Ubuntu 16.04 and Windows. If you do not want to do the installation but still want to use `ansible-scripts` you can skip to [Run Using Docker](#run-using-docker).

## Ubuntu 16.04

Run the following commands to install `ansible-scripts` on your home folder.

```
$ sudo apt update
$ sudo apt install software-properties-common openssh-client git python-pip
$ sudo apt-add-repository ppa:ansible/ansible
$ sudo apt update
$ sudo apt install ansible
$ cd ~
$ git clone https://github.com/alair-aurea/ansible-scripts.git
$ cd ansible-scripts
$ pip install -r requirements.txt
```
Go to the [Quickstart](#quickstart) section to start using `ansible-scripts`.

## Windows

Windows isn't supported for the control machine. However, there are some workarounds to run `ansible-scripts` if you are on a windows machine. You can use:

1. [Cygwin](https://cygwin.com) ( Recommended )
1. [Docker for Windows](https://docs.docker.com/docker-for-windows/install/) ( Only Windows 10 )
1. VirtualBox or VMWare to virtualize a machine running linux
1. Windows Subsystem for Linux (WSL) \[possibly\] ( also only Windows 10 )

### Installation using Cygwin

To install Cygwin and `ansible-scripts`, follow these steps:

1. Download Cygwin from [http://cygwin.com/setup-x86_64.exe](http://cygwin.com/setup-x86_64.exe); 
1. To install Cygwin and all Ansible dependences, run the following command:
    ```
    setup-x86_64.exe -q --packages=binutils,curl,cygwin32-gcc-g++,gcc-g++,git,gmp,libffi-devel,libgmp-devel,make,nano,openssh,openssl-devel,python-crypto,python-paramiko,python2,python2-devel,python2-openssl,python2-pip,python2-setuptools
    ```
1. Open Cygwin prompt and check which `pip` commando you should use:
    * Run `which pip` and `which pip2`. Do not use the command that gives you something like `cygdrive/c/...`.
1. From Cygwin bash run `pip install ansible` or `pip2 install ansible`, depending on the results of the previous command.
    * This command may take a long time. So, be patient.

## Mac

T.B.D.

## Run Using Docker

A docker image is available to run `ansible-scripts`. If you have docker installed, you just need to create the following tree structure in your home folder:

```
.
├── ansible-data
│   ├── inventories
│   ├── keys
│   └── playbooks
```
Then, just run:

```
docker run -it --rm -v ~/ansible-data/keys:/home/ansible/ansible-scripts/keys -v ~/ansible-data/inventories:/home/ansible/ansible-scripts/inventories -v ~/ansible-data/playbooks:/home/ansible/ansible-scripts/playbooks alairjunior/ansiblescripts
```
Your data will be available in `~/ansible-data` even if you delete the docker container. Check this [video](https://drive.google.com/open?id=1ELdMpqVwhbl_osVwRoyJMmzLhrxvkzrh) to see how it works.

# Managed Nodes Setup

## Linux

To control a Linux node, the only requirements are:

1. Python 2 (version 2.6 or later) or Python 3 (version 3.5 or later)
1. A running ssh server

## Windows

In order to a Control Machine to use Ansible for controlling a Windows Managed Node, it is necessary to follow some procedures. Mostly of the Windows related are marked as "not stable interface" on Ansible, which means that Windows host monitoring may break due to updates. 

### Microsoft Windows Prerequisites for Ansible

1. PowerShell 3.0 or newer
1. At least .NET 4.0

    * You can find detailed original post in below link.
      `https://docs.ansible.com/ansible/2.5/user_guide/windows_setup.html`
    * To check your powershell version; `$PSVersionTAble.PSVersion`

1. WinRM listener should be created and activated.

Connect to the VDI Instance and open a PowerShell. Then, execute the following commands:

```
$url = "https://raw.githubusercontent.com/ansible/ansible/devel/examples/scripts/ConfigureRemotingForAnsible.ps1"
$file = "$env:temp\ConfigureRemotingForAnsible.ps1"

(New-Object -TypeName System.Net.WebClient).DownloadFile($url, $file)

powershell.exe -ExecutionPolicy ByPass -File $file
```

After this step ansible can connect to windows machine with not secure `ntlm` configuration. 

# Usage

The tool have a user interface that guides the user through the configuration process. To run it, just got to the repository root directory and run the python script `run.py`.

## Creating Scripts for Managed Nodes

After running `ansible-scripts` for the first time you should see the following menu:

![Create new Host Menu](figures/create_new_host.png)

To create a new host, just follow the prompts. Check [this video](https://drive.google.com/open?id=1aLZP0MF4ZIiYITmFetV3bA7i_F2oJCU1) to see an example.

## Running the Provisioning Scripts

When a managed node (host) is available, you may run the script from the initial menu. [This video](https://drive.google.com/open?id=1SBDjO8uC4Re0uoLKki-lBdtC_Nsp6mqJ) shows how to do it.

Example of inventory files can be seen below.

# Advanced Topics

## Creating Prepared Scripts

## Managing Configuration Files

## What if...

### ... I am using another linux distribution?

### ... some package is broken on the repository?

### ... I need a tool that is not being installed?

### ... I want to use this to configure Dev environment?

### ... there is a tool in pre / post tasks hat I don't need/want to be installed?

### ... I don't like ansible and prefer \[write here any other scripting language\]
