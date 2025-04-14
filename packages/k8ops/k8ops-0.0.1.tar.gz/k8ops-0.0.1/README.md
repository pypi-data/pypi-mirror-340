# k8ops - Kubernetes Operations Tools

[![Publish Python Package to PyPI](https://github.com/nomagicln/k8ops/actions/workflows/publish-to-pypi.yml/badge.svg?branch=main)](https://github.com/nomagicln/k8ops/actions/workflows/publish-to-pypi.yml)

A collection of tools to help with Kubernetes cluster operations and management.

## Installation

You can install k8ops using pip:

```bash
pip install k8ops
```

Or using uv:

```bash
uv pip install k8ops
```

Alternatively, you can download and use the standalone scripts directly from the repository.

## Node Drain Analyzer

The Node Drain Analyzer is a tool that helps you assess the impact and risk of draining nodes in your Kubernetes cluster. It analyzes various factors such as resource usage, pod placement constraints, and node characteristics to provide insights into potential issues that might arise when draining specific nodes.

### Features

- Comprehensive analysis of node drain impact
- Resource usage evaluation (CPU, memory, pods)
- Detection of scheduling constraints (taints, tolerations, node selectors)
- Architecture and operating system compatibility checks
- Detailed reporting with severity levels
- Multiple output formats (table, JSON, CSV)

### Requirements

- Python 3.6+
- `kubectl` configured with access to your Kubernetes cluster
- Required Python packages (standard library)

### Usage

If installed via pip:

```bash
node-drain-analyzer [options] [node_names...]
```

If using the standalone script:

```bash
python node-drain-analyzer [options] [node_names...]
```

#### Options

- `--wide`: Show wide output with additional columns
- `--output`, `-o`: Output destination (default: stdout)
- `--verbose`, `-v`: Enable verbose output
- `--images`: Show images information
- `--pods`: Show pods information
- `--taints`: Show taints information
- `--metrics`: Show metrics information
- `--factor`: The factor for resource calculations (default: 1.5)

#### Examples

Analyze the impact of draining a single node:

```bash
node-drain-analyzer node-1
```

Analyze multiple nodes with verbose output:

```bash
node-drain-analyzer -v node-1 node-2
```

Show detailed information including pods and taints:

```bash
node-drain-analyzer --pods --taints node-1
```

Save analysis to a file:

```bash
node-drain-analyzer -o analysis.txt node-1
```

### How It Works

1. Collects information about all nodes and pods in the cluster
2. Simulates removing the specified nodes
3. Analyzes the impact on the remaining nodes
4. Checks for potential issues like:
   - Resource constraints
   - Pod scheduling constraints
   - Architecture/OS compatibility
   - Taints and tolerations
5. Generates a report with severity levels for identified issues

### Severity Levels

- **High**: Critical issues that will likely prevent successful node draining
- **Medium**: Significant issues that may cause problems
- **Low**: Minor issues that should be reviewed
- **None**: No issues detected

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)
