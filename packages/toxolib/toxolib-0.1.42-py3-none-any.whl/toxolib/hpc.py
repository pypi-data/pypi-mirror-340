"""
Module for HPC integration with toxolib
"""
import os
import sys
import logging
import subprocess
import paramiko
import getpass
import tempfile
from pathlib import Path
import yaml
import time
from .abundance_matrix import create_abundance_matrix
from .database import setup_databases, setup_kraken2_db, setup_corn_db
from .session import (
    store_credentials, get_credentials, initialize_session,
    store_connection, get_connection, close_connection
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class HPCConnection:
    """Class to handle HPC connections and job submission"""
    
    def __init__(self, config_file=None, no_persist=False):
        """Initialize HPC connection with configuration
        
        Args:
            config_file (str, optional): Path to HPC configuration file
            no_persist (bool, optional): If True, don't maintain persistent connection
        """
        self.config = {}
        self.ssh = None
        self.sftp = None
        self.no_persist = no_persist
        
        # If config file is provided, load it
        if config_file and os.path.exists(config_file):
            self.load_config(config_file)
        else:
            # Default config file in user's home directory
            default_config = os.path.expanduser("~/.toxolib/hpc_config.yaml")
            if os.path.exists(default_config):
                self.load_config(default_config)
    
    def load_config(self, config_file):
        """Load HPC configuration from YAML file"""
        try:
            with open(config_file, 'r') as f:
                self.config = yaml.safe_load(f)
            logging.info(f"Loaded HPC configuration from {config_file}")
        except Exception as e:
            logging.error(f"Error loading HPC configuration: {e}")
            self.config = {}
    
    def save_config(self, config_file=None):
        """Save HPC configuration to YAML file"""
        if not config_file:
            # Default config file in user's home directory
            config_dir = os.path.expanduser("~/.toxolib")
            os.makedirs(config_dir, exist_ok=True)
            config_file = os.path.join(config_dir, "hpc_config.yaml")
        
        try:
            with open(config_file, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False)
            logging.info(f"Saved HPC configuration to {config_file}")
            return True
        except Exception as e:
            logging.error(f"Error saving HPC configuration: {e}")
            return False
    
    def setup_connection(self, hostname=None, username=None, password=None, key_file=None, use_session=True, persist_connection=True):
        """Set up SSH connection to HPC
        
        Args:
            hostname (str, optional): HPC hostname
            username (str, optional): HPC username
            password (str, optional): HPC password
            key_file (str, optional): Path to SSH key file
            use_session (bool, optional): Whether to use session-based password storage
            persist_connection (bool, optional): Whether to keep the connection open for future commands
            
        Returns:
            bool: True if connection was successful, False otherwise
        """
        # Initialize session for credential and connection storage
        initialize_session()
        
        # Use provided values or get from config
        hostname = hostname or self.config.get('hostname')
        username = username or self.config.get('username')
        key_file = key_file or self.config.get('key_file')
        
        # If any required values are missing, prompt user
        if not hostname:
            hostname = input("Enter HPC hostname: ")
        if not username:
            username = input(f"Enter username for {hostname}: ")
        
        # Update config
        self.config['hostname'] = hostname
        self.config['username'] = username
        
        if key_file and os.path.exists(os.path.expanduser(key_file)):
            self.config['key_file'] = key_file
        
        # Check if we already have a connection in the session
        if persist_connection:
            existing_ssh, existing_sftp = get_connection(hostname, username)
            if existing_ssh and existing_sftp:
                try:
                    # Test if the connection is still active
                    transport = existing_ssh.get_transport()
                    if transport and transport.is_active():
                        # Connection is still active, use it
                        self.ssh = existing_ssh
                        self.sftp = existing_sftp
                        logging.info(f"Using existing connection to {hostname}")
                        return True
                except Exception:
                    # Connection is dead, create a new one
                    pass
        
        # Connect to HPC
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            if key_file and os.path.exists(os.path.expanduser(key_file)):
                # Connect with key file
                self.ssh.connect(
                    hostname=hostname,
                    username=username,
                    key_filename=os.path.expanduser(key_file)
                )
                logging.info(f"Connected to {hostname} using key file")
            else:
                # Try to get password from session first if use_session is enabled
                if use_session and not password:
                    password = get_credentials(hostname, username)
                
                # If no password in session or not using session, prompt for password
                if not password:
                    password = getpass.getpass(f"Enter password for {username}@{hostname}: ")
                    # Store password in session for future use
                    if use_session:
                        store_credentials(hostname, username, password)
                
                self.ssh.connect(
                    hostname=hostname,
                    username=username,
                    password=password
                )
                logging.info(f"Connected to {hostname} using password")
            
            # Create SFTP connection
            self.sftp = self.ssh.open_sftp()
            
            # Test connection
            _, stdout, _ = self.ssh.exec_command("echo 'Connection successful'")
            output = stdout.read().decode().strip()
            
            if output == 'Connection successful':
                logging.info("HPC connection test successful")
                
                # Store connection in session if persist_connection is True
                if persist_connection:
                    store_connection(hostname, username, self.ssh, self.sftp)
                    logging.info(f"Connection to {hostname} will be kept alive for future commands")
                
                return True
            else:
                logging.error("HPC connection test failed")
                return False
                
        except Exception as e:
            logging.error(f"Error connecting to HPC: {e}")
            return False
    
    def close_connection(self, force=False):
        """Close SSH and SFTP connections
        
        Args:
            force (bool): If True, force close the connection even if persistence is enabled
        """
        # By default, we want to keep connections alive unless explicitly forced to close
        # or if the no_persist flag is set
        if not force and not self.no_persist:
            # Log that we're keeping the connection alive
            hostname = self.config.get('hostname')
            if hostname:
                logging.info(f"Connection to {hostname} will be kept alive for future commands")
            return
        
        # If we get here, we should close the connection
        hostname = self.config.get('hostname')
        username = self.config.get('username')
        
        if hostname and username:
            connection_key = f"{username}@{hostname}"
            # Close the connection in the session if it exists
            from .session import close_connection as session_close_connection
            session_close_connection(connection_key)
            logging.info(f"Connection closed: {connection_key}")
            
            # Only clear session credentials if explicitly requested (force=True)
            if force:
                from .session import clear_credentials
                clear_credentials(hostname, username, force=True)
        
        # Close the local connection objects
        if self.sftp:
            try:
                self.sftp.close()
            except Exception as e:
                logging.error(f"Error closing SFTP connection: {e}")
            self.sftp = None
        
        if self.ssh:
            try:
                self.ssh.close()
            except Exception as e:
                logging.error(f"Error closing SSH connection: {e}")
            self.ssh = None
    
    def upload_file(self, local_path, remote_path):
        """Upload a file to HPC"""
        if not self.sftp:
            logging.error("No SFTP connection. Please set up connection first.")
            return False
        
        try:
            # Create remote directory if it doesn't exist
            remote_dir = os.path.dirname(remote_path)
            self.ssh.exec_command(f"mkdir -p {remote_dir}")
            
            # Upload file
            self.sftp.put(local_path, remote_path)
            logging.info(f"Uploaded {local_path} to {remote_path}")
            return True
        except Exception as e:
            logging.error(f"Error uploading file: {e}")
            return False
    
    def download_file(self, remote_path, local_path):
        """Download a file from HPC"""
        if not self.sftp:
            logging.error("No SFTP connection. Please set up connection first.")
            return False
        
        try:
            # Create local directory if it doesn't exist
            local_dir = os.path.dirname(local_path)
            os.makedirs(local_dir, exist_ok=True)
            
            # Download file
            self.sftp.get(remote_path, local_path)
            logging.info(f"Downloaded {remote_path} to {local_path}")
            return True
        except Exception as e:
            logging.error(f"Error downloading file: {e}")
            return False
    
    def execute_command(self, command):
        """Execute a command on HPC"""
        if not self.ssh:
            logging.error("No SSH connection. Please set up connection first.")
            return None
        
        try:
            # Execute command
            _, stdout, stderr = self.ssh.exec_command(command)
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            
            if error:
                logging.warning(f"Command execution warning: {error}")
            
            return output
        except Exception as e:
            logging.error(f"Error executing command: {e}")
            return None
    
    def check_file_exists(self, remote_path):
        """Check if a file exists on HPC"""
        if not self.ssh:
            logging.error("No SSH connection. Please set up connection first.")
            return False
        
        try:
            # Check if file exists
            _, stdout, _ = self.ssh.exec_command(f"test -f {remote_path} && echo 'exists'")
            output = stdout.read().decode().strip()
            
            return output == 'exists'
        except Exception as e:
            logging.error(f"Error checking file existence: {e}")
            return False
    
    def submit_job(self, job_script_path, job_name=None):
        """Submit a job to HPC using sbatch"""
        if not self.ssh:
            logging.error("No SSH connection. Please set up connection first.")
            return None
        
        try:
            # Submit job
            job_name_arg = f"-J {job_name}" if job_name else ""
            _, stdout, stderr = self.ssh.exec_command(f"sbatch {job_name_arg} {job_script_path}")
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            
            if error:
                logging.error(f"Job submission error: {error}")
                return None
            
            # Extract job ID from output (e.g., "Submitted batch job 123456")
            if "Submitted batch job" in output:
                job_id = output.split()[-1]
                logging.info(f"Job submitted with ID: {job_id}")
                return job_id
            else:
                logging.error(f"Unexpected job submission output: {output}")
                return None
        except Exception as e:
            logging.error(f"Error submitting job: {e}")
            return None
    
    def check_job_status(self, job_id):
        """Check the status of a job on HPC"""
        if not self.ssh:
            logging.error("No SSH connection. Please set up connection first.")
            return None
        
        try:
            # Check job status
            _, stdout, _ = self.ssh.exec_command(f"sacct -j {job_id} --format=State --noheader | head -1")
            status = stdout.read().decode().strip()
            
            if status:
                logging.info(f"Job {job_id} status: {status}")
                return status
            else:
                logging.warning(f"No status found for job {job_id}")
                return None
        except Exception as e:
            logging.error(f"Error checking job status: {e}")
            return None
    
    def wait_for_job_completion(self, job_id, check_interval=60, timeout=None):
        """Wait for a job to complete on HPC"""
        if not self.ssh:
            logging.error("No SSH connection. Please set up connection first.")
            return False
        
        start_time = time.time()
        logging.info(f"Waiting for job {job_id} to complete...")
        
        while True:
            # Check if timeout has been reached
            if timeout and (time.time() - start_time) > timeout:
                logging.error(f"Timeout waiting for job {job_id} to complete")
                return False
            
            # Check job status
            status = self.check_job_status(job_id)
            
            if status in ['COMPLETED']:
                logging.info(f"Job {job_id} completed successfully")
                return True
            elif status in ['FAILED', 'CANCELLED', 'TIMEOUT', 'NODE_FAIL']:
                logging.error(f"Job {job_id} failed with status: {status}")
                return False
            elif status in ['RUNNING', 'PENDING', 'CONFIGURING']:
                # Job still running, wait and check again
                logging.info(f"Job {job_id} is {status}. Checking again in {check_interval} seconds...")
                time.sleep(check_interval)
            else:
                logging.warning(f"Unknown job status: {status}. Checking again in {check_interval} seconds...")
                time.sleep(check_interval)
                
    def get_current_directory(self):
        """Get the current working directory on the HPC"""
        if not self.ssh:
            logging.error("No SSH connection. Please set up connection first.")
            return None
        
        try:
            # Execute pwd command to get current directory
            _, stdout, _ = self.ssh.exec_command("pwd")
            current_dir = stdout.read().decode().strip()
            
            logging.info(f"Current HPC working directory: {current_dir}")
            return current_dir
        except Exception as e:
            logging.error(f"Error getting current directory: {e}")
            return None
    
    def create_directory(self, directory_path, parents=True):
        """Create a new directory on the HPC
        
        Args:
            directory_path (str): Path of the directory to create
            parents (bool): If True, create parent directories as needed
        
        Returns:
            bool: True if directory was created successfully, False otherwise
        """
        if not self.ssh:
            logging.error("No SSH connection. Please set up connection first.")
            return False
        
        try:
            # Create directory with or without parents
            if parents:
                command = f"mkdir -p {directory_path}"
            else:
                command = f"mkdir {directory_path}"
                
            _, stdout, stderr = self.ssh.exec_command(command)
            error = stderr.read().decode().strip()
            
            if error:
                logging.error(f"Error creating directory: {error}")
                return False
            
            # Verify directory was created
            _, stdout, _ = self.ssh.exec_command(f"test -d {directory_path} && echo 'exists'")
            output = stdout.read().decode().strip()
            
            if output == 'exists':
                logging.info(f"Directory created successfully: {directory_path}")
                return True
            else:
                logging.error(f"Failed to create directory: {directory_path}")
                return False
        except Exception as e:
            logging.error(f"Error creating directory: {e}")
            return False
            
    def change_directory(self, directory_path):
        """Change the current working directory on the HPC
        
        Args:
            directory_path (str): Path to change to. Use '..' to go up one level.
        
        Returns:
            str: New current directory path if successful, None otherwise
        """
        if not self.ssh:
            logging.error("No SSH connection. Please set up connection first.")
            return None
        
        try:
            # First check if the directory exists
            _, stdout, stderr = self.ssh.exec_command(f"test -d {directory_path} && echo 'exists'")
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            
            if output != 'exists':
                logging.error(f"Directory does not exist: {directory_path}")
                return None
                
            # Change directory and get new path
            # Note: Since SSH commands are stateless, we need to use a workaround
            # to simulate changing directories by executing commands in the target directory
            _, stdout, _ = self.ssh.exec_command(f"cd {directory_path} && pwd")
            new_dir = stdout.read().decode().strip()
            
            if new_dir:
                logging.info(f"Changed directory to: {new_dir}")
                return new_dir
            else:
                logging.error(f"Failed to change directory to: {directory_path}")
                return None
        except Exception as e:
            logging.error(f"Error changing directory: {e}")
            return None
    
    def list_directory(self, directory_path=None, long_format=False, show_hidden=False):
        """List files and directories in the specified or current directory on the HPC
        
        Args:
            directory_path (str, optional): Path to list. If None, lists the current directory.
            long_format (bool): If True, use long listing format (like ls -l)
            show_hidden (bool): If True, show hidden files (starting with .)
        
        Returns:
            list: List of files/directories if successful, None otherwise
        """
        if not self.ssh:
            logging.error("No SSH connection. Please set up connection first.")
            return None
        
        try:
            # Build ls command with options
            ls_cmd = "ls"
            if long_format:
                ls_cmd += " -l"
            if show_hidden:
                ls_cmd += " -a"
                
            # Add directory path if specified
            if directory_path:
                ls_cmd += f" {directory_path}"
                
            # Execute ls command
            _, stdout, stderr = self.ssh.exec_command(ls_cmd)
            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()
            
            if error:
                logging.error(f"Error listing directory: {error}")
                return None
                
            # Split output into lines and return as list
            files = output.split('\n') if output else []
            return files
        except Exception as e:
            logging.error(f"Error listing directory: {e}")
            return None
            
    # Interactive shell functionality removed to simplify the HPC workflow
            
    # Help text for interactive shell removed to simplify the HPC workflow

def generate_job_script(snakemake_file, output_dir, kraken_db_dir, corn_db_dir, job_name="toxolib_job", partition="normal", threads=32, memory=200, time="144:00:00", raw_data_dir=None):
    """Generate a SLURM job script for running Snakemake on HPC with enhanced logging and offline support
    
    Args:
        snakemake_file (str): Path to the Snakemake file on HPC
        output_dir (str): Output directory on HPC
        kraken_db_dir (str): Path to the Kraken2 database directory on HPC
        corn_db_dir (str): Path to the corn database directory on HPC
        job_name (str): Name of the job
        partition (str): SLURM partition to use
        threads (int): Number of CPU threads to request
        memory (int): Memory in GB to request
        time (str): Time limit for the job in format HH:MM:SS
        raw_data_dir (str, optional): Path to the raw data directory on HPC
    """
    script = f"""#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --output={output_dir}/logs/{job_name}_%j.out
#SBATCH --error={output_dir}/logs/{job_name}_%j.err
#SBATCH --time={time}
#SBATCH --ntasks=1
#SBATCH --cpus-per-task={threads}
#SBATCH --mem={memory}G
#SBATCH --partition={partition}
#SBATCH --mail-type=END,FAIL

# Enhanced logging setup
LOG_DIR="{output_dir}/logs"
DEBUG_LOG="$LOG_DIR/debug_${{SLURM_JOB_ID}}.log"
SNAKEMAKE_LOG="$LOG_DIR/snakemake_${{SLURM_JOB_ID}}.log"

# Function to log with timestamp
log_message() {{
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$DEBUG_LOG"
}}

# Create output directories
mkdir -p {output_dir}/logs
touch "$DEBUG_LOG"
log_message "Created logs directory at {output_dir}/logs"

# Log system information
log_message "========== TOXOLIB JOB STARTED =========="
log_message "Job ID: $SLURM_JOB_ID"
log_message "Job Name: {job_name}"
log_message "Working Directory: $(pwd)"
log_message "Output Directory: {output_dir}"
log_message "Snakemake File: {snakemake_file}"
log_message "Hostname: $(hostname)"
log_message "CPU Cores: {threads}"
log_message "Memory: {memory}G"

# Check if required directories exist
log_message "Checking required directories..."
if [ ! -f "{snakemake_file}" ]; then
    log_message "ERROR: Snakemake file not found: {snakemake_file}"
    exit 1
fi

# Check for Raw_Data directory and files
log_message "Checking Raw_Data directory..."
OUTPUT_PARENT_DIR=$(dirname "{output_dir}")
RAW_DATA_DIR="$OUTPUT_PARENT_DIR/Raw_Data"
log_message "Looking for Raw_Data directory at: $RAW_DATA_DIR"
if [ ! -d "$RAW_DATA_DIR" ]; then
    log_message "ERROR: Raw_Data directory not found: $RAW_DATA_DIR"
    exit 1
fi

# Check if raw data files exist in the Raw_Data directory
log_message "Checking for raw data files in Raw_Data directory..."
RAW_FILES_COUNT=$(find "$RAW_DATA_DIR" -name "*.fastq.gz" | wc -l)
log_message "Found $RAW_FILES_COUNT raw data files in $RAW_DATA_DIR"
if [ "$RAW_FILES_COUNT" -eq 0 ]; then
    log_message "ERROR: No raw data files (*.fastq.gz) found in $RAW_DATA_DIR"
    log_message "Files in Raw_Data directory:"
    ls -la "$RAW_DATA_DIR" >> "$DEBUG_LOG"
    exit 1
fi

# Check if Kraken2_DB directory exists
log_message "Checking Kraken2_DB directory..."
KRAKEN2_DB_DIR="{kraken_db_dir}"
log_message "Looking for Kraken2_DB directory at: $KRAKEN2_DB_DIR"
if [ ! -d "$KRAKEN2_DB_DIR" ]; then
    log_message "ERROR: Kraken2_DB directory not found: $KRAKEN2_DB_DIR"
    exit 1
fi

# Check if corn_db directory exists
log_message "Checking corn_db directory..."
CORN_DB_DIR="{corn_db_dir}"
log_message "Looking for corn_db directory at: $CORN_DB_DIR"
if [ ! -d "$CORN_DB_DIR" ]; then
    log_message "ERROR: corn_db directory not found: $CORN_DB_DIR"
    exit 1
fi

log_message "Listing files in Raw_Data directory:"
ls -la "$RAW_DATA_DIR" >> "$DEBUG_LOG"

# Set up conda environment - try multiple approaches
log_message "Setting up conda environment..."

# Check for internet connectivity first
# Use a safer approach that won't fail the script if ping fails
if ping -c 1 -W 2 8.8.8.8 &>/dev/null || ping -c 1 -W 2 1.1.1.1 &>/dev/null; then
    log_message "Internet connection available"
    OFFLINE_MODE=false
else
    log_message "OFFLINE MODE: No internet connection detected"
    OFFLINE_MODE=true
fi

# First try: Use module if specified
if command -v module &> /dev/null; then
    log_message "Trying to load anaconda3 module..."
    module load anaconda3 || log_message "Module anaconda3 not available, trying alternatives"
    
    # Try other common module names for Python environments
    if ! command -v conda &> /dev/null; then
        log_message "Trying alternative modules..."
        module load python || module load python3 || module load miniconda3 || true
    fi
fi

# Second try: Check if conda is already in PATH
if ! command -v conda &> /dev/null; then
    log_message "Conda not found in PATH, checking for Miniconda installation"
    
    # Third try: Check for existing Miniconda installation
    if [ -d "$HOME/miniconda3/bin" ]; then
        log_message "Found existing Miniconda installation"
        export PATH="$HOME/miniconda3/bin:$PATH"
        
        # Initialize conda properly
        log_message "Initializing conda..."
        eval "$($HOME/miniconda3/bin/conda shell.bash hook)"
    else
        log_message "WARNING: No conda installation found."
        log_message "Using system Python instead."
        
        # Check if Python is available
        if command -v python3 &> /dev/null; then
            log_message "Using system Python: $(which python3) $(python3 --version 2>&1)"
        elif command -v python &> /dev/null; then
            log_message "Using system Python: $(which python) $(python --version 2>&1)"
        else
            log_message "ERROR: No Python installation found. Exiting."
            exit 1
        fi
    fi
fi

# Verify conda is available
if command -v conda &> /dev/null; then
    log_message "Using conda from: $(which conda)"
    log_message "Conda version: $(conda --version)"
    
    # Make sure conda is properly initialized for this script
    log_message "Initializing conda for this script..."
    eval "$(conda shell.bash hook)"
    conda info &>/dev/null || log_message "WARNING: Conda initialization may not be complete"
fi

# Set output directory variable for shell script
OUTPUT_DIR="{output_dir}"

# Check if we have conda available
if command -v conda &> /dev/null; then
    # Check for taxonomy_env.yaml first, then fall back to environment.yml
    if [ -f "$OUTPUT_DIR/taxonomy_env.yaml" ]; then
        ENV_FILE="$OUTPUT_DIR/taxonomy_env.yaml"
        ENV_NAME="toxo_env"
    else
        ENV_FILE="$OUTPUT_DIR/environment.yml"
        ENV_NAME="toxolib_env"
    fi

    log_message "Using environment file: $ENV_FILE"
    log_message "Environment name: $ENV_NAME"

    # Try to create conda environment if it doesn't exist
    if ! conda env list | grep -q "$ENV_NAME"; then
        log_message "Creating conda environment $ENV_NAME..."
        
        # First try to create environment normally
        conda env create -f "$ENV_FILE" -n "$ENV_NAME" 2>&1 | tee -a "$DEBUG_LOG"
        
        # If that fails, try to create a minimal environment and install packages manually
        if [ $? -ne 0 ]; then
            log_message "WARNING: Failed to create environment from file. Creating minimal environment..."
            conda create -y -n "$ENV_NAME" python=3.9 2>&1 | tee -a "$DEBUG_LOG"
            
            if [ $? -ne 0 ]; then
                log_message "ERROR: Failed to create minimal conda environment. Compute node may not have internet access."
                log_message "Will try to use system Python instead."
            else
                log_message "Minimal conda environment created successfully"
            fi
        else
            log_message "Conda environment created successfully"
        fi
    else
        log_message "Using existing conda environment"
    fi

    # Activate conda environment
    log_message "Activating conda environment $ENV_NAME..."
    source "$(conda info --base)/etc/profile.d/conda.sh" 2>/dev/null || true
    conda activate "$ENV_NAME" 2>&1 | tee -a "$DEBUG_LOG" || log_message "WARNING: Failed to activate conda environment. Using system Python instead."
    
    # Verify Python is available
    if command -v python &> /dev/null; then
        log_message "Using Python: $(which python)"
        log_message "Python version: $(python --version 2>&1)"
    else
        log_message "ERROR: No Python available after environment activation. Using system Python."
        if command -v python3 &> /dev/null; then
            log_message "Using system Python: $(which python3)"
        elif command -v python &> /dev/null; then
            log_message "Using system Python: $(which python)"
        else
            log_message "ERROR: No Python installation found. Exiting."
            exit 1
        fi
    fi
else
    # No conda available, use system Python
    log_message "No conda available. Using system Python."
    if command -v python3 &> /dev/null; then
        log_message "Using system Python: $(which python3) $(python3 --version 2>&1)"
    elif command -v python &> /dev/null; then
        log_message "Using system Python: $(which python) $(python --version 2>&1)"
    else
        log_message "ERROR: No Python installation found. Exiting."
        exit 1
    fi
fi

# Check if environment was activated successfully
if [ $? -ne 0 ]; then
    log_message "ERROR: Failed to activate conda environment"
    exit 1
fi

# Log environment details
log_message "Using Python: $(which python)"
log_message "Python version: $(python --version 2>&1)"

# Check for snakemake and handle offline mode
if command -v snakemake &> /dev/null; then
    log_message "Snakemake found: $(which snakemake)"
    SNAKEMAKE_CMD="snakemake"
else
    log_message "Snakemake command not found in PATH"
    
    # Check if we can find the snakemake module directly
    if python -c "import snakemake" 2>/dev/null; then
        log_message "Snakemake module found, will use python -m snakemake"
        SNAKEMAKE_CMD="python -m snakemake"
    else
        # In offline mode, we'll try to run the workflow directly without snakemake
        log_message "OFFLINE MODE: Snakemake not available. Will attempt to run workflow directly."
        
        # Create a simple function to run the workflow steps directly
        cat > "$OUTPUT_DIR/run_workflow.py" << 'EOF'
#!/usr/bin/env python
import os
import sys
import subprocess
import glob

def run_command(command_str):
    print(f"Running: {command_str}")
    subprocess.run(command_str, shell=True, check=True)

def main():
    # Get input files from Snakefile directory
    input_files = glob.glob(os.path.join(os.environ.get("RAW_DATA_DIR", "Raw_Data"), "*.fastq.gz"))
    if not input_files:
        print("ERROR: No input FASTQ files found")
        sys.exit(1)
    
    # Get database paths from environment variables
    kraken_db = os.environ.get("KRAKEN2_DB_DIR", "")
    corn_db = os.environ.get("CORN_DB_DIR", "")
    
    if not kraken_db or not corn_db:
        print("ERROR: Database paths not set")
        sys.exit(1)
    
    # Run kraken2 directly on each input file
    for input_file in input_files:
        base_name = os.path.basename(input_file).split(".")[0]
        output_file = f"kraken_output/{base_name}.kraken"
        report_file = f"kraken_output/{base_name}.report"
        
        os.makedirs("kraken_output", exist_ok=True)
        
        threads = os.environ.get("SLURM_CPUS_PER_TASK", "1")
        kraken_command = f"kraken2 --db {kraken_db} --threads {threads} "
        kraken_command += f"--output {output_file} --report {report_file} {input_file}"
        
        try:
            print(f"Processing {input_file}...")
            run_command(kraken_command)
            print(f"Successfully processed {input_file}")
        except subprocess.CalledProcessError as e:
            print(f"WARNING: kraken2 failed for {input_file} with error: {e}")

# Create abundance matrix
def create_matrix():
    try:
        print("Creating abundance matrix...")
        
        # Get database paths from environment variables
        corn_db = os.environ.get("CORN_DB_DIR", "")
        if not corn_db:
            print("ERROR: CORN_DB_DIR environment variable not set")
            sys.exit(1)
            
        # Try to import the module directly
        try:
            # Add current directory to path to find module
            sys.path.append(os.getcwd())
            from create_abundance_matrix import create_abundance_matrix
            create_abundance_matrix("kraken_output", "abundance_matrix.tsv", corn_db)
        except ImportError:
            # Fall back to command line if module import fails
            print("Module not found, running script directly")
            command = f"python create_abundance_matrix.py kraken_output abundance_matrix.tsv {corn_db}"
            print(f"Running: {command}")
            subprocess.run(command, shell=True, check=True)
            
        print("Abundance matrix created successfully")
    except Exception as e:
        print(f"Error creating abundance matrix: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
    create_matrix()
EOF
        chmod +x "$OUTPUT_DIR/run_workflow.py"
        SNAKEMAKE_CMD="python $OUTPUT_DIR/run_workflow.py"
    fi
fi

log_message "Using workflow command: $SNAKEMAKE_CMD"

# Export environment variables for the direct workflow runner
export KRAKEN2_DB_DIR="{kraken_db_dir}"
export CORN_DB_DIR="{corn_db_dir}"
export RAW_DATA_DIR="{raw_data_dir or '$OUTPUT_PARENT_DIR/Raw_Data'}"

# Check for database directories
log_message "Checking database directories..."
log_message "KRAKEN2_DB_DIR=$KRAKEN2_DB_DIR"
log_message "CORN_DB_DIR=$CORN_DB_DIR"
log_message "RAW_DATA_DIR=$RAW_DATA_DIR"

# Run Snakemake with detailed logging
log_message "Changing to Snakemake directory: $(dirname {snakemake_file})"
cd $(dirname {snakemake_file})

log_message "Starting workflow..."
if [[ "$SNAKEMAKE_CMD" == "snakemake" || "$SNAKEMAKE_CMD" == "python -m snakemake" ]]; then
    log_message "Running Snakemake: $SNAKEMAKE_CMD -s {os.path.basename(snakemake_file)} --cores $SLURM_CPUS_PER_TASK --verbose"
    $SNAKEMAKE_CMD -s {os.path.basename(snakemake_file)} --cores $SLURM_CPUS_PER_TASK --verbose 2>&1 | tee -a "$DEBUG_LOG"
else
    log_message "Running direct workflow: $SNAKEMAKE_CMD"
    $SNAKEMAKE_CMD 2>&1 | tee -a "$DEBUG_LOG"
fi

# Run the workflow using the appropriate command
if [[ "$SNAKEMAKE_CMD" == "snakemake" || "$SNAKEMAKE_CMD" == "python -m snakemake" ]]; then
    $SNAKEMAKE_CMD -s {os.path.basename(snakemake_file)} --cores $SLURM_CPUS_PER_TASK --verbose 2>&1 | tee -a "$SNAKEMAKE_LOG"
else
    $SNAKEMAKE_CMD 2>&1 | tee -a "$SNAKEMAKE_LOG"
fi
SNAKEMAKE_EXIT_CODE=$?

# Check if job completed successfully
if [ $SNAKEMAKE_EXIT_CODE -eq 0 ]; then
    log_message "Snakemake workflow completed successfully"
    
    # Create a summary of the output files
    log_message "Creating output summary..."
    find {output_dir} -type f -name "*.csv" -o -name "*.html" | sort >> "$DEBUG_LOG"
    
    log_message "========== TOXOLIB JOB COMPLETED SUCCESSFULLY =========="
    exit 0
else
    log_message "ERROR: Snakemake workflow failed with exit code $SNAKEMAKE_EXIT_CODE"
    log_message "Check the Snakemake log for details: $SNAKEMAKE_LOG"
    
    # Collect additional debug information
    log_message "Collecting debug information..."
    log_message "Disk space:" 
    df -h >> "$DEBUG_LOG"
    
    log_message "Memory usage:"
    free -h >> "$DEBUG_LOG"
    
    log_message "========== TOXOLIB JOB FAILED =========="
    exit 1
fi
"""
    return script

def update_snakemake_paths(snakemake_file, raw_data_files, output_dir, kraken_db_dir, corn_db_dir):
    """Update paths in Snakemake file for HPC execution"""
    with open(snakemake_file, 'r') as f:
        content = f.read()
    
    # Extract the parent directory of output_dir
    output_parent_dir = os.path.dirname(output_dir.rstrip('/'))
    raw_data_dir = f"{output_parent_dir}/Raw_Data"
    
    # Update directories - Raw_Data is outside the output directory
    content = content.replace("RAW_DATA_DIR = \"/home/dac6360/Toxonomy/Raw_Data\"", f"RAW_DATA_DIR = \"{raw_data_dir}\"")
    content = content.replace("PREPROCESSED_DATA_DIR = \"/home/dac6360/Toxonomy/Preprocessed_Data\"", f"PREPROCESSED_DATA_DIR = \"{output_dir}/Preprocessed_Data\"")
    content = content.replace("KRAKEN2_DB_DIR = \"/home/dac6360/Toxonomy/Kraken2_DB\"", f"KRAKEN2_DB_DIR = \"{kraken_db_dir}\"")
    
    # Update other directories
    for dir_name in ["KRAKEN2_DNA_DIR", "BRACKEN_DNA_DIR", "PYTHON_BRACKEN_TO_KRONA_DIR", 
                    "PYTHON_ALPHA_BETA_DIVERSITY_DIR", "PYTHON_RELATIVE_ABUNDANCE_MATRIX_DIR",
                    "FASTP_LOGS_DIR", "BOWTIE2_HOST_LOGS_DIR", "KRAKEN2_DB_LOGS_DIR",
                    "KRAKEN2_DNA_LOGS_DIR", "BRACKEN_DNA_LOGS_DIR", "PYTHON_BRACKEN_TO_KRONA_LOGS_DIR",
                    "PYTHON_ALPHA_BETA_DIVERSITY_LOGS_DIR", "PYTHON_RELATIVE_ABUNDANCE_MATRIX_LOGS_DIR"]:
        content = content.replace(f"{dir_name} = \"/home/dac6360/Toxonomy/", f"{dir_name} = \"{output_dir}/")
    
    # Update corn_db path - ensure it uses the user-uploaded corn database
    content = content.replace("params.index_prefix = \"/home/dac6360/Toxonomy/corn_db/corn_db\"", f"params.index_prefix = \"{corn_db_dir}/corn_db\"")
    
    # Also check for alternative path formats that might be in the Snakefile
    if "params.index_prefix = \"/home/ssd6515/toxotest/corn_db/corn_db\"" in content:
        content = content.replace("params.index_prefix = \"/home/ssd6515/toxotest/corn_db/corn_db\"", f"params.index_prefix = \"{corn_db_dir}/corn_db\"")
    
    # Handle any other hardcoded paths that might be in the Snakefile
    if "index_prefix = \"/home/" in content:
        content = content.replace("index_prefix = \"/home/", f"index_prefix = \"{corn_db_dir}/corn_db\"#")
        content = content.replace("#/corn_db/corn_db\"", "")
    
    # Update sample list based on input files
    sample_names = []
    for raw_file in raw_data_files:
        # Extract sample name from filename (assuming format like sample_R1.fastq.gz)
        base_name = os.path.basename(raw_file)
        sample_name = base_name.split('_')[0]
        if sample_name not in sample_names:
            sample_names.append(sample_name)
    
    # Replace SAMPLES list
    samples_str = ", ".join([f'"{s}"' for s in sample_names])
    content = content.replace("SAMPLES = [\"S1\", \"S2\", \"S3\", \"S4\", \"S5\", \"S6\", \"S7\", \"S8\", \"S9\", \"S10\", \n           \"S11\", \"S12\", \"S13\", \"S14\", \"S15\", \"S16\", \"S17\", \"S18\", \"S19\", \"S20\", \n           \"S21\", \"S22\", \"S23\", \"S24\", \"S25\", \"S26\"]", f"SAMPLES = [{samples_str}]")
    
    # Write updated content back to file
    with open(snakemake_file, 'w') as f:
        f.write(content)
    
    return True

def run_on_hpc(raw_files, output_dir, kraken_db_dir=None, corn_db_dir=None, config_file=None, partition="normal", threads=32, memory=200, time="144:00:00", setup_kraken_db=False, setup_corn_db=False, no_persist=False):
    """Run the toxolib workflow on HPC
    
    Args:
        raw_files (list): List of raw data files to process
        output_dir (str): Output directory on HPC
        kraken_db_dir (str, optional): Path to Kraken2 database on HPC
        corn_db_dir (str, optional): Path to corn genome database on HPC
        config_file (str, optional): Path to HPC configuration file
        partition (str): SLURM partition to use
        threads (int): Number of CPU threads to request
        memory (int): Memory in GB to request
        time (str): Time limit for the job in format HH:MM:SS
        setup_kraken_db (bool): Whether to download and setup Kraken2 database
        setup_corn_db (bool): Whether to download and setup corn genome database
    """
    # Initialize HPC connection
    hpc = HPCConnection(config_file, no_persist=no_persist)
    
    # If not connected, set up connection
    if not hpc.ssh:
        if not hpc.setup_connection():
            logging.error("Failed to connect to HPC")
            return False
    
    try:
        # Create remote directories
        remote_output_dir = output_dir
        # Create Raw_Data directory at the same level as output_dir
        # Extract the parent directory of output_dir
        output_parent_dir = os.path.dirname(output_dir.rstrip('/'))
        remote_raw_data_dir = f"{output_parent_dir}/Raw_Data"
        remote_scripts_dir = f"{remote_output_dir}/scripts"
        remote_kraken_db_dir = kraken_db_dir or f"{remote_output_dir}/Kraken2_DB"
        remote_corn_db_dir = corn_db_dir or f"{remote_output_dir}/corn_db"
        
        # Create output directory and Raw_Data directory separately
        hpc.execute_command(f"mkdir -p {remote_output_dir} {remote_scripts_dir}")
        hpc.execute_command(f"mkdir -p {remote_raw_data_dir}")
        
        logging.info(f"Created output directory: {remote_output_dir}")
        logging.info(f"Created Raw_Data directory: {remote_raw_data_dir}")
        
        # Setup databases if requested
        if setup_kraken_db:
            logging.info(f"Setting up Kraken2 database on HPC at {remote_kraken_db_dir}...")
            hpc.execute_command(f"mkdir -p {remote_kraken_db_dir}")
            
            # Download Kraken2 database locally first
            logging.info("Downloading Kraken2 database locally...")
            local_kraken_db_dir = os.path.join(tempfile.mkdtemp(), "kraken2_db")
            os.makedirs(local_kraken_db_dir, exist_ok=True)
            
            try:
                # Download database
                kraken_db_archive = os.path.join(local_kraken_db_dir, "k2_standard_20240112.tar.gz")
                logging.info(f"Downloading Kraken2 database to {kraken_db_archive}...")
                from .database import download_file
                download_file(
                    "https://genome-idx.s3.amazonaws.com/kraken/k2_standard_20240112.tar.gz", 
                    kraken_db_archive, 
                    "Downloading Kraken2 DB"
                )
                
                # Extract database locally
                logging.info("Extracting Kraken2 database locally...")
                subprocess.run(["tar", "-xzf", kraken_db_archive, "-C", local_kraken_db_dir], check=True)
                
                # Upload extracted database to HPC
                logging.info(f"Uploading Kraken2 database to HPC at {remote_kraken_db_dir}...")
                for item in os.listdir(local_kraken_db_dir):
                    if os.path.isdir(os.path.join(local_kraken_db_dir, item)):
                        # Upload directory contents
                        local_dir = os.path.join(local_kraken_db_dir, item)
                        remote_dir = f"{remote_kraken_db_dir}/{item}"
                        hpc.execute_command(f"mkdir -p {remote_dir}")
                        
                        for root, dirs, files in os.walk(local_dir):
                            for dir_name in dirs:
                                rel_dir = os.path.relpath(os.path.join(root, dir_name), local_dir)
                                hpc.execute_command(f"mkdir -p {remote_dir}/{rel_dir}")
                            
                            for file_name in files:
                                local_file = os.path.join(root, file_name)
                                rel_path = os.path.relpath(local_file, local_dir)
                                remote_file = f"{remote_dir}/{rel_path}"
                                hpc.upload_file(local_file, remote_file)
                
                logging.info("Kraken2 database setup complete")
            
            except Exception as e:
                logging.error(f"Error setting up Kraken2 database: {e}")
                logging.warning("Continuing without Kraken2 database setup. Please set up the database manually.")
            
            finally:
                # Clean up temp directory
                shutil.rmtree(os.path.dirname(local_kraken_db_dir))
        
        if setup_corn_db:
            logging.info(f"Setting up corn genome database on HPC at {remote_corn_db_dir}...")
            hpc.execute_command(f"mkdir -p {remote_corn_db_dir}")
            
            # Download corn genome database locally first
            logging.info("Downloading corn genome database locally...")
            local_corn_db_dir = os.path.join(tempfile.mkdtemp(), "corn_db")
            os.makedirs(local_corn_db_dir, exist_ok=True)
            
            try:
                # Download database
                corn_db_archive = os.path.join(local_corn_db_dir, "corn_db.zip")
                logging.info(f"Downloading corn genome database to {corn_db_archive}...")
                from .database import download_file
                download_file(
                    "https://glwasoilmetagenome.s3.us-east-1.amazonaws.com/corn_db.zip", 
                    corn_db_archive, 
                    "Downloading Corn Genome DB"
                )
                
                # Extract database locally
                logging.info("Extracting corn genome database locally...")
                subprocess.run(["unzip", "-o", corn_db_archive, "-d", local_corn_db_dir], check=True)
                
                # Upload extracted database to HPC
                logging.info(f"Uploading corn genome database to HPC at {remote_corn_db_dir}...")
                for item in os.listdir(local_corn_db_dir):
                    local_path = os.path.join(local_corn_db_dir, item)
                    remote_path = f"{remote_corn_db_dir}/{item}"
                    
                    if os.path.isdir(local_path):
                        # Upload directory contents
                        hpc.execute_command(f"mkdir -p {remote_path}")
                        for root, dirs, files in os.walk(local_path):
                            for dir_name in dirs:
                                rel_dir = os.path.relpath(os.path.join(root, dir_name), local_path)
                                hpc.execute_command(f"mkdir -p {remote_path}/{rel_dir}")
                            
                            for file_name in files:
                                local_file = os.path.join(root, file_name)
                                rel_path = os.path.relpath(local_file, local_path)
                                remote_file = f"{remote_path}/{rel_path}"
                                hpc.upload_file(local_file, remote_file)
                    else:
                        # Upload file
                        hpc.upload_file(local_path, remote_path)
                
                logging.info("Corn genome database setup complete")
            
            except Exception as e:
                logging.error(f"Error setting up corn genome database: {e}")
                logging.warning("Continuing without corn genome database setup. Please set up the database manually.")
            
            finally:
                # Clean up temp directory
                shutil.rmtree(os.path.dirname(local_corn_db_dir))
        
        # Upload raw data files
        logging.info("Uploading raw data files to HPC...")
        for raw_file in raw_files:
            remote_file = f"{remote_raw_data_dir}/{os.path.basename(raw_file)}"
            hpc.upload_file(raw_file, remote_file)
        
        # Upload Snakemake file
        local_snakemake = os.path.join(os.path.dirname(__file__), "data", "Snakefile")
        remote_snakemake = f"{remote_output_dir}/Snakefile"
        hpc.upload_file(local_snakemake, remote_snakemake)
        
        # Upload create_abundance_matrix.py script
        local_script = os.path.join(os.path.dirname(__file__), "data", "create_abundance_matrix.py")
        remote_script = f"{remote_scripts_dir}/create_abundance_matrix.py"
        hpc.upload_file(local_script, remote_script)
        
        # Upload environment.yml file for conda environment creation
        local_env_file = os.path.join(os.path.dirname(__file__), "data", "environment.yml")
        remote_env_file = f"{remote_output_dir}/environment.yml"
        hpc.upload_file(local_env_file, remote_env_file)
        logging.info("Uploaded environment.yml for conda environment creation")
        
        # Update paths in Snakemake file
        logging.info("Updating paths in Snakemake file...")
        # First download the file
        temp_snakemake = "/tmp/Snakefile.tmp"
        hpc.download_file(remote_snakemake, temp_snakemake)
        
        # Update paths
        update_snakemake_paths(
            temp_snakemake, 
            raw_files, 
            remote_output_dir, 
            kraken_db_dir or f"{remote_output_dir}/Kraken2_DB", 
            corn_db_dir or f"{remote_output_dir}/corn_db"
        )
        
        # Upload updated file
        hpc.upload_file(temp_snakemake, remote_snakemake)
        os.remove(temp_snakemake)
        
        # Generate and upload job script
        logging.info("Generating job script...")
        # Use the actual kraken_db_dir and corn_db_dir paths
        actual_kraken_db_dir = kraken_db_dir or f"{remote_output_dir}/Kraken2_DB"
        actual_corn_db_dir = corn_db_dir or f"{remote_output_dir}/corn_db"
        
        try:
            job_script = generate_job_script(
                remote_snakemake, 
                remote_output_dir,
                actual_kraken_db_dir,
                actual_corn_db_dir,
                partition=partition,
                threads=threads,
                memory=memory,
                time=time,
                raw_data_dir=remote_raw_data_dir
            )
        except Exception as e:
            logging.error(f"Error generating job script: {e}")
            return False
        job_script_path = f"{remote_output_dir}/run_toxolib.sh"
        
        with open("/tmp/run_toxolib.sh", "w") as f:
            f.write(job_script)
        
        hpc.upload_file("/tmp/run_toxolib.sh", job_script_path)
        os.remove("/tmp/run_toxolib.sh")
        
        # Make job script executable
        hpc.execute_command(f"chmod +x {job_script_path}")
        
        # Submit job
        logging.info("Submitting job to HPC...")
        job_id = hpc.submit_job(job_script_path)
        
        if not job_id:
            logging.error("Failed to submit job")
            return False
        
        # Wait for job completion
        logging.info(f"Job submitted with ID: {job_id}")
        logging.info("You can check job status using: toxolib hpc-status --job-id JOB_ID")
        logging.info("Or download results using: toxolib hpc-download --job-id JOB_ID --output-dir LOCAL_DIR")
        
        return job_id
        
    except Exception as e:
        logging.error(f"Error running on HPC: {e}")
        return False
    finally:
        # Don't close the connection to maintain persistence between commands
        pass

def get_job_details(job_id, config_file=None, no_persist=False):
    """Get detailed information about a job from SLURM's accounting system
    
    Args:
        job_id (str): HPC job ID to get details for
        config_file (str, optional): Path to HPC configuration file
        no_persist (bool): Do not maintain persistent connection
        
    Returns:
        dict: Dictionary containing job details, or None if job not found
    """
    # Initialize HPC connection
    hpc = HPCConnection(config_file, no_persist=no_persist)
    
    # If not connected, set up connection
    if not hpc.ssh:
        if not hpc.setup_connection():
            logging.error("Failed to connect to HPC")
            return None
    
    try:
        # Get detailed job information from sacct
        cmd = f"sacct -j {job_id} --format=JobID,State,ExitCode,NodeList,Start,End,Elapsed,MaxRSS,MaxVMSize,Comment --parsable2"
        _, stdout, stderr = hpc.ssh.exec_command(cmd)
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        
        if error:
            logging.error(f"Error getting job details: {error}")
            return None
        
        if not output:
            logging.error(f"No information found for job {job_id}")
            return None
        
        # Parse the output
        lines = output.split('\n')
        if len(lines) < 2:
            logging.error(f"Unexpected output format from sacct: {output}")
            return None
        
        # Get headers and values
        headers = lines[0].split('|')
        values = lines[1].split('|')
        
        # Create a dictionary of job details
        job_details = {}
        for i in range(min(len(headers), len(values))):
            job_details[headers[i]] = values[i]
        
        return job_details
    
    except Exception as e:
        logging.error(f"Error getting job details: {e}")
        return None
    finally:
        if no_persist:
            hpc.close_connection()

def retrieve_job_logs(job_id, local_dir=None, log_type="all", tail=50, config_file=None, no_persist=False):
    """Retrieve and view logs from HPC jobs
    
    Args:
        job_id (str): HPC job ID to retrieve logs for
        local_dir (str, optional): Local directory to save logs
        log_type (str): Type of logs to retrieve (all, out, err, debug, snakemake)
        tail (int): Number of lines to show from the end of each log file
        config_file (str, optional): Path to HPC configuration file
        no_persist (bool): Do not maintain persistent connection
        
    Returns:
        bool: True if logs were successfully retrieved, False otherwise
    """
    # Initialize HPC connection
    hpc = HPCConnection(config_file, no_persist=no_persist)
    
    # If not connected, set up connection
    if not hpc.ssh:
        if not hpc.setup_connection():
            logging.error("Failed to connect to HPC")
            return False
    
    try:
        # Get job details to find output directory
        _, stdout, _ = hpc.ssh.exec_command(f"sacct -j {job_id} --format=WorkDir --noheader | head -1")
        work_dir = stdout.read().decode().strip()
        
        if not work_dir:
            # Try to find the job directory by searching for log files
            logging.info(f"Searching for log files for job {job_id}...")
            _, stdout, _ = hpc.ssh.exec_command(f"find ~/ -name '*{job_id}*.out' -o -name '*{job_id}*.err' | head -1")
            log_file = stdout.read().decode().strip()
            
            if log_file:
                # Extract directory from log file path
                work_dir = os.path.dirname(os.path.dirname(log_file))
                logging.info(f"Found job directory: {work_dir}")
            else:
                logging.error(f"Could not find any log files for job {job_id}")
                return False
        
        # Determine log directory - first check in the output directory
        output_dir = work_dir
        log_dir = f"{output_dir}/logs"
        
        # Check if log directory exists
        _, stdout, _ = hpc.ssh.exec_command(f"test -d {log_dir} && echo 'exists'")
        if stdout.read().decode().strip() != 'exists':
            # If not found, try in the parent directory (for the new structure)
            output_dir = os.path.dirname(work_dir)
            log_dir = f"{output_dir}/logs"
            _, stdout, _ = hpc.ssh.exec_command(f"test -d {log_dir} && echo 'exists'")
            if stdout.read().decode().strip() != 'exists':
                # If still not found, try the standard SLURM output directory
                _, stdout, _ = hpc.ssh.exec_command(f"find ~/ -name '*{job_id}*.out' -o -name '*{job_id}*.err' | head -1")
                slurm_log = stdout.read().decode().strip()
                if slurm_log:
                    log_dir = os.path.dirname(slurm_log)
                    _, stdout, _ = hpc.ssh.exec_command(f"test -d {log_dir} && echo 'exists'")
                    if stdout.read().decode().strip() != 'exists':
                        logging.error(f"Log directory not found: {log_dir}")
                        return False
                else:
                    # Create logs directory in the output directory
                    logging.info(f"Creating logs directory in {output_dir}")
                    hpc.execute_command(f"mkdir -p {output_dir}/logs")
                    log_dir = f"{output_dir}/logs"
                    
                    # Check if creation was successful
                    _, stdout, _ = hpc.ssh.exec_command(f"test -d {log_dir} && echo 'exists'")
                    if stdout.read().decode().strip() != 'exists':
                        logging.error(f"Failed to create logs directory in {output_dir}")
                        logging.error(f"Log directory not found and no SLURM logs found for job {job_id}")
                        return False
                    else:
                        logging.info(f"Created logs directory: {log_dir}")
        
        # Get list of log files
        _, stdout, _ = hpc.ssh.exec_command(f"find {log_dir} -name '*{job_id}*' | sort")
        log_files = stdout.read().decode().strip().split('\n')
        
        if not log_files or log_files[0] == '':
            # Try to find standard SLURM output files - search more aggressively
            logging.info(f"No log files found in {log_dir}, searching for SLURM output files...")
            
            # Search in multiple locations with a single command for efficiency
            search_cmd = f"""find ~/ /scratch /tmp -name '*{job_id}*' -type f 2>/dev/null | grep -E '\.(out|err|log)$|{job_id}' | sort"""
            logging.info(f"Executing search command: {search_cmd}")
            _, stdout, _ = hpc.ssh.exec_command(search_cmd)
            slurm_logs = stdout.read().decode().strip().split('\n')
            
            if not slurm_logs or slurm_logs[0] == '':
                # Try a more general search for any file containing the job ID
                logging.info("No log files found with standard extensions, searching for any files containing the job ID...")
                _, stdout, _ = hpc.ssh.exec_command(f"find ~/ -type f -name '*{job_id}*' 2>/dev/null | sort")
                general_logs = stdout.read().decode().strip().split('\n')
                
                if not general_logs or general_logs[0] == '':
                    # Last resort: check SLURM's sacct command for detailed job info
                    logging.info("No files found, retrieving job details from sacct...")
                    _, stdout, _ = hpc.ssh.exec_command(f"sacct -j {job_id} --format=JobID,State,ExitCode,NodeList,Start,End,Elapsed,MaxRSS,MaxVMSize --parsable2")
                    sacct_output = stdout.read().decode().strip()
                    
                    if sacct_output:
                        print(f"\n{'=' * 80}")
                        print(f"Job {job_id} details from sacct:")
                        print(f"{'=' * 80}")
                        print(sacct_output)
                        print(f"\nNo log files found for job {job_id}. The job may have failed before creating any logs.")
                        return True
                    else:
                        logging.error(f"No information found for job {job_id}")
                        return False
                else:
                    log_files = general_logs
                    log_dir = os.path.dirname(general_logs[0])
                    logging.info(f"Found files containing job ID: {log_files}")
            else:
                log_files = slurm_logs
                log_dir = os.path.dirname(slurm_logs[0])
                logging.info(f"Found SLURM output files: {log_files}")
        
        # Filter log files based on log_type
        if log_type != "all":
            log_files = [f for f in log_files if f"_{log_type}" in f or f".{log_type}" in f]
            
            if not log_files:
                logging.error(f"No {log_type} log files found for job {job_id}")
                return False
        
        # Create local directory if specified
        if local_dir:
            os.makedirs(local_dir, exist_ok=True)
        
        # Process each log file
        for log_file in log_files:
            file_name = os.path.basename(log_file)
            
            # Download file if local_dir is specified
            if local_dir:
                local_file = os.path.join(local_dir, file_name)
                hpc.download_file(log_file, local_file)
                logging.info(f"Downloaded {file_name} to {local_file}")
            
            # Display tail of log file
            print(f"\n{'=' * 80}")
            print(f"Log file: {log_file}")
            print(f"{'=' * 80}")
            
            _, stdout, _ = hpc.ssh.exec_command(f"tail -n {tail} {log_file}")
            log_content = stdout.read().decode()
            print(log_content)
        
        return True
    
    except Exception as e:
        logging.error(f"Error retrieving logs: {e}")
        return False
    finally:
        if no_persist:
            hpc.close_connection()

def download_results(job_id, local_dir, config_file=None, no_persist=False):
    """Download results from HPC after job completion"""
    # Initialize HPC connection
    hpc = HPCConnection(config_file, no_persist=no_persist)
    
    # If not connected, set up connection
    if not hpc.ssh:
        if not hpc.setup_connection():
            logging.error("Failed to connect to HPC")
            return False
    
    try:
        # Check job status
        status = hpc.check_job_status(job_id)
        
        if status != 'COMPLETED':
            logging.error(f"Job {job_id} has not completed successfully. Status: {status}")
            return False
        
        # Get job details to find output directory
        _, stdout, _ = hpc.ssh.exec_command(f"sacct -j {job_id} --format=WorkDir --noheader | head -1")
        work_dir = stdout.read().decode().strip()
        
        if not work_dir:
            logging.error(f"Could not determine working directory for job {job_id}")
            return False
        
        # Determine output directory based on working directory
        output_dir = os.path.dirname(work_dir)
        abundance_matrix = f"{output_dir}/Results/Taxonomic_Profiling/5_DNA_Relative_Abundance_Matrix_Python/relative_abundance_matrix_species.csv"
        
        # Check if abundance matrix exists
        if not hpc.check_file_exists(abundance_matrix):
            logging.error(f"Abundance matrix not found at {abundance_matrix}")
            return False
        
        # Create local directory
        os.makedirs(local_dir, exist_ok=True)
        
        # Download abundance matrix
        local_matrix = os.path.join(local_dir, "abundance_matrix.csv")
        if not hpc.download_file(abundance_matrix, local_matrix):
            logging.error("Failed to download abundance matrix")
            return False
        
        logging.info(f"Downloaded abundance matrix to {local_matrix}")
        return local_matrix
        
    except Exception as e:
        logging.error(f"Error downloading results: {e}")
        return False
    finally:
        # Don't close the connection to maintain persistence between commands
        pass
