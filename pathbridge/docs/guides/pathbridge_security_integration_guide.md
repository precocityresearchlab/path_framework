# PathBridge Security Integration Guide

## Overview

PathBridge security system provides comprehensive security analysis, vulnerability scanning, and compliance validation for AI-generated code and infrastructure.

**Security Capabilities:**
- **SAST Scanning**: Static application security testing
- **Secrets Detection**: Hardcoded credentials and sensitive data detection
- **Dependency Scanning**: Third-party vulnerability analysis
- **Compliance Validation**: OWASP, CIS, GDPR, HIPAA compliance
- **Threat Modeling**: Automated security risk assessment

## Quick Start

### 1. Basic Security Scanning

```python
from pathbridge.security.security_engine import SecurityAnalysisEngine, SecurityRequest

async def basic_security_scan():
    security_engine = SecurityAnalysisEngine()
    
    # Create security scan request
    request = SecurityRequest(
        scan_type="comprehensive",
        target_path="src/",
        include_dependencies=True,
        compliance_frameworks=["owasp", "cis"],
        severity_threshold="medium"
    )
    
    # Execute security scan
    result = await security_engine.analyze_security(request)
    
    print(f"Vulnerabilities found: {len(result.vulnerabilities)}")
    print(f"Security score: {result.security_score}/100")
    print(f"Compliance status: {result.compliance_status}")
    
    # Process high-severity issues
    critical_issues = [v for v in result.vulnerabilities if v.severity == "critical"]
    for issue in critical_issues:
        print(f"CRITICAL: {issue.title} in {issue.file_path}:{issue.line_number}")
    
    return result
```

### 2. Integration with PATH Agents

```python
from pathbridge.agents.base_agent import CoreAgent
from pathbridge.security.security_engine import SecurityAnalysisEngine

class SecurityValidatedAgent(CoreAgent):
    def __init__(self, agent_id: str, phase: int, capabilities: List[str]):
        super().__init__(agent_id, phase, capabilities)
        self.security_engine = SecurityAnalysisEngine()
    
    async def execute_with_security_validation(self, request: CapabilityRequest) -> CapabilityResponse:
        # Execute capability
        result = await self.execute_capability(request)
        
        # Perform security validation on generated code
        if result.success and "generated_code" in result.result:
            security_result = await self._validate_code_security(
                code=result.result["generated_code"],
                context=request.context
            )
            
            # Block execution if critical security issues found
            if security_result.has_critical_issues:
                return CapabilityResponse(
                    success=False,
                    result={},
                    errors=[f"Critical security issues found: {security_result.critical_issues}"],
                    warnings=security_result.warnings,
                    execution_time_ms=result.execution_time_ms,
                    metadata={"security_blocked": True, "security_score": security_result.security_score}
                )
            
            # Add security metadata to successful result
            result.metadata.update({
                "security_validated": True,
                "security_score": security_result.security_score,
                "vulnerabilities_found": len(security_result.vulnerabilities)
            })
        
        return result
    
    async def _validate_code_security(self, code: str, context: Dict[str, Any]) -> SecurityResult:
        """Validate generated code for security issues"""
        request = SecurityRequest(
            scan_type="code_analysis",
            code_content=code,
            language=context.get("language", "python"),
            severity_threshold="low"
        )
        
        return await self.security_engine.analyze_code_security(request)
```

## Static Application Security Testing (SAST)

### Code Vulnerability Scanning

```python
from pathbridge.security.sast import StaticAnalysisSecurityTester

async def comprehensive_sast_scan():
    sast_scanner = StaticAnalysisSecurityTester()
    
    # Configure scan parameters
    scan_config = {
        "target_directory": "src/",
        "languages": ["python", "javascript", "java"],
        "rule_sets": ["owasp_top_10", "cwe_top_25", "custom_rules"],
        "exclude_patterns": ["tests/", "*.min.js", "node_modules/"],
        "severity_levels": ["critical", "high", "medium", "low"]
    }
    
    # Execute SAST scan
    sast_result = await sast_scanner.scan_source_code(scan_config)
    
    # Process results by category
    vulnerability_categories = {
        "injection": [],
        "authentication": [],
        "sensitive_data": [],
        "xml_external_entities": [],
        "broken_access_control": [],
        "security_misconfiguration": [],
        "cross_site_scripting": [],
        "insecure_deserialization": [],
        "known_vulnerabilities": [],
        "insufficient_logging": []
    }
    
    for vulnerability in sast_result.vulnerabilities:
        category = vulnerability.owasp_category.lower().replace(" ", "_")
        if category in vulnerability_categories:
            vulnerability_categories[category].append(vulnerability)
    
    # Generate remediation suggestions
    remediation_plan = await sast_scanner.generate_remediation_plan(sast_result)
    
    return {
        "scan_result": sast_result,
        "categorized_vulnerabilities": vulnerability_categories,
        "remediation_plan": remediation_plan
    }
```

### Language-Specific Security Rules

```python
class PythonSecurityRules:
    """Python-specific security validation rules"""
    
    async def validate_python_code(self, code: str) -> List[SecurityIssue]:
        issues = []
        
        # Check for SQL injection vulnerabilities
        if self._has_sql_injection_risk(code):
            issues.append(SecurityIssue(
                title="Potential SQL Injection",
                severity="high",
                description="String concatenation used in SQL query",
                remediation="Use parameterized queries or ORM",
                cwe_id="CWE-89"
            ))
        
        # Check for command injection
        if self._has_command_injection_risk(code):
            issues.append(SecurityIssue(
                title="Command Injection Risk",
                severity="critical",
                description="User input passed to system command",
                remediation="Validate and sanitize input, use subprocess with shell=False",
                cwe_id="CWE-78"
            ))
        
        # Check for hardcoded secrets
        secrets = self._detect_hardcoded_secrets(code)
        for secret in secrets:
            issues.append(SecurityIssue(
                title="Hardcoded Secret",
                severity="high",
                description=f"Potential {secret.type} found in code",
                remediation="Use environment variables or secure vault",
                cwe_id="CWE-798"
            ))
        
        return issues
    
    def _has_sql_injection_risk(self, code: str) -> bool:
        """Detect potential SQL injection patterns"""
        sql_injection_patterns = [
            r'execute\s*\(\s*["\'].*%.*["\']',  # String formatting in SQL
            r'cursor\.execute\s*\(\s*f["\']',    # f-string in SQL
            r'query\s*=\s*["\'].*\+.*["\']'      # String concatenation
        ]
        
        return any(re.search(pattern, code) for pattern in sql_injection_patterns)
```

## Secrets Detection

### Comprehensive Secrets Scanning

```python
from pathbridge.security.secrets import SecretsDetectionEngine

async def detect_secrets():
    secrets_detector = SecretsDetectionEngine()
    
    # Configure detection rules
    detection_config = {
        "target_paths": ["src/", "config/", "scripts/"],
        "secret_types": [
            "api_keys", "passwords", "tokens", "certificates",
            "database_urls", "private_keys", "oauth_secrets"
        ],
        "entropy_threshold": 4.5,
        "exclude_files": [".git/", "*.log", "*.pyc"],
        "custom_patterns": [
            r"CUSTOM_API_KEY_[A-Za-z0-9]{32}",
            r"sk-[A-Za-z0-9]{48}"  # OpenAI API key pattern
        ]
    }
    
    # Execute secrets detection
    secrets_result = await secrets_detector.scan_for_secrets(detection_config)
    
    # Categorize findings
    secrets_by_type = {}
    for secret in secrets_result.detected_secrets:
        secret_type = secret.secret_type
        if secret_type not in secrets_by_type:
            secrets_by_type[secret_type] = []
        secrets_by_type[secret_type].append(secret)
    
    # Generate remediation recommendations
    remediation_steps = []
    for secret_type, secrets in secrets_by_type.items():
        remediation_steps.append({
            "secret_type": secret_type,
            "count": len(secrets),
            "remediation": secrets_detector.get_remediation_for_type(secret_type),
            "affected_files": list(set(s.file_path for s in secrets))
        })
    
    return {
        "total_secrets": len(secrets_result.detected_secrets),
        "secrets_by_type": secrets_by_type,
        "remediation_steps": remediation_steps,
        "risk_score": secrets_result.risk_score
    }
```

### Real-time Secrets Prevention

```python
class SecretsPreventionHook:
    """Prevent secrets from being committed"""
    
    def __init__(self):
        self.secrets_detector = SecretsDetectionEngine()
    
    async def pre_commit_hook(self, staged_files: List[str]) -> bool:
        """Check staged files for secrets before commit"""
        
        secrets_found = []
        
        for file_path in staged_files:
            file_content = await self._read_file(file_path)
            
            # Quick entropy-based check
            if self._has_high_entropy_strings(file_content):
                detailed_scan = await self.secrets_detector.scan_content(
                    content=file_content,
                    file_path=file_path
                )
                
                if detailed_scan.secrets_found:
                    secrets_found.extend(detailed_scan.secrets_found)
        
        if secrets_found:
            print("🚨 SECRETS DETECTED - COMMIT BLOCKED")
            for secret in secrets_found:
                print(f"  {secret.file_path}:{secret.line_number} - {secret.secret_type}")
            
            return False  # Block commit
        
        return True  # Allow commit
```

## Dependency Security Scanning

### Third-Party Vulnerability Analysis

```python
from pathbridge.security.dependencies import DependencySecurityScanner

async def scan_dependencies():
    dependency_scanner = DependencySecurityScanner()
    
    # Scan different package managers
    scan_results = {}
    
    # Python dependencies
    if await dependency_scanner.has_requirements_file():
        python_scan = await dependency_scanner.scan_python_dependencies(
            requirements_file="requirements.txt",
            include_dev_dependencies=True
        )
        scan_results["python"] = python_scan
    
    # Node.js dependencies
    if await dependency_scanner.has_package_json():
        nodejs_scan = await dependency_scanner.scan_nodejs_dependencies(
            package_file="package.json",
            include_dev_dependencies=False
        )
        scan_results["nodejs"] = nodejs_scan
    
    # Java dependencies
    if await dependency_scanner.has_pom_xml():
        java_scan = await dependency_scanner.scan_java_dependencies(
            pom_file="pom.xml"
        )
        scan_results["java"] = java_scan
    
    # Aggregate results
    total_vulnerabilities = sum(len(result.vulnerabilities) for result in scan_results.values())
    critical_vulnerabilities = sum(
        len([v for v in result.vulnerabilities if v.severity == "critical"])
        for result in scan_results.values()
    )
    
    # Generate update recommendations
    update_recommendations = []
    for ecosystem, result in scan_results.items():
        for vulnerability in result.vulnerabilities:
            if vulnerability.fixed_version:
                update_recommendations.append({
                    "ecosystem": ecosystem,
                    "package": vulnerability.package_name,
                    "current_version": vulnerability.current_version,
                    "fixed_version": vulnerability.fixed_version,
                    "severity": vulnerability.severity,
                    "cve_id": vulnerability.cve_id
                })
    
    return {
        "scan_results": scan_results,
        "total_vulnerabilities": total_vulnerabilities,
        "critical_vulnerabilities": critical_vulnerabilities,
        "update_recommendations": update_recommendations
    }
```

## Compliance Validation

### Multi-Framework Compliance Checking

```python
from pathbridge.security.compliance import ComplianceFrameworkValidator

async def validate_compliance():
    compliance_validator = ComplianceFrameworkValidator()
    
    # Define compliance requirements
    compliance_frameworks = {
        "owasp": {
            "version": "2021",
            "categories": ["A01", "A02", "A03", "A04", "A05", "A06", "A07", "A08", "A09", "A10"]
        },
        "cis": {
            "version": "1.1",
            "controls": ["access_control", "data_protection", "logging", "monitoring"]
        },
        "gdpr": {
            "requirements": ["data_minimization", "consent", "right_to_erasure", "data_portability"]
        },
        "hipaa": {
            "safeguards": ["administrative", "physical", "technical"]
        }
    }
    
    compliance_results = {}
    
    for framework, config in compliance_frameworks.items():
        result = await compliance_validator.validate_framework_compliance(
            framework=framework,
            config=config,
            target_path="src/",
            include_infrastructure=True
        )
        
        compliance_results[framework] = {
            "compliance_score": result.compliance_score,
            "passed_controls": result.passed_controls,
            "failed_controls": result.failed_controls,
            "recommendations": result.recommendations
        }
    
    # Generate compliance report
    overall_compliance = await compliance_validator.generate_compliance_report(
        compliance_results
    )
    
    return {
        "framework_results": compliance_results,
        "overall_compliance": overall_compliance,
        "action_items": overall_compliance.priority_actions
    }
```

### GDPR Compliance Validation

```python
class GDPRComplianceValidator:
    """GDPR-specific compliance validation"""
    
    async def validate_gdpr_compliance(self, codebase_path: str) -> GDPRComplianceResult:
        """Validate GDPR compliance requirements"""
        
        compliance_checks = {
            "data_minimization": await self._check_data_minimization(codebase_path),
            "consent_management": await self._check_consent_management(codebase_path),
            "right_to_erasure": await self._check_data_deletion(codebase_path),
            "data_portability": await self._check_data_export(codebase_path),
            "privacy_by_design": await self._check_privacy_by_design(codebase_path),
            "data_protection_impact": await self._check_dpia_requirements(codebase_path)
        }
        
        # Calculate compliance score
        passed_checks = sum(1 for check in compliance_checks.values() if check.passed)
        compliance_score = (passed_checks / len(compliance_checks)) * 100
        
        # Generate recommendations
        recommendations = []
        for check_name, result in compliance_checks.items():
            if not result.passed:
                recommendations.extend(result.recommendations)
        
        return GDPRComplianceResult(
            compliance_score=compliance_score,
            checks=compliance_checks,
            recommendations=recommendations,
            risk_level=self._calculate_gdpr_risk_level(compliance_score)
        )
```

## Threat Modeling

### Automated Security Risk Assessment

```python
from pathbridge.security.threat_modeling import ThreatModelingEngine

async def perform_threat_modeling():
    threat_modeler = ThreatModelingEngine()
    
    # Analyze system architecture
    architecture_analysis = await threat_modeler.analyze_system_architecture(
        architecture_file="docs/architecture.md",
        code_path="src/",
        infrastructure_path="infrastructure/"
    )
    
    # Identify threat vectors
    threat_vectors = await threat_modeler.identify_threat_vectors(
        architecture=architecture_analysis,
        threat_categories=["STRIDE", "OWASP_Top_10", "Cloud_Security"]
    )
    
    # Assess risk levels
    risk_assessment = await threat_modeler.assess_risks(
        threats=threat_vectors,
        business_context={
            "data_sensitivity": "high",
            "user_base_size": "large",
            "regulatory_requirements": ["gdpr", "hipaa"]
        }
    )
    
    # Generate mitigation strategies
    mitigation_strategies = await threat_modeler.generate_mitigation_strategies(
        risks=risk_assessment.high_risk_threats
    )
    
    return {
        "architecture_analysis": architecture_analysis,
        "identified_threats": len(threat_vectors),
        "high_risk_threats": len(risk_assessment.high_risk_threats),
        "mitigation_strategies": mitigation_strategies,
        "overall_risk_score": risk_assessment.overall_risk_score
    }
```

## Security Remediation

### Automated Fix Generation

```python
from pathbridge.security.remediation import SecurityRemediationEngine

async def generate_security_fixes():
    remediation_engine = SecurityRemediationEngine()
    
    # Get security scan results
    security_scan = await perform_security_scan()
    
    # Generate fixes for each vulnerability
    remediation_results = []
    
    for vulnerability in security_scan.vulnerabilities:
        if vulnerability.severity in ["critical", "high"]:
            fix_suggestion = await remediation_engine.generate_fix(
                vulnerability=vulnerability,
                context={
                    "language": vulnerability.language,
                    "framework": vulnerability.framework,
                    "file_content": await read_file(vulnerability.file_path)
                }
            )
            
            if fix_suggestion.auto_fixable:
                # Apply automatic fix
                fix_result = await remediation_engine.apply_fix(
                    file_path=vulnerability.file_path,
                    fix_suggestion=fix_suggestion,
                    create_backup=True
                )
                
                remediation_results.append({
                    "vulnerability_id": vulnerability.id,
                    "fix_applied": fix_result.success,
                    "fix_type": "automatic",
                    "backup_created": fix_result.backup_path
                })
            else:
                # Generate manual fix instructions
                manual_instructions = await remediation_engine.generate_manual_fix_instructions(
                    vulnerability=vulnerability,
                    fix_suggestion=fix_suggestion
                )
                
                remediation_results.append({
                    "vulnerability_id": vulnerability.id,
                    "fix_applied": False,
                    "fix_type": "manual",
                    "instructions": manual_instructions
                })
    
    return {
        "total_vulnerabilities": len(security_scan.vulnerabilities),
        "auto_fixed": len([r for r in remediation_results if r["fix_applied"]]),
        "manual_fixes_required": len([r for r in remediation_results if not r["fix_applied"]]),
        "remediation_details": remediation_results
    }
```

## Configuration

### Security Settings

```bash
# Security Scanning Settings
PATH_SECURITY_ENABLED=true
PATH_SECURITY_SCAN_ON_COMMIT=true
PATH_SECURITY_BLOCK_ON_CRITICAL=true
PATH_SECURITY_SEVERITY_THRESHOLD=medium

# SAST Configuration
PATH_SAST_ENABLED=true
PATH_SAST_RULE_SETS=owasp_top_10,cwe_top_25
PATH_SAST_EXCLUDE_PATTERNS=tests/,*.min.js,node_modules/

# Secrets Detection
PATH_SECRETS_DETECTION_ENABLED=true
PATH_SECRETS_ENTROPY_THRESHOLD=4.5
PATH_SECRETS_BLOCK_COMMITS=true

# Dependency Scanning
PATH_DEPENDENCY_SCAN_ENABLED=true
PATH_DEPENDENCY_INCLUDE_DEV=false
PATH_DEPENDENCY_AUTO_UPDATE=false

# Compliance Validation
PATH_COMPLIANCE_FRAMEWORKS=owasp,cis
PATH_COMPLIANCE_REQUIRED_SCORE=80
```

## Testing Security Integration

```python
import pytest
from pathbridge.security.security_engine import SecurityAnalysisEngine

@pytest.mark.asyncio
async def test_security_vulnerability_detection():
    """Test security vulnerability detection"""
    security_engine = SecurityAnalysisEngine()
    
    # Test code with known vulnerability
    vulnerable_code = """
import sqlite3

def get_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # SQL Injection vulnerability
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    return cursor.fetchone()
"""
    
    # Scan for vulnerabilities
    result = await security_engine.analyze_code_security(
        SecurityRequest(
            scan_type="code_analysis",
            code_content=vulnerable_code,
            language="python"
        )
    )
    
    # Verify vulnerability detected
    assert len(result.vulnerabilities) > 0
    sql_injection_found = any(
        "sql injection" in vuln.title.lower()
        for vuln in result.vulnerabilities
    )
    assert sql_injection_found
```

## Best Practices

### Security Guidelines

1. **Shift Left Security**: Integrate security scanning early in development
2. **Continuous Monitoring**: Run security scans on every commit
3. **Risk-Based Approach**: Prioritize fixes based on risk assessment
4. **Compliance Automation**: Automate compliance validation
5. **Security Training**: Educate developers on secure coding practices
6. **Incident Response**: Have clear procedures for security incidents

### Performance Optimization

```python
# Parallel security scanning
async def parallel_security_scan():
    security_engine = SecurityAnalysisEngine()
    
    # Run different scan types concurrently
    tasks = [
        security_engine.sast_scan("src/"),
        security_engine.secrets_scan("src/"),
        security_engine.dependency_scan("requirements.txt"),
        security_engine.compliance_scan("src/")
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Combine results
    combined_result = SecurityResult()
    for result in results:
        if not isinstance(result, Exception):
            combined_result.merge(result)
    
    return combined_result
```