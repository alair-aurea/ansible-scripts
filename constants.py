#!/usr/bin/python

# directories
INVENTORIES_DIR = 'inventories'
PLAYBOOKS_DIR = 'playbooks'
PREPARED_TASKS_DIR = 'prepared-tasks'
KEY_FILES_DIR = 'keys'
CONFIGS_DIR = 'configs'


# user texts
CREATE_NEW_HOST_TEXT = 'Create new host or overwrite existing host'
SELECT_OR_CREATE_HOST_TEXT = 'Select a predefined host or create a new one'

HOST_IDENTIFICATION_TEXT = "Host Inventory Identification"
HOST_ADDRESS_TEXT = "Hostname or network address"
DEVELOPMENT_ENV_TEXT = "Development Environment"
BASE_OS_TEXT = "Base Operating System"
USERNAME_TEXT = "Username"
USE_KEY_FILE_TEXT = "Use key file for security"
KEY_FILE_TEXT = "Select the key file"
PASSWORD_TEXT = "Password"
FILE_OVERWRITE_TEXT = "Overwrite file"
CONFIRM_FILE_SELECTION_TEXT = "Confirm selection of file"
USE_PREPARATION_TASK_FILE_TEXT = "Use Preparation task file"
USE_POST_INSTALLATION_TASK_FILE_TEXT = "Use Post Installation task file"
PREPARATION_TASK_FILE_TEXT = "Select the preparation tasks file"
POST_INSTALLATION_TASK_FILE_TEXT = "Select the post-installation tasks file"
INSTALL_ADDITIONAL_PACKAGES_TEXT = "Install additional packages available in the repository"
ADDITIONAL_PACKAGES_TEXT = "Package name (this will not be validated by this automation tool)"
PACKAGES_TEXT = "Select packages"
NO_KEY_AVAILABLE = "There is no key available in the 'keys' directory."
SELECT_ACTION = "Select action"
ADD_KEY_AND_RETRY = "Add key and try again"
FALLBACK_TO_PASS = "Fallback to password authentication"
