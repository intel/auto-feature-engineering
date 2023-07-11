# Auto Feature Engineering

![Version: 0.2.1](https://img.shields.io/badge/Version-0.2.1-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 1.16.0](https://img.shields.io/badge/AppVersion-1.16.0-informational?style=flat-square)

A Helm chart for Kubernetes

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| dataset.application | string | `"nyc_taxi_fare"` | Application name |
| dataset.local.repo_path | string | `"nil"` | Host Path to project repo Directory |
| dataset.nfs.path | string | `"nil"` | Path to Local NFS Share in Cluster Host |
| dataset.nfs.server | string | `"nil"` | Hostname of NFS Server |
| dataset.nfs.repo_path | string | `"nil"` | Path to project repo in Local NFS |
| dataset.type | string | `"<nfs/local>"` | `nfs`, or `local` Dataset input enabler |
| image.name | string | `"intel/ai-workflows:pa-autofe"` |  |
| metadata.name | string | `"auto-feature-engineering"` |  |
| proxy | string | `"nil"` |  |

