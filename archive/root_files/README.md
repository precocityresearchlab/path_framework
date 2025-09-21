---
created_date: 2025-09-21
created_by: PATH Framework Team
last_modified: 2025-09-21
version: 1.0.0
purpose: Documentation for archived root-level files that were moved to maintain clean project structure
framework_phase: N/A
dependencies: [PATH Framework cleanup]
status: archived
tags: [archive, cleanup, root-files, legacy]
---

# Archived Root Files

![Status](https://img.shields.io/badge/Status-Archived-red?style=flat-square)
![Framework](https://img.shields.io/badge/Framework-PATH-orange?style=flat-square)
![Version](https://img.shields.io/badge/Version-1.0.0-blue?style=flat-square)

This directory contains files that were previously in the root directory but have been archived to maintain a clean project structure following PATH Framework standards.

## Archive Structure

### `/demos/`
Demo and example files that were used for testing and demonstration:
- `demo_phase1_output.py` - Phase 1 output demonstration
- `demo_proper_projects.py` - Proper project structure demo
- `demo_real_llm.py` - Real LLM integration demo

### `/experimental/`
Experimental and development files:
- `direct_llm_architecture.py` - Direct LLM architecture experiments
- `test_gemma_llm.py` - Gemma LLM testing
- `path_generate.py` - PATH generation utilities
- `generate_path_artifacts.py` - Artifact generation scripts

### `/legacy/`
Legacy files and backups:
- `projects_backup_*.tar.gz` - Project backups
- `project-folders.log` - Project folder logs
- `dependency-report.txt` - Dependency reports
- `coverage.xml` - Coverage reports
- `Dockerfile` - Legacy Docker configuration (use `/docker/` instead)
- `docker-compose.yml` - Legacy Docker Compose (use `/docker/` instead)

## Rationale for Archiving

These files were moved to maintain:
1. **Clean Root Structure**: Keep root directory focused on essential project files
2. **PATH Framework Standards**: Follow established organizational patterns
3. **Clear Separation**: Distinguish between active and experimental code
4. **Documentation Compliance**: Ensure all files follow metadata standards

## Recovery

If any of these files are needed:
1. They remain accessible in this archive
2. Can be moved back to root if required
3. Should be updated to follow current PATH Framework standards before reactivation

## Archive Date
**Archived**: 2025-09-21
**Reason**: Root directory cleanup and PATH Framework standardization