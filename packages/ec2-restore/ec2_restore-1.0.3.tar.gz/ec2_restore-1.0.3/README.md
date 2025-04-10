# EC2 Restore Tool

A powerful command-line tool for restoring EC2 instances from AMIs with advanced features and detailed reporting.

## Features

- **Full Instance Restore**: Create a new instance from an AMI while preserving network configuration
- **Volume-Level Restore**: Restore specific volumes from an AMI to an existing instance
- **Detailed Progress Tracking**: Real-time progress updates with rich console output
- **Comprehensive Reporting**: Generate detailed restoration reports
- **Network Configuration Preservation**: Maintain private IP addresses and network settings
- **Systems Manager Integration**: Execute post-restore commands using AWS Systems Manager
- **Instance Metadata Backup**: Automatic backup of instance metadata before restoration
- **Volume Change Visualization**: Clear display of volume changes before and after restoration
- **Instance Change Tracking**: Detailed comparison of instance configurations
- **Error Handling & Rollback**: Robust error handling with automatic rollback capabilities

## Installation

```bash
pip install ec2-restore
```

## Configuration

Create a `config.yaml` file in your working directory:

```yaml
aws:
  profile: default
  region: us-east-1

restore:
  max_amis: 5
  backup_metadata: true
  log_level: INFO
  log_file: ec2_restore.log

ssm:
  enabled: true
  commands:
    - command: "echo 'Test command executed'"
      timeout: 30
      wait_for_completion: true
  document_name: AWS-RunShellScript
  output_s3_bucket: ""
  output_s3_prefix: ""
```

## Usage

### Full Instance Restore

```bash
# Restore by instance ID
ec2-restore restore --instance-id i-1234567890abcdef0

# Restore by instance name
ec2-restore restore --instance-name my-instance

# Restore multiple instances
ec2-restore restore --instance-ids i-1234567890abcdef0,i-0987654321fedcba0
```

### Volume Restore

```bash
# Restore specific volumes
ec2-restore restore --instance-id i-1234567890abcdef0 --restore-type volume
```

### Options

- `--instance-id`: EC2 instance ID to restore
- `--instance-name`: EC2 instance name (tag) to restore
- `--instance-ids`: Comma-separated list of EC2 instance IDs to restore
- `--restore-type`: Type of restore (full or volume)
- `--config`: Path to configuration file (default: config.yaml)

## Development

1. Clone the repository:
```bash
git clone https://github.com/jyothishkshatri/ec2-restore.git
cd ec2-restore
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 