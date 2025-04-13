"""
Command-line interface for toxolib
"""
import argparse
import sys
import os
import logging
import atexit
import tempfile
import shutil
from pathlib import Path
from .abundance_matrix import process_raw_data, create_abundance_matrix, check_dependencies
from .hpc import HPCConnection, run_on_hpc, download_results, retrieve_job_logs, get_job_details
from .database import setup_databases, setup_kraken2_db, setup_corn_db
from .session import clear_connections

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def print_banner():
    """Print the toxolib banner"""
    banner = """
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║   ████████╗ ██████╗ ██╗  ██╗ ██████╗ ██╗     ██╗██████╗   ║
    ║   ╚══██╔══╝██╔═══██╗╚██╗██╔╝██╔═══██╗██║     ██║██╔══██╗  ║
    ║      ██║   ██║   ██║ ╚███╔╝ ██║   ██║██║     ██║██████╔╝  ║
    ║      ██║   ██║   ██║ ██╔██╗ ██║   ██║██║     ██║██╔══██╗  ║
    ║      ██║   ╚██████╔╝██╔╝ ██╗╚██████╔╝███████╗██║██████╔╝  ║
    ║      ╚═╝    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝╚═════╝   ║
    ║                                                            ║
    ║   Metagenomic Taxonomic Profiling & Abundance Matrix Tool  ║
    ║                         v0.1.39                           ║
    ╚════════════════════════════════════════════════════════════╝
    """
    print(banner)

# Register cleanup function to close all connections on exit
atexit.register(clear_connections)

def main():
    """Main entry point for the toxolib CLI"""
    # Check if help is requested
    help_requested = False
    if len(sys.argv) == 1 or '--help' in sys.argv or '-h' in sys.argv:
        help_requested = True
        
    # Check if version is requested
    version_requested = False
    if '--version' in sys.argv or '-v' in sys.argv:
        version_requested = True
    
    # Only print banner for actual commands, not for help
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-') and not help_requested:
        print_banner()
    
    parser = argparse.ArgumentParser(
        description="toxolib - A tool for metagenomic taxonomic profiling and abundance matrix generation",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Add version argument at the top level
    parser.add_argument('--version', '-v', action='store_true', help='Show version information')
    
    # Add global option for persistent connections
    parser.add_argument('--no-persist', action='store_true', help='Do not maintain persistent connections between commands')
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Abundance matrix from raw data command
    abundance_parser = subparsers.add_parser(
        "abundance", help="Generate abundance matrix from raw data"
    )
    abundance_parser.add_argument(
        "-r", "--raw-files", nargs="+", required=True,
        help="Raw fastq files (can be gzipped)"
    )
    abundance_parser.add_argument(
        "-o", "--output-dir", required=True,
        help="Output directory"
    )
    abundance_parser.add_argument(
        "-t", "--threads", type=int, default=8,
        help="Number of threads to use (default: 8)"
    )
    
    # Direct abundance matrix creation from Bracken files
    matrix_parser = subparsers.add_parser(
        "matrix", help="Create abundance matrix from existing Bracken files"
    )
    matrix_parser.add_argument(
        "-i", "--input-files", nargs="+", required=True,
        help="List of Bracken files"
    )
    matrix_parser.add_argument(
        "-o", "--output", required=True,
        help="Output CSV file"
    )
    
    # Add version command
    version_parser = subparsers.add_parser(
        "version", help="Show version information"
    )
    
    # HPC commands
    hpc_parser = subparsers.add_parser(
        "hpc", help="Run on HPC cluster"
    )
    hpc_parser.add_argument(
        "-r", "--raw-files", nargs="+", required=True,
        help="Raw fastq files (can be gzipped)"
    )
    hpc_parser.add_argument(
        "-o", "--output-dir", required=True,
        help="Output directory on HPC"
    )
    hpc_parser.add_argument(
        "--kraken-db", 
        help="Path to Kraken2 database on HPC"
    )
    hpc_parser.add_argument(
        "--corn-db", 
        help="Path to corn database on HPC"
    )
    hpc_parser.add_argument(
        "--setup-kraken-db", action="store_true",
        help="Download and setup Kraken2 database on HPC"
    )
    hpc_parser.add_argument(
        "--setup-corn-db", action="store_true",
        help="Download and setup corn genome database on HPC"
    )
    hpc_parser.add_argument(
        "--config", 
        help="Path to HPC configuration file"
    )
    hpc_parser.add_argument(
        "--no-persist", action="store_true",
        help="Do not maintain persistent connection"
    )
    
    # HPC job configuration
    hpc_parser.add_argument(
        "--partition",
        default="normal",
        help="SLURM partition to use (default: normal)"
    )
    hpc_parser.add_argument(
        "--threads",
        type=int,
        default=32,
        help="Number of CPU threads to request (default: 32)"
    )
    hpc_parser.add_argument(
        "--memory",
        type=int,
        default=200,
        help="Memory in GB to request (default: 200)"
    )
    hpc_parser.add_argument(
        "--time",
        default="144:00:00",
        help="Time limit for the job in format HH:MM:SS (default: 144:00:00)")
    
    # HPC setup command
    hpc_setup_parser = subparsers.add_parser(
        "hpc-setup", help="Set up HPC connection"
    )
    hpc_setup_parser.add_argument(
        "--hostname", required=True,
        help="HPC hostname"
    )
    hpc_setup_parser.add_argument(
        "--username", required=True,
        help="HPC username"
    )
    hpc_setup_parser.add_argument(
        "--key-file",
        help="Path to SSH key file"
    )
    
    # HPC status command
    hpc_status_parser = subparsers.add_parser(
        "hpc-status", help="Check HPC job status"
    )
    hpc_status_parser.add_argument(
        "--job-id", required=True,
        help="HPC job ID"
    )
    hpc_status_parser.add_argument(
        "--config",
        help="Path to HPC configuration file"
    )
    hpc_status_parser.add_argument(
        "--no-persist", action="store_true",
        help="Do not maintain persistent connection"
    )
    
    # HPC download command
    hpc_download_parser = subparsers.add_parser(
        "hpc-download", help="Download results from HPC"
    )
    hpc_download_parser.add_argument(
        "--job-id", required=True,
        help="HPC job ID"
    )
    hpc_download_parser.add_argument(
        "--output-dir", required=True,
        help="Local output directory"
    )
    hpc_download_parser.add_argument(
        "--config",
        help="Path to HPC configuration file"
    )
    hpc_download_parser.add_argument(
        "--no-persist", action="store_true",
        help="Do not maintain persistent connection"
    )
    
    # HPC logs command
    hpc_logs_parser = subparsers.add_parser(
        "hpc-logs", help="Retrieve and view logs from HPC jobs"
    )
    hpc_logs_parser.add_argument(
        "--job-id", required=True,
        help="HPC job ID to retrieve logs for"
    )
    hpc_logs_parser.add_argument(
        "--output-dir",
        help="Local directory to save logs (optional)"
    )
    hpc_logs_parser.add_argument(
        "--log-type", choices=["all", "out", "err", "debug", "snakemake"], default="all",
        help="Type of logs to retrieve (default: all)"
    )
    hpc_logs_parser.add_argument(
        "--tail", type=int, default=50,
        help="Number of lines to show from the end of each log file (default: 50)"
    )
    hpc_logs_parser.add_argument(
        "--config",
        help="Path to HPC configuration file"
    )
    hpc_logs_parser.add_argument(
        "--no-persist", action="store_true",
        help="Do not maintain persistent connection"
    )
    
    # HPC job details command
    hpc_details_parser = subparsers.add_parser(
        "hpc-details", help="Get detailed information about HPC jobs"
    )
    hpc_details_parser.add_argument(
        "--job-id", required=True,
        help="HPC job ID to get details for"
    )
    hpc_details_parser.add_argument(
        "--config",
        help="Path to HPC configuration file"
    )
    hpc_details_parser.add_argument(
        "--no-persist", action="store_true",
        help="Do not maintain persistent connection"
    )
    
    # HPC pwd command (get current working directory)
    hpc_pwd_parser = subparsers.add_parser(
        "hpc-pwd", help="Get current working directory on HPC"
    )
    hpc_pwd_parser.add_argument(
        "--config",
        help="Path to HPC configuration file"
    )
    hpc_pwd_parser.add_argument(
        "--no-persist", action="store_true",
        help="Do not maintain persistent connection"
    )
    
    # HPC mkdir command (create directory)
    hpc_mkdir_parser = subparsers.add_parser(
        "hpc-mkdir", help="Create a new directory on HPC"
    )
    hpc_mkdir_parser.add_argument(
        "--path", required=True,
        help="Path of the directory to create on HPC"
    )
    hpc_mkdir_parser.add_argument(
        "--parents", action="store_true", default=True,
        help="Create parent directories as needed (default: True)"
    )
    hpc_mkdir_parser.add_argument(
        "--config",
        help="Path to HPC configuration file"
    )
    hpc_mkdir_parser.add_argument(
        "--no-persist", action="store_true",
        help="Do not maintain persistent connection"
    )
    
    # HPC cd command (change directory)
    hpc_cd_parser = subparsers.add_parser(
        "hpc-cd", help="Change the current working directory on HPC"
    )
    hpc_cd_parser.add_argument(
        "--path", required=True,
        help="Path to change to. Use '..' to go up one level."
    )
    hpc_cd_parser.add_argument(
        "--config",
        help="Path to HPC configuration file"
    )
    hpc_cd_parser.add_argument(
        "--no-persist", action="store_true",
        help="Do not maintain persistent connection"
    )
    
    # HPC ls command (list directory)
    hpc_ls_parser = subparsers.add_parser(
        "hpc-ls", help="List files in a directory on HPC"
    )
    hpc_ls_parser.add_argument(
        "--path",
        help="Path to list. If not specified, lists the current directory."
    )
    hpc_ls_parser.add_argument(
        "--long", "-l", action="store_true",
        help="Use long listing format"
    )
    hpc_ls_parser.add_argument(
        "--all", "-a", action="store_true",
        help="Show hidden files (starting with .)"
    )
    hpc_ls_parser.add_argument(
        "--config",
        help="Path to HPC configuration file"
    )
    hpc_ls_parser.add_argument(
        "--no-persist", action="store_true",
        help="Do not maintain persistent connection"
    )
    
    # HPC shell command (interactive shell)
    hpc_shell_parser = subparsers.add_parser(
        "hpc-shell", help="Start an interactive shell session with the HPC"
    )
    hpc_shell_parser.add_argument(
        "--config",
        help="Path to HPC configuration file"
    )
    
    # Add database setup command
    db_setup_parser = subparsers.add_parser(
        "db-setup", help="Download and setup databases"
    )
    db_setup_parser.add_argument(
        "-o", "--output-dir", required=True,
        help="Directory to store databases"
    )
    db_setup_parser.add_argument(
        "--kraken", action="store_true",
        help="Download and setup Kraken2 database"
    )
    db_setup_parser.add_argument(
        "--corn", action="store_true",
        help="Download and setup corn genome database"
    )
    db_setup_parser.add_argument(
        "--force", action="store_true",
        help="Force re-download of databases even if they exist"
    )
    db_setup_parser.add_argument(
        "--hpc", action="store_true",
        help="Setup databases on HPC instead of locally"
    )
    db_setup_parser.add_argument(
        "--config",
        help="Path to HPC configuration file (only used with --hpc)"
    )
    db_setup_parser.add_argument(
        "--no-persist", action="store_true",
        help="Do not maintain persistent connection (only used with --hpc)"
    )
    
    # Parse arguments
    # If help is requested, print help and exit
    if help_requested:
        parser.print_help()
        sys.exit(0)
    
    # If version is requested, show version and exit
    if version_requested:
        from . import __version__
        print(f"toxolib version {__version__}")
        sys.exit(0)
        
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(0)
    
    # Handle version command first
    if args.command == "version":
        from . import __version__
        print(f"toxolib version {__version__}")
        sys.exit(0)
    
    # Handle HPC commands
    if args.command == "hpc-setup":
        hpc = HPCConnection()
        if hpc.setup_connection(args.hostname, args.username, key_file=args.key_file):
            hpc.save_config()
            print(f"\n✅ HPC connection set up successfully for {args.username}@{args.hostname}")
            print("Configuration saved to ~/.toxolib/hpc_config.yaml")
        else:
            print("\n❌ Failed to set up HPC connection")
        sys.exit(0)
    
    elif args.command == "hpc-status":
        hpc = HPCConnection(args.config)
        if not hpc.setup_connection():
            print("\n❌ Failed to connect to HPC")
            sys.exit(1)
            
        status = hpc.check_job_status(args.job_id)
        if status:
            print(f"\nJob {args.job_id} status: {status}")
            if status == "COMPLETED":
                print("\n✅ Job completed successfully")
                print("You can download results using:")
                print(f"  toxolib hpc-download --job-id {args.job_id} --output-dir /path/to/local/dir")
            elif status in ["FAILED", "CANCELLED", "TIMEOUT", "NODE_FAIL"]:
                print("\n❌ Job failed")
            elif status in ["RUNNING", "PENDING", "CONFIGURING"]:
                print("\n⏳ Job is still running")
        else:
            print(f"\n❌ Could not get status for job {args.job_id}")
        sys.exit(0)
        
    elif args.command == "hpc-download":
        result = download_results(args.job_id, args.output_dir, args.config, no_persist=args.no_persist)
        if result:
            print(f"\n✅ Results downloaded successfully to {result}")
        else:
            print("\n❌ Failed to download results")
        sys.exit(0)
        
    elif args.command == "hpc-logs":
        print(f"\n📋 Retrieving logs for job {args.job_id}...")
        result = retrieve_job_logs(
            args.job_id, 
            args.output_dir, 
            args.log_type, 
            args.tail, 
            args.config, 
            no_persist=args.no_persist
        )
        if not result:
            print("\n❌ Failed to retrieve logs")
            print("\nTry running with a different log-type or check if the job ID is correct.")
        sys.exit(0)
        
    elif args.command == "hpc-details":
        print(f"\n📋 Getting detailed information for job {args.job_id}...")
        from .hpc import get_job_details
        job_details = get_job_details(
            args.job_id,
            args.config,
            no_persist=args.no_persist
        )
        if job_details:
            print(f"\n✅ Job {args.job_id} details:")
            print("="*80)
            # Print job details in a formatted way
            for key, value in job_details.items():
                print(f"{key:20}: {value}")
            print("="*80)
            
            # Provide interpretation of job status
            if 'State' in job_details:
                state = job_details['State']
                if state in ["COMPLETED", "COMPLETING"]:
                    print("\n✅ Job completed successfully")
                elif state in ["FAILED", "CANCELLED", "TIMEOUT", "NODE_FAIL"]:
                    print("\n❌ Job failed")
                    if 'ExitCode' in job_details:
                        exit_code = job_details['ExitCode']
                        print(f"Exit code: {exit_code}")
                        if exit_code == "0:0":
                            print("The job exited normally but may have been cancelled by the scheduler.")
                        else:
                            print("The job exited with an error. Check the logs for more details.")
                elif state in ["RUNNING", "PENDING", "CONFIGURING"]:
                    print("\n⏳ Job is still running")
        else:
            print(f"\n❌ Could not get details for job {args.job_id}")
        sys.exit(0)
        
    elif args.command == "hpc-pwd":
        # Connect to HPC
        hpc_conn = HPCConnection(args.config, no_persist=args.no_persist)
        if not hpc_conn.setup_connection():
            print("\n❌ Failed to connect to HPC")
            sys.exit(1)
            
        # Get current working directory
        current_dir = hpc_conn.get_current_directory()
        if current_dir:
            print(f"\n✅ Current HPC working directory: {current_dir}")
        else:
            print("\n❌ Failed to get current working directory")
            
        # Interactive shell functionality removed to simplify the HPC workflow
            
        # Keep connection alive for future commands
        # Don't call sys.exit(0) to allow connections to persist
        
    elif args.command == "hpc-mkdir":
        # Connect to HPC
        hpc_conn = HPCConnection(args.config, no_persist=args.no_persist)
        if not hpc_conn.setup_connection():
            print("\n❌ Failed to connect to HPC")
            sys.exit(1)
            
        # Create directory
        success = hpc_conn.create_directory(args.path, parents=args.parents)
        if success:
            print(f"\n✅ Directory created successfully: {args.path}")
        else:
            print(f"\n❌ Failed to create directory: {args.path}")
            
        # Interactive shell functionality removed to simplify the HPC workflow
            
        # Keep connection alive for future commands
        # Don't call sys.exit(0) to allow connections to persist
        
    elif args.command == "hpc-cd":
        # Connect to HPC
        hpc_conn = HPCConnection(args.config, no_persist=args.no_persist)
        if not hpc_conn.setup_connection():
            print("\n❌ Failed to connect to HPC")
            sys.exit(1)
            
        # Change directory
        new_dir = hpc_conn.change_directory(args.path)
        if new_dir:
            print(f"\n✅ Changed directory to: {new_dir}")
        else:
            print(f"\n❌ Failed to change directory to: {args.path}")
            
        # Interactive shell functionality removed to simplify the HPC workflow
            
        # Keep connection alive for future commands
        # Don't call sys.exit(0) to allow connections to persist
        
    elif args.command == "hpc-ls":
        # Connect to HPC
        hpc_conn = HPCConnection(args.config, no_persist=args.no_persist)
        if not hpc_conn.setup_connection():
            print("\n❌ Failed to connect to HPC")
            sys.exit(1)
            
        # List directory
        files = hpc_conn.list_directory(args.path, long_format=args.long, show_hidden=args.all)
        if files is not None:
            # Get current directory for display
            current_dir = args.path if args.path else hpc_conn.get_current_directory()
            print(f"\n✅ Contents of {current_dir}:")
            for item in files:
                print(item)
        else:
            path_display = args.path if args.path else "current directory"
            print(f"\n❌ Failed to list contents of: {path_display}")
            
        # Interactive shell functionality removed to simplify the HPC workflow
            
        # Keep connection alive for future commands
        # Don't call sys.exit(0) to allow connections to persist
        
    elif args.command == "hpc-shell":
        # Connect to HPC
        hpc_conn = HPCConnection(args.config)
        if not hpc_conn.setup_connection():
            print("\n❌ Failed to connect to HPC")
            sys.exit(1)
            
        # Interactive shell functionality removed to simplify the HPC workflow
        print("\n⚠️ The interactive shell has been removed to simplify the HPC workflow.")
        print("Please use the standard HPC commands instead:")
        print("  - toxolib hpc-pwd: Print working directory")
        print("  - toxolib hpc-cd: Change directory")
        print("  - toxolib hpc-ls: List files")
        print("  - toxolib hpc-mkdir: Create directory")
        print("  - toxolib hpc: Submit jobs to HPC")
        
        # Keep connection alive for future commands
        # Don't call sys.exit(0) to allow connections to persist
        
    elif args.command == "db-setup":
        # Check if at least one database is selected
        if not args.kraken and not args.corn:
            print("\n❌ Please specify at least one database to set up (--kraken or --corn)")
            sys.exit(1)
            
        if args.hpc:
            # Setup databases on HPC
            
            # Create HPC connection
            hpc = HPCConnection(config_file=args.config, no_persist=args.no_persist)
            if not hpc.setup_connection():
                print("\n❌ Failed to connect to HPC")
                sys.exit(1)
                
            # Create output directory on HPC
            if not hpc.execute_command(f"mkdir -p {args.output_dir}"):
                print(f"\n❌ Failed to create directory {args.output_dir} on HPC")
                sys.exit(1)
                
            # Setup databases locally first
            temp_dir = tempfile.mkdtemp()
            kraken_db_dir, corn_db_dir = setup_databases(
                temp_dir,
                setup_kraken=args.kraken,
                setup_corn=args.corn,
                force=args.force
            )
            
            # Upload databases to HPC
            print("\n📤 Uploading databases to HPC...")
            if args.kraken and kraken_db_dir:
                hpc_kraken_dir = os.path.join(args.output_dir, "Kraken2_DB")
                print(f"Uploading Kraken2 database to {hpc_kraken_dir}...")
                if not hpc.execute_command(f"mkdir -p {hpc_kraken_dir}"):
                    print(f"\n❌ Failed to create directory {hpc_kraken_dir} on HPC")
                else:
                    # Upload directory contents
                    for root, dirs, files in os.walk(kraken_db_dir):
                        for file in files:
                            local_file = os.path.join(root, file)
                            rel_path = os.path.relpath(local_file, kraken_db_dir)
                            remote_file = os.path.join(hpc_kraken_dir, rel_path)
                            remote_dir = os.path.dirname(remote_file)
                            hpc.execute_command(f"mkdir -p {remote_dir}")
                            hpc.upload_file(local_file, remote_file)
                    print(f"✅ Kraken2 database uploaded to HPC at {hpc_kraken_dir}")
                    hpc_kraken_db_dir = hpc_kraken_dir
            
            if args.corn and corn_db_dir:
                hpc_corn_dir = os.path.join(args.output_dir, "corn_db")
                print(f"Uploading corn genome database to {hpc_corn_dir}...")
                if not hpc.execute_command(f"mkdir -p {hpc_corn_dir}"):
                    print(f"\n❌ Failed to create directory {hpc_corn_dir} on HPC")
                else:
                    # Upload directory contents
                    for root, dirs, files in os.walk(corn_db_dir):
                        for file in files:
                            local_file = os.path.join(root, file)
                            rel_path = os.path.relpath(local_file, corn_db_dir)
                            remote_file = os.path.join(hpc_corn_dir, rel_path)
                            remote_dir = os.path.dirname(remote_file)
                            hpc.execute_command(f"mkdir -p {remote_dir}")
                            hpc.upload_file(local_file, remote_file)
                    print(f"✅ Corn genome database uploaded to HPC at {hpc_corn_dir}")
                    hpc_corn_db_dir = hpc_corn_dir
            
            # Clean up temp directory
            shutil.rmtree(temp_dir)
            
            # Close connection if requested
            if args.no_persist:
                hpc.close_connection(force=True)
            
            # Print summary
            print("\n✅ Database setup on HPC complete")
            if args.kraken:
                print(f"Kraken2 database: {hpc_kraken_dir}")
            if args.corn:
                print(f"Corn genome database: {hpc_corn_dir}")
        else:
            # Create output directory if it doesn't exist
            os.makedirs(args.output_dir, exist_ok=True)
            
            # Setup databases locally
            kraken_db_dir, corn_db_dir = setup_databases(
                args.output_dir,
                setup_kraken=args.kraken,
                setup_corn=args.corn,
                force=args.force
            )
            
            # Print summary
            print("\n✅ Database setup complete")
            if args.kraken and kraken_db_dir:
                print(f"Kraken2 database: {kraken_db_dir}")
                print(f"Set KRAKEN2_DB_DIR environment variable to: {os.path.dirname(kraken_db_dir)}")
            if args.corn and corn_db_dir:
                print(f"Corn genome database: {corn_db_dir}")
    
    elif args.command == "hpc":
        # Check if raw files exist
        for raw_file in args.raw_files:
            if not os.path.exists(raw_file):
                logging.error(f"Raw file {raw_file} does not exist")
                sys.exit(1)
                
        # Run on HPC
        job_id = run_on_hpc(
            args.raw_files,
            args.output_dir,
            kraken_db_dir=args.kraken_db,
            corn_db_dir=args.corn_db,
            config_file=args.config,
            partition=args.partition,
            threads=args.threads,
            memory=args.memory,
            time=args.time,
            setup_kraken_db=args.setup_kraken_db,
            setup_corn_db=args.setup_corn_db
        )
        
        if job_id:
            print(f"\n✅ Job submitted successfully with ID: {job_id}")
            print("\nYou can check job status using:")
            print(f"  toxolib hpc-status --job-id {job_id}")
            print("\nAnd download results when complete using:")
            print(f"  toxolib hpc-download --job-id {job_id} --output-dir /path/to/local/dir")
        else:
            print("\n❌ Failed to submit job to HPC")
        sys.exit(0)
    
    # Check dependencies for local commands
    if args.command in ["abundance", "matrix"] and not check_dependencies():
        logging.error("Missing required dependencies. Please install them before proceeding.")
        print("\nTip: You can install all dependencies using the provided conda environment:")
        print("  conda env create -f environment.yml")
        print("  conda activate taxonomy_env")
        sys.exit(1)
    
    # Handle commands
    if args.command == "abundance":
        # Check if raw files exist
        for raw_file in args.raw_files:
            if not os.path.exists(raw_file):
                logging.error(f"Raw file {raw_file} does not exist")
                sys.exit(1)
        
        # Process raw data
        try:
            logging.info(f"Starting taxonomic profiling for {len(args.raw_files)} input files...")
            logging.info(f"Output will be saved to: {args.output_dir}")
            
            abundance_file = process_raw_data(
                args.raw_files, args.output_dir, args.threads
            )
            
            logging.info(f"Abundance matrix generated: {abundance_file}")
            print(f"\n✅ Process completed successfully!")
            print(f"Abundance matrix saved to: {abundance_file}")
            print(f"Check the logs directory for detailed information.")
            
        except Exception as e:
            logging.error(f"Error generating abundance matrix: {e}")
            sys.exit(1)
    
    elif args.command == "matrix":
        # Check if input files exist
        for input_file in args.input_files:
            if not os.path.exists(input_file):
                logging.error(f"Input file {input_file} does not exist")
                sys.exit(1)
        
        # Create abundance matrix
        try:
            logging.info(f"Creating abundance matrix from {len(args.input_files)} Bracken files...")
            create_abundance_matrix(args.input_files, args.output)
            
            logging.info(f"Abundance matrix created: {args.output}")
            print(f"\n✅ Abundance matrix created successfully: {args.output}")
            
        except Exception as e:
            logging.error(f"Error creating abundance matrix: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
