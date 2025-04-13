# toxolib (v0.1.38)

A Python package for metagenomic taxonomic profiling and abundance matrix generation.

## Installation

### Using pip

```bash
pip install toxolib
```

### Install directly from GitHub

```bash
pip install git+https://github.com/dhruvac29/toxolib.git
```

### Using conda

We recommend using conda to install all dependencies. An environment file is included in the package:

```bash
# Clone the repository
git clone https://github.com/dhruvac29/toxolib.git
cd toxolib

# Create and activate the conda environment
conda env create -f environment.yml
conda activate taxonomy_env

# Install the package
pip install -e .
```

## Requirements

This package requires the following external tools to be installed and available in your PATH:

- Kraken2
- Bracken
- Krona (for visualization)
- fastp (for preprocessing)
- bowtie2 (for host removal)
- samtools

All these dependencies are included in the conda environment file.

## Database Setup

### Automated Database Setup

Toxolib provides automated database setup for both local and HPC environments.

#### Local Database Setup

```bash
# Set up both Kraken2 and corn genome databases locally
toxolib db-setup -o /path/to/databases --kraken --corn

# Set up only Kraken2 database locally
toxolib db-setup -o /path/to/databases --kraken

# Set up only corn genome database locally
toxolib db-setup -o /path/to/databases --corn

# Force re-download of databases even if they exist
toxolib db-setup -o /path/to/databases --kraken --corn --force

# Set up databases directly on HPC (new in v0.1.22)
toxolib db-setup -o /path/on/hpc/databases --kraken --corn --hpc
```

After setup, you should set the environment variable for Kraken2:

```bash
export KRAKEN2_DB_DIR=/path/to/databases/Kraken2_DB
```

#### HPC Database Setup

There are two ways to set up reference databases on your HPC server:

##### Option 1: Direct HPC Database Setup (New in v0.1.23)

You can directly set up databases on your HPC server without processing any data:

```bash
# Set up both Kraken2 and corn genome databases directly on HPC
toxolib db-setup -o /path/on/hpc/databases --kraken --corn --hpc

# Set up only Kraken2 database on HPC
toxolib db-setup -o /path/on/hpc/databases --kraken --hpc

# Set up only corn genome database on HPC
toxolib db-setup -o /path/on/hpc/databases --corn --hpc
```

##### Option 2: Database Setup During Job Submission

When submitting jobs to the HPC, you can also set up the databases as part of the job submission process:

```bash
# Process data and set up both databases
toxolib hpc -r sample1_R1.fastq.gz sample1_R2.fastq.gz -o /path/on/hpc/output_dir \
    --setup-kraken-db --setup-corn-db

# Process data and set up only Kraken2 database
toxolib hpc -r sample1_R1.fastq.gz sample1_R2.fastq.gz -o /path/on/hpc/output_dir \
    --setup-kraken-db

# Process data and set up only corn genome database
toxolib hpc -r sample1_R1.fastq.gz sample1_R2.fastq.gz -o /path/on/hpc/output_dir \
    --setup-corn-db
```

When using these options, toxolib will:
1. Download the databases to your local machine
2. Extract the databases locally
3. Upload the extracted databases to the HPC
4. Configure the Snakefile to use the correct database paths

This approach works even if your HPC has restricted internet access or firewalls that prevent direct downloads.

### Manual Database Setup

If you prefer to set up the databases manually, you can follow these steps:

#### Kraken2 Database

You can download the standard Kraken2 database from:
[https://genome-idx.s3.amazonaws.com/kraken/k2_standard_20240112.tar.gz](https://genome-idx.s3.amazonaws.com/kraken/k2_standard_20240112.tar.gz)

```bash
wget https://genome-idx.s3.amazonaws.com/kraken/k2_standard_20240112.tar.gz
tar -xzf k2_standard_20240112.tar.gz -C /path/to/kraken2/database
export KRAKEN2_DB_DIR=/path/to/kraken2/database
```

#### Corn Genome Database

For host removal, you can download the corn genome reference from:
[https://glwasoilmetagenome.s3.us-east-1.amazonaws.com/corn_db.zip](https://glwasoilmetagenome.s3.us-east-1.amazonaws.com/corn_db.zip)

```bash
wget https://glwasoilmetagenome.s3.us-east-1.amazonaws.com/corn_db.zip
unzip corn_db.zip -d /path/to/corn_db
```

## Usage

### Local Usage

#### Generate abundance matrix from raw data

```bash
toxolib abundance -r raw_data_1.fastq.gz raw_data_2.fastq.gz -o output_directory
```

This will:
1. Run Kraken2 on the raw data
2. Run Bracken on the Kraken2 results
3. Generate an abundance matrix from the Bracken results

#### Create abundance matrix from existing Bracken files

```bash
toxolib matrix -i sample1_species.bracken sample2_species.bracken -o abundance_matrix.csv
```

### HPC Usage

Toxolib can run the analysis pipeline on an HPC cluster using SLURM for job scheduling.

#### 1. Set up HPC connection

```bash
toxolib hpc-setup --hostname your-hpc-server.edu --username your-username --key-file ~/.ssh/id_rsa
```

This will save your HPC connection details to `~/.toxolib/hpc_config.yaml`.

#### 2. Run the pipeline on HPC

```bash
toxolib hpc -r raw_data_1.fastq.gz raw_data_2.fastq.gz -o /path/on/hpc/output_dir \
    --kraken-db /path/on/hpc/kraken2_db \
    --corn-db /path/on/hpc/corn_db \
    --partition normal --threads 32 --memory 200 --time 144:00:00
```

This will:
1. Upload your raw data files to the HPC in a separate Raw_Data directory (new in v0.1.25)
2. Create a Snakemake workflow file
3. Upload an environment.yml file to the HPC
4. Submit a SLURM job to run the analysis
5. Return a job ID for tracking

> **Note (New in v0.1.25)**: Raw data files are now uploaded to a `Raw_Data` directory that is created at the same level as your output directory, not inside it. This change ensures better organization and separation between raw data and processed outputs.
>
> **Note (New in v0.1.26)**: Fixed issues with database paths in the Snakefile. The corn database path is now properly updated to use the user-uploaded database. Added additional validation checks to ensure all required directories and files exist before running the workflow.
>
> **Note (New in v0.1.27)**: Fixed an issue with database path references in the job script. The Kraken2 and corn database paths are now correctly passed to the job script, ensuring proper validation of database directories before running the workflow.
>
> **Note (New in v0.1.28)**: Significantly improved log retrieval functionality. The `hpc-logs` command now searches multiple locations for job logs, including the output directory, parent directory, user's home directory, and the standard SLURM output directories. This ensures that logs can be found even if the job fails early in execution.
>
> **Note (New in v0.1.29)**: Further enhanced log retrieval with aggressive searching across the entire file system. When logs cannot be found, the system now falls back to displaying detailed job information from SLURM's accounting system, providing critical information about job failures even when no log files are available.
>
> **Note (New in v0.1.30)**: Added a new `hpc-details` command that provides comprehensive job information directly from SLURM's accounting system. This command shows detailed job statistics including state, exit code, node list, run time, and resource usage, helping diagnose job failures even when log files are not accessible.
>
> **Note (New in v0.1.31)**: Significantly improved conda environment handling in HPC jobs. The system now uses multiple fallback methods to find or install conda if the anaconda3 module isn't available on the HPC system. Added support for using a custom taxonomy_env.yaml file if available, and switched to named environments for better compatibility. These changes make toxolib more robust across different HPC environments.
>
> **Note (New in v0.1.32)**: Enhanced logs directory handling to automatically create the logs directory if it doesn't exist. This ensures that log files can be written without errors even when the logs directory is not present in the output directory.

##### Automatic Conda Environment Creation

When submitting a job to the HPC, toxolib will automatically:
1. Upload a conda environment.yml file to the HPC
2. Create a conda environment in the output directory if it doesn't exist
3. Activate the environment before running the analysis

This ensures all required dependencies are available on the HPC without requiring manual environment setup.

#### 3. Check job status

```bash
toxolib hpc-status --job-id your_job_id
```

#### 4. View job logs (New in v0.1.24)

The new `hpc-logs` command allows you to easily retrieve and view logs from your HPC jobs:

```bash
# View all logs for a job
toxolib hpc-logs --job-id your_job_id

# View only Snakemake logs
toxolib hpc-logs --job-id your_job_id --log-type snakemake

# View only error logs
toxolib hpc-logs --job-id your_job_id --log-type err

# View more lines from the logs
toxolib hpc-logs --job-id your_job_id --tail 100

# Download logs to a local directory
toxolib hpc-logs --job-id your_job_id --output-dir ./job_logs
```

This command is particularly useful for debugging failed jobs, as it provides detailed information about what went wrong during execution.

#### 5. Download results when complete

```bash
toxolib hpc-download --job-id your_job_id --output-dir ./local_results
```

#### 6. HPC File Management

Toxolib provides several commands to manage files and directories on the HPC:

```bash
# Print working directory on HPC
toxolib hpc-pwd

# Change directory on HPC
toxolib hpc-cd --path /path/on/hpc

# List files on HPC
toxolib hpc-ls [--path /path/on/hpc] [--long] [--all]

# Create directory on HPC
toxolib hpc-mkdir --path /path/on/hpc [--parents]
```

These commands allow you to navigate and manage files on the HPC without needing to manually connect via SSH.

#### 7. Persistent Connections

Toxolib now maintains persistent SSH connections to the HPC between commands. This means:

1. You only need to authenticate once per terminal session
2. Connections remain open for subsequent commands
3. No need to reconnect for each command
4. Faster command execution since connection setup is skipped

Connections are automatically managed:
- Kept alive with keep-alive packets
- Automatically closed after 10 minutes of inactivity
- Automatically closed when your terminal session ends

If you prefer not to use persistent connections, you can disable this feature with the `--no-persist` flag:

```bash
toxolib hpc-pwd --no-persist
```

#### 7. Session-Based Password Storage

Toxolib includes session-based password storage, which allows you to enter your password just once per terminal session. The password is securely stored in memory and automatically reused for subsequent commands during your session.

- Password is only stored for the current terminal session
- Password is automatically cleared when your session ends
- Password is encrypted in memory using strong cryptography
- No passwords are ever saved to disk

This feature makes it more convenient to run multiple HPC commands without having to re-enter your password each time.

##### Get Current Working Directory

```bash
# Show current directory and close connection
toxolib hpc-pwd

# Show current directory and keep connection open
toxolib hpc-pwd --keep-open
```

##### Change Directory

```bash
# Change directory and close connection
toxolib hpc-cd --path /path/to/directory

# Change directory and keep connection open
toxolib hpc-cd --path /path/to/directory --keep-open

# Go up one level
toxolib hpc-cd --path ..

# Go up one level and keep connection open
toxolib hpc-cd --path .. --keep-open
```

##### Create Directory

```bash
# Create directory and close connection
toxolib hpc-mkdir --path /path/to/new/directory

# Create directory and keep connection open
toxolib hpc-mkdir --path /path/to/new/directory --keep-open
```

##### List Files

```bash
# List files in current directory and close connection
toxolib hpc-ls

# List files in current directory and keep connection open
toxolib hpc-ls --keep-open

# List files in specific directory
toxolib hpc-ls --path /path/to/directory

# List files in specific directory and keep connection open
toxolib hpc-ls --path /path/to/directory --keep-open

# Long format listing (like ls -l)
toxolib hpc-ls --long

# Show hidden files (like ls -a)
toxolib hpc-ls --all

# Combine options
toxolib hpc-ls --path /path/to/directory --long --all

# Combine options and keep connection open
toxolib hpc-ls --path /path/to/directory --long --all --keep-open
```

#### Manual Setup on HPC

When using the HPC functionality, you can manually upload and extract these databases on your HPC system:

```bash
# On your local machine, download the databases
wget https://genome-idx.s3.amazonaws.com/kraken/k2_standard_20240112.tar.gz
wget https://glwasoilmetagenome.s3.us-east-1.amazonaws.com/corn_db.zip

# Upload to HPC (using scp)
scp k2_standard_20240112.tar.gz your-username@your-hpc-server.edu:/path/on/hpc/
scp corn_db.zip your-username@your-hpc-server.edu:/path/on/hpc/

# SSH into HPC and extract
ssh your-username@your-hpc-server.edu
mkdir -p /path/on/hpc/kraken2_db
tar -xzf /path/on/hpc/k2_standard_20240112.tar.gz -C /path/on/hpc/kraken2_db
mkdir -p /path/on/hpc/corn_db
unzip /path/on/hpc/corn_db.zip -d /path/on/hpc/corn_db
```

Then when running toxolib, specify these paths:

```bash
toxolib hpc -r raw_data_1.fastq.gz raw_data_2.fastq.gz -o /path/on/hpc/output_dir \
    --kraken-db /path/on/hpc/kraken2_db \
    --corn-db /path/on/hpc/corn_db
```

## Version History

### v0.1.38
- Fixed variable reference error in job script that was causing job submission failures
- Improved HPC job script to correctly handle Raw_Data directory paths

### v0.1.37
- Added complete offline mode support for HPC environments without internet access
- Implemented a direct workflow runner as fallback when Snakemake is not available
- Improved environment detection and handling for compute nodes
- Added automatic detection of network connectivity

### v0.1.36
- Hotfix for syntax error in snakemake installation script
- Fixed shell script syntax for error handling in offline environments

### v0.1.35
- Added automatic snakemake installation in HPC job script
- Improved conda initialization for offline environments
- Fixed conda activation in shell script for compute nodes
- Enhanced error handling for missing dependencies

### v0.1.34
- Hotfix for syntax error in HPC job script generation
- Fixed shell script formatting for conda environment activation
- Improved quoting of environment variables in shell script

### v0.1.33
- Enhanced conda environment handling in HPC job scripts
- Added fallback mechanisms for environments when compute nodes lack internet access
- Improved conda initialization with proper shell hooks
- Added support for alternative Python modules when conda is unavailable
- Added graceful degradation to system Python when environment creation fails

### v0.1.32
- Added automatic creation of logs directory if it doesn't exist
- Enhanced job script to check for required directories and files before execution
- Improved log retrieval with better error handling and diagnostics

## License

MIT
