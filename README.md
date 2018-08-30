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
- [Quickstart](#quickstart)
  * [Creating Scripts for Managed Nodes](#creating-scripts-for-managed-nodes)
  * [Running the Provisioning Scripts](#running-the-provisioning-scripts)
- [Advanced Topics](#advanced-topics)
  * [Creating Prepared Scripts](#creating-prepared-scripts)
  * [Managing Configuration Files](#managing-configuration-files)
  * [What if...](#what-if)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>



# Requirements

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

## Windows

In order to a Control Machine to use Ansible for controlling a Windows Managed Node, it is necessary to follow some procedures. Mostly of the Windows related are marked as "not stable interface" on Ansible, which means that Windows host monitoring may break due to updates. 

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

After this step ansible can connect to windows machine with not secure `ntlm` configuration. 

# Quickstart

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
