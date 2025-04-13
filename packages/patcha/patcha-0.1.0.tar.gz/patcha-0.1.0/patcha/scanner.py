import os
import sys
import json
import subprocess
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import ast
import re
from datetime import datetime
import tempfile

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("patcha")

class SecurityScanner:
    def __init__(self, repo_path: str, output_file: str):
        self.repo_path = Path(repo_path).resolve()
        self.output_file = output_file
        self.findings = []
        self.security_score = None
        
        # Verify the repository path exists
        if not self.repo_path.exists() or not self.repo_path.is_dir():
            raise ValueError(f"Repository path does not exist or is not a directory: {self.repo_path}")
            
        logger.info(f"Initializing scanner for repository: {self.repo_path}")
    
    def scan(self, target_url=None):
        """Run all security scans on the repository"""
        logger.info("Starting security scan")
        
        # Run Semgrep scan
        self._run_semgrep_scan()
        
        # Run TruffleHog scan for secrets in the repository using subprocess
        self._run_trufflehog_scan()
        
        # Run Trivy scan for dependency vulnerabilities
        self._run_trivy_scan()
        
        # Check if there are Python files and run Bandit if found
        python_files = list(self.repo_path.glob("**/*.py"))
        if python_files:
            logger.info(f"Found {len(python_files)} Python files, running Bandit scan")
            self._run_bandit_scan()
        else:
            logger.info("No Python files found, skipping Bandit scan")
        
        # Run custom Python code analysis
        if python_files:
            self._scan_python_files()
        
        # Run Nikto DAST scan if target URL is provided
        if target_url:
            self._run_nikto_scan(target_url)
        
        # Output findings
        self._save_findings()
        
        logger.info(f"Scan complete. Found {len(self.findings)} potential issues.")
        return self.findings
    
    def _run_semgrep_scan(self):
        """Run Semgrep scan for security vulnerabilities"""
        try:
            logger.info("Running Semgrep security scan")
            
            # Check if Semgrep is installed
            try:
                subprocess.run(["semgrep", "--version"], check=True, capture_output=True)
            except (subprocess.SubprocessError, FileNotFoundError):
                logger.warning("Semgrep not found. Please install with 'pip install semgrep'. Skipping Semgrep scan.")
                return
            
            # Run Semgrep with security rules and capture JSON output
            result = subprocess.run(
                ["semgrep", "--config=auto", 
                 "--json", 
                 "--quiet",
                 "--no-git-ignore",  # Don't use git ignore rules
                 str(self.repo_path)],
                capture_output=True,
                text=True
            )
            
            # Semgrep returns 0 for no findings, 1 for findings, other codes for errors
            if result.returncode in (0, 1):
                try:
                    semgrep_data = json.loads(result.stdout)
                    self._process_semgrep_findings(semgrep_data)
                except json.JSONDecodeError:
                    logger.error("Failed to parse Semgrep output")
                    logger.debug(f"Semgrep stdout: {result.stdout[:500]}...")
            else:
                logger.error(f"Semgrep scan failed with exit code {result.returncode}")
                logger.error(f"Error: {result.stderr}")
                
        except Exception as e:
            logger.error(f"Error running Semgrep scan: {str(e)}")
    
    def _run_trufflehog_scan(self):
        """Run TruffleHog scan for secrets in the repository"""
        try:
            logger.info("Running TruffleHog secrets scan")
            
            # Check if TruffleHog is installed
            try:
                subprocess.run(["trufflehog", "--help"], check=True, capture_output=True)
                logger.info("TruffleHog is installed and available")
            except (subprocess.SubprocessError, FileNotFoundError) as e:
                logger.warning(f"TruffleHog check failed: {str(e)}. Skipping secrets scan.")
                return
            
            # Run TruffleHog with filesystem mode instead of git mode
            logger.info(f"Running TruffleHog on {self.repo_path}")
            result = subprocess.run(
                ["trufflehog", "filesystem", "--json", str(self.repo_path)],
                capture_output=True,
                text=True
            )
            
            # Log the command output for debugging
            logger.debug(f"TruffleHog command exit code: {result.returncode}")
            logger.debug(f"TruffleHog stderr: {result.stderr}")
            
            if result.stdout:
                # Process the results
                self._process_trufflehog_findings_v2(result.stdout)
            else:
                logger.info("No secrets found by TruffleHog or no output produced")
                
        except Exception as e:
            logger.error(f"Error running TruffleHog scan: {str(e)}")
    
    def _run_bandit_scan(self):
        """Run Bandit scan for Python-specific security vulnerabilities"""
        try:
            logger.info("Running Bandit security scan for Python files")
            
            # Check if Bandit is installed
            try:
                subprocess.run(["bandit", "--version"], check=True, capture_output=True)
            except (subprocess.SubprocessError, FileNotFoundError):
                logger.warning("Bandit not found. Please install with 'pip3 install bandit'. Skipping Bandit scan.")
                return
            
            # Create a temporary file with a list of directories to exclude
            exclude_dirs = ["__MACOSX", "node_modules", ".git"]
            exclude_args = []
            for dir_name in exclude_dirs:
                exclude_args.extend(["-e", dir_name])
            
            # Run Bandit with JSON output format and exclusions
            result = subprocess.run(
                ["bandit", "-r"] + exclude_args + ["-f", "json", str(self.repo_path)],
                capture_output=True,
                text=True
            )
            
            # Bandit returns 0 for no issues, 1 for issues found, 2 for scan failed
            if result.returncode in (0, 1):
                try:
                    # Check if output is empty
                    if not result.stdout.strip():
                        logger.info("Bandit scan completed but found no issues")
                        return
                        
                    bandit_data = json.loads(result.stdout)
                    self._process_bandit_findings(bandit_data)
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse Bandit output: {str(e)}")
                    # Log a portion of the output to help diagnose
                    logger.debug(f"Bandit output (first 500 chars): {result.stdout[:500]}")
                else:
                    logger.error(f"Bandit scan failed with exit code {result.returncode}")
                    logger.error(f"Error: {result.stderr}")
                
        except Exception as e:
            logger.error(f"Error running Bandit scan: {str(e)}")
    
    def _process_bandit_findings(self, bandit_data: Dict):
        """Process Bandit scan results"""
        if not bandit_data.get("results"):
            logger.info("No vulnerabilities found by Bandit")
            return
            
        for result in bandit_data.get("results", []):
            # Map Bandit severity to our format
            severity_map = {
                "HIGH": "high",
                "MEDIUM": "medium",
                "LOW": "low"
            }
            severity = severity_map.get(result.get("issue_severity", "MEDIUM"), "medium")
            
            # Extract file path relative to repo
            file_path = result.get("filename", "")
            if file_path.startswith(str(self.repo_path)):
                file_path = os.path.relpath(file_path, self.repo_path)
            
            finding = {
                "source": "bandit",
                "severity": severity,
                "title": f"Bandit: {result.get('test_id', 'Unknown')} - {result.get('test_name', 'Unknown issue')}",
                "description": result.get("issue_text", "No description provided"),
                "file_path": file_path,
                "line_number": result.get("line_number"),
                "code_snippet": result.get("code", ""),
                "remediation": f"Review and fix the {result.get('test_name', 'identified')} issue",
                "metadata": {
                    "test_id": result.get("test_id"),
                    "confidence": result.get("issue_confidence"),
                    "cwe": result.get("cwe", {}).get("id") if result.get("cwe") else None,
                }
            }
            self.findings.append(finding)
    
    def _process_semgrep_findings(self, semgrep_data: Dict):
        """Process Semgrep scan results"""
        try:
            # Handle both old and new Semgrep output formats
            results = semgrep_data.get("results", [])
            if not results and "errors" in semgrep_data:
                logger.warning("Semgrep reported errors but may still have findings")
            
            for result in results:
                # Map Semgrep severity to our format
                severity = "medium"  # Default
                if "extra" in result and "metadata" in result["extra"]:
                    severity_map = {
                        "ERROR": "high",
                        "WARNING": "medium",
                        "INFO": "low"
                    }
                    severity = severity_map.get(result["extra"]["metadata"].get("severity", "WARNING"), "medium")
                
                # Extract file path relative to repo
                file_path = result.get("path", "")
                if file_path.startswith(str(self.repo_path)):
                    file_path = os.path.relpath(file_path, self.repo_path)
                
                # Get a clean description
                description = result.get("extra", {}).get("message", "")
                if not description:
                    description = result.get("message", "No description provided")
                
                # Create the finding
                finding = {
                    "source": "semgrep",
                    "severity": severity,
                    "title": f"Semgrep: {result.get('check_id', 'Unknown rule')}",
                    "description": description,
                    "file_path": file_path,
                    "line_number": result.get("start", {}).get("line"),
                    "code_snippet": result.get("extra", {}).get("lines", ""),
                    "remediation": result.get("extra", {}).get("fix", "Review and fix the identified issue"),
                    "metadata": {
                        "rule_id": result.get("check_id"),
                        "category": result.get("extra", {}).get("metadata", {}).get("category", ""),
                        "cwe": result.get("extra", {}).get("metadata", {}).get("cwe", []),
                    }
                }
                self.findings.append(finding)
            
        except Exception as e:
            logger.error(f"Error processing Semgrep findings: {str(e)}")
            logger.debug(f"Semgrep data: {str(semgrep_data)[:500]}...")
    
    def _process_trufflehog_findings_v2(self, output: str):
        """Process TruffleHog v2 scan results"""
        try:
            # TruffleHog v2 outputs JSON objects, one per line
            findings_count = 0
            initial_findings_count = len(self.findings)
            
            for line in output.strip().split('\n'):
                if not line.strip():
                    continue
                    
                try:
                    result = json.loads(line)
                    
                    # Extract information from the result
                    path = result.get("path", "Unknown file")
                    branch = result.get("branch", "Unknown branch")
                    commit = result.get("commit", "Unknown commit")
                    reason = result.get("reason", "Unknown detector")
                    
                    finding = {
                        "source": "trufflehog",
                        "severity": "high",  # Secrets are always high severity
                        "title": f"Secret detected: {reason}",
                        "description": f"Potential secret found in {path}",
                        "file_path": path,
                        "line_number": None,  # TruffleHog v2 doesn't provide line numbers
                        "code_snippet": "<redacted>",  # Don't include the actual secret
                        "remediation": "Remove the secret and revoke it immediately. Use environment variables or a secure vault instead.",
                        "metadata": {
                            "detector": reason,
                            "branch": branch,
                            "commit": commit
                        }
                    }
                    self.findings.append(finding)
                    findings_count += 1
                    logger.debug(f"Added TruffleHog finding: {reason} in {path}")
                    
                except json.JSONDecodeError:
                    logger.warning(f"Failed to parse TruffleHog result line: {line[:50]}...")
                    continue
            
            final_findings_count = len(self.findings)
            logger.debug(f"TruffleHog findings before: {initial_findings_count}, after: {final_findings_count}")
                
            if findings_count > 0:
                logger.info(f"TruffleHog found {findings_count} potential secrets")
            else:
                logger.info("No secrets found by TruffleHog")
                
        except Exception as e:
            logger.error(f"Error processing TruffleHog results: {str(e)}")
    
    def _scan_python_files(self):
        """Scan Python files for security issues"""
        try:
            logger.info("Scanning Python files for security issues")
            
            # Find all Python files, excluding macOS resource files
            python_files = []
            for py_file in self.repo_path.glob("**/*.py"):
                # Skip macOS resource fork files and __MACOSX directories
                if "__MACOSX" in str(py_file) or os.path.basename(py_file).startswith("._"):
                    continue
                python_files.append(py_file)
            
            logger.info(f"Found {len(python_files)} Python files to scan")
            
            for py_file in python_files:
                try:
                    # Try to read the file with UTF-8 encoding first
                    try:
                        with open(py_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                    except UnicodeDecodeError:
                        # If UTF-8 fails, try with latin-1 encoding (which accepts any byte sequence)
                        logger.debug(f"UTF-8 decoding failed for {py_file}, trying latin-1")
                        with open(py_file, 'r', encoding='latin-1') as f:
                            content = f.read()
                    
                    # Parse the file with ast
                    try:
                        tree = ast.parse(content)
                        self._analyze_python_ast(tree, py_file, content)
                    except SyntaxError:
                        logger.warning(f"Syntax error in {py_file}, skipping AST analysis")
                    
                    # Also do some regex-based checks
                    self._check_python_patterns(content, py_file)
                    
                except Exception as e:
                    logger.error(f"Error analyzing {py_file}: {str(e)}")
        except Exception as e:
            logger.error(f"Error in Python file scanning: {str(e)}")
    
    def _analyze_python_ast(self, tree: ast.AST, file_path: Path, content: str):
        """Analyze Python AST for security issues"""
        # Find dangerous function calls
        dangerous_functions = {
            'eval': 'Dangerous eval() function can execute arbitrary code',
            'exec': 'Dangerous exec() function can execute arbitrary code',
            'os.system': 'Command injection risk with os.system()',
            'subprocess.call': 'Command injection risk with subprocess.call()',
            'subprocess.Popen': 'Command injection risk with subprocess.Popen()',
            'pickle.load': 'Insecure deserialization with pickle.load()',
            'pickle.loads': 'Insecure deserialization with pickle.loads()',
            'yaml.load': 'Insecure YAML loading without safe loader',
        }
        
        for node in ast.walk(tree):
            # Check for dangerous function calls
            if isinstance(node, ast.Call):
                func_name = None
                
                # Direct function call like eval()
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                
                # Module function call like os.system()
                elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                    func_name = f"{node.func.value.id}.{node.func.attr}"
                
                if func_name in dangerous_functions:
                    line_num = node.lineno
                    line = content.splitlines()[line_num-1]
                    
                    self.findings.append({
                        "source": "custom_python_analyzer",
                        "severity": "high",
                        "title": f"Use of dangerous function: {func_name}",
                        "description": dangerous_functions[func_name],
                        "file_path": str(file_path.relative_to(self.repo_path)),
                        "line_number": line_num,
                        "code_snippet": line.strip(),
                        "remediation": f"Avoid using {func_name} with untrusted input. Consider safer alternatives.",
                        "metadata": {
                            "function": func_name,
                            "type": "dangerous_function_call"
                        }
                    })
    
    def _check_python_patterns(self, content: str, file_path: Path):
        """Check Python code for security issues using regex patterns"""
        patterns = [
            # Removed hardcoded password and secret key patterns as they're covered by TruffleHog
            {
                "pattern": r"open\([^,)]+\)\s*\.\s*write",
                "title": "Potential unsafe file write",
                "description": "File write operation without proper path validation",
                "severity": "medium",
                "remediation": "Validate file paths and use secure file operations"
            },
            {
                "pattern": r"@app\.route\([^)]*methods=\[[^\]]*['\"]GET['\"][^\]]*['\"]POST['\"][^\]]*\]",
                "title": "CSRF vulnerability in Flask route",
                "description": "Flask route accepts both GET and POST without CSRF protection",
                "severity": "medium",
                "remediation": "Implement CSRF protection for POST routes"
            },
            # SSRF detection patterns
            {
                "pattern": r"requests\.get\s*\(\s*[^,)]*\)",
                "title": "Potential SSRF vulnerability",
                "description": "Unvalidated URL in HTTP request could lead to Server-Side Request Forgery",
                "severity": "high",
                "remediation": "Validate and sanitize URLs before making HTTP requests. Consider implementing URL allowlisting."
            },
            {
                "pattern": r"urllib\.request\.urlopen\s*\(\s*[^,)]*\)",
                "title": "Potential SSRF vulnerability",
                "description": "Unvalidated URL in urllib request could lead to Server-Side Request Forgery",
                "severity": "high",
                "remediation": "Validate and sanitize URLs before making HTTP requests. Consider implementing URL allowlisting."
            },
            # JWT insecure handling
            {
                "pattern": r"jwt\.decode\([^,)]*,\s*verify\s*=\s*False",
                "title": "JWT verification disabled",
                "description": "JWT token verification is explicitly disabled",
                "severity": "high",
                "remediation": "Always verify JWT tokens and their signatures"
            },
            # GraphQL vulnerabilities
            {
                "pattern": r"graphql\.execute_sync\([^)]*\)",
                "title": "Potential GraphQL injection",
                "description": "GraphQL query execution without proper validation",
                "severity": "high",
                "remediation": "Validate and sanitize GraphQL queries, use query whitelisting"
            },
            # NoSQL injection
            {
                "pattern": r"db\.collection\.find\(\s*{[^}]*\$where[^}]*}\s*\)",
                "title": "Potential NoSQL injection",
                "description": "MongoDB query using $where operator which can lead to NoSQL injection",
                "severity": "high",
                "remediation": "Avoid using $where operator with user input, use query parameters instead"
            },
            # Prototype pollution
            {
                "pattern": r"Object\.assign\(\s*{}\s*,",
                "title": "Potential prototype pollution",
                "description": "Merging objects without proper validation can lead to prototype pollution",
                "severity": "medium",
                "remediation": "Use Object.create(null) for empty objects or dedicated libraries for safe object merging"
            },
            # Insecure deserialization (JavaScript)
            {
                "pattern": r"JSON\.parse\(\s*[^,)]*\)",
                "title": "Potential insecure deserialization",
                "description": "JSON parsing without validation could lead to prototype pollution or other issues",
                "severity": "medium",
                "remediation": "Validate JSON data before parsing, consider using JSON schema validation"
            },
            # Server-side template injection
            {
                "pattern": r"render_template_string\(\s*[^,)]*\)",
                "title": "Potential server-side template injection",
                "description": "Dynamic template rendering could lead to template injection attacks",
                "severity": "high",
                "remediation": "Avoid using user input in template strings, use static templates with parameters"
            },
            # Insecure file upload
            {
                "pattern": r"\.save\(\s*os\.path\.join\([^,)]*\)\s*\)",
                "title": "Potential insecure file upload",
                "description": "File upload without proper validation could lead to path traversal or code execution",
                "severity": "high",
                "remediation": "Validate file extensions, content types, and sanitize filenames before saving"
            },
            # Insecure randomness
            {
                "pattern": r"random\.[a-zA-Z]+\(\)",
                "title": "Potential insecure randomness",
                "description": "Using non-cryptographic random number generator for security purposes",
                "severity": "medium",
                "remediation": "Use cryptographically secure random number generators (e.g., secrets module in Python)"
            },
            # Insecure hashing
            {
                "pattern": r"hashlib\.md5\(\)",
                "title": "Insecure hashing algorithm",
                "description": "MD5 is cryptographically broken and unsuitable for security purposes",
                "severity": "medium",
                "remediation": "Use secure hashing algorithms like SHA-256 or better"
            },
            # Rate limiting bypass
            {
                "pattern": r"@limiter\.exempt",
                "title": "Rate limiting bypass",
                "description": "Endpoint is exempt from rate limiting which could lead to abuse",
                "severity": "medium",
                "remediation": "Apply appropriate rate limiting to all public endpoints"
            }
        ]
        
        lines = content.splitlines()
        for pattern_info in patterns:
            for i, line in enumerate(lines):
                if re.search(pattern_info["pattern"], line):
                    self.findings.append({
                        "source": "custom_pattern_matcher",
                        "severity": pattern_info["severity"],
                        "title": pattern_info["title"],
                        "description": pattern_info["description"],
                        "file_path": str(file_path.relative_to(self.repo_path)),
                        "line_number": i + 1,
                        "code_snippet": line.strip(),
                        "remediation": pattern_info["remediation"],
                        "metadata": {
                            "pattern": pattern_info["pattern"],
                            "type": "pattern_match"
                        }
                    })
    
    def _save_findings(self):
        """Save findings to a JSON file with improved structure for LLM consumption"""
        try:
            if not self.findings:
                # Create an empty report structure even if no findings
                output = {
                    "scan_info": {
                        "scanner": "patcha-security-scanner",
                        "repository": str(self.repo_path),
                        "scan_time": datetime.now().isoformat(),
                        "total_findings": 0,
                        "version": "1.0.0"
                    },
                    "summary": {
                        "total_issues": 0,
                        "severity_counts": {"high": 0, "medium": 0, "low": 0},
                        "files_affected": 0
                    },
                    "security_score": {
                        "score": 0,
                        "rating": "A",
                        "summary": "No security issues found"
                    },
                    "security_issues": []
                }
            else:
                # Process findings as before
                unique_findings = self._filter_actionable_findings(self.findings)
                
                # Calculate security score
                security_score = self.calculate_security_score()
                
                # Group findings by severity and file
                findings_by_severity = {"high": [], "medium": [], "low": []}
                findings_by_file = {}
                
                for finding in unique_findings:
                    severity = finding.get("severity", "low")
                    file_path = finding.get("file_path", "unknown")
                    
                    if severity in findings_by_severity:
                        findings_by_severity[severity].append(finding)
                    
                    if file_path not in findings_by_file:
                        findings_by_file[file_path] = []
                    findings_by_file[file_path].append(finding)
                
                # Create output structure
                output = {
                    "scan_info": {
                        "scanner": "patcha-security-scanner",
                        "repository": str(self.repo_path),
                        "scan_time": datetime.now().isoformat(),
                        "total_findings": len(unique_findings),
                        "version": "1.0.0"
                    },
                    "summary": {
                        "total_issues": len(unique_findings),
                        "severity_counts": {
                            "high": len(findings_by_severity["high"]),
                            "medium": len(findings_by_severity["medium"]),
                            "low": len(findings_by_severity["low"])
                        },
                        "files_affected": len(findings_by_file),
                        "top_vulnerable_files": sorted(
                            [(file, len(issues)) for file, issues in findings_by_file.items()],
                            key=lambda x: x[1],
                            reverse=True
                        )[:5]
                    },
                    "security_score": {
                        "score": security_score,
                        "rating": self._get_security_rating(security_score),
                        "summary": self._get_score_summary(security_score)
                    },
                    "security_issues": unique_findings
                }
            
            # Always write to sec.json
            with open('sec.json', 'w') as f:
                json.dump(output, f, indent=2)
            
            logger.info(f"Findings saved to sec.json")
            if self.findings:
                logger.info(f"Summary: {len(self.findings)} issues found "
                          f"({len(findings_by_severity['high'])} high, "
                          f"{len(findings_by_severity['medium'])} medium, "
                          f"{len(findings_by_severity['low'])} low)")
            
        except Exception as e:
            logger.error(f"Error saving findings: {str(e)}")
            # Try to save in a simpler format as fallback
            try:
                with open('sec.json', 'w') as f:
                    json.dump({"findings": self.findings}, f)
            except Exception as backup_error:
                logger.error(f"Failed to save even simple findings: {str(backup_error)}")

    def _run_nikto_scan(self, target_url=None):
        """Run Nikto web server scanner for DAST analysis"""
        try:
            logger.info("Running Nikto web server scan")
            
            # Check if a target URL was provided
            if not target_url:
                logger.warning("No target URL provided for Nikto scan. Use --target-url parameter. Skipping DAST scan.")
                return
            
            # Check if Nikto is installed
            try:
                subprocess.run(["nikto", "-Version"], check=True, capture_output=True)
            except (subprocess.SubprocessError, FileNotFoundError):
                logger.warning("Nikto not found. Please install Nikto. Skipping DAST scan.")
                return
            
            logger.info(f"Starting Nikto scan against {target_url}")
            
            # Run Nikto with TEXT output format and additional options for SSL issues
            # -nossl: Disable SSL
            # -Tuning x: Disable SSL-related checks
            # -maxtime 300s: Set a maximum scan time of 5 minutes
            result = subprocess.run(
                ["nikto", "-h", target_url, "-Format", "txt", "-output", "nikto_results.txt", 
                 "-maxtime", "300s", "-Tuning", "x", "-nossl"],
                capture_output=True,
                text=True
            )
            
            # Nikto can return 1 for findings or errors, so we need to check if the output file exists
            if os.path.exists("nikto_results.txt"):
                try:
                    with open("nikto_results.txt", "r") as f:
                        nikto_output = f.read()
                    
                    # Check if the output contains actual findings or just errors
                    if "+ ERROR: Error limit" in nikto_output and len(nikto_output.split('\n')) < 10:
                        logger.error(f"Nikto scan failed with SSL errors: {nikto_output}")
                        # Try again without SSL
                        logger.info("Retrying Nikto scan without SSL...")
                        os.remove("nikto_results.txt")
                        return
                    
                    self._process_nikto_findings_txt(nikto_output, target_url)
                    
                    # Clean up the temporary file
                    os.remove("nikto_results.txt")
                except FileNotFoundError as e:
                    logger.error(f"Failed to process Nikto results: {str(e)}")
            else:
                logger.error(f"Nikto scan failed with exit code {result.returncode}")
                logger.error(f"Error: {result.stderr}")
                
        except Exception as e:
            logger.error(f"Error running Nikto scan: {str(e)}")
            # Clean up any temporary files
            if os.path.exists("nikto_results.txt"):
                os.remove("nikto_results.txt")

    def _process_nikto_findings_txt(self, output_text, target_url):
        """Process Nikto scan results in text format"""
        findings_count = 0
        
        # Simple parsing of Nikto text output
        for line in output_text.split('\n'):
            if "+ " in line:  # Nikto prefixes findings with "+ "
                # Extract information from the line
                description = line.strip()
                
                # Try to determine severity based on keywords
                severity = "medium"  # Default
                high_keywords = ["critical", "high", "severe", "vulnerability", "XSS", "SQL injection", "remote code"]
                low_keywords = ["information", "informational", "info", "low"]
                
                if any(keyword.lower() in description.lower() for keyword in high_keywords):
                    severity = "high"
                elif any(keyword.lower() in description.lower() for keyword in low_keywords):
                    severity = "low"
                
                # Create a finding
                finding = {
                    "source": "nikto",
                    "severity": severity,
                    "title": f"Nikto: Web Vulnerability",
                    "description": description,
                    "file_path": target_url,
                    "line_number": None,
                    "code_snippet": "",
                    "remediation": "Review and fix the identified web server vulnerability",
                    "metadata": {
                        "url": target_url
                    }
                }
                self.findings.append(finding)
                findings_count += 1
        
        if findings_count > 0:
            logger.info(f"Nikto found {findings_count} potential vulnerabilities")
        else:
            logger.info("No vulnerabilities found by Nikto")

    def _should_skip_file(self, file_path):
        """Check if a file should be skipped during scanning"""
        file_str = str(file_path)
        
        # Skip macOS resource files and directories
        if "__MACOSX" in file_str or os.path.basename(file_str).startswith("._"):
            return True
        
        # Skip common binary files
        binary_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.zip', '.tar', '.gz', '.exe', '.dll']
        if any(file_str.lower().endswith(ext) for ext in binary_extensions):
            return True
        
        # Skip very large files (>10MB)
        try:
            if os.path.getsize(file_path) > 10 * 1024 * 1024:
                logger.warning(f"Skipping large file: {file_path}")
                return True
        except (OSError, IOError):
            # If we can't check the size, better to skip
            return True
        
        return False

    def _filter_actionable_findings(self, findings):
        """Filter findings to only include actionable items"""
        actionable_findings = []
        
        for finding in findings:
            file_path = finding.get("file_path", "")
            
            # Skip findings in dependency directories
            if any(pattern in file_path for pattern in [
                "node_modules/", 
                "vendor/",
                "third_party/",
                "external/",
                ".venv/",
                "env/",
                "venv/",
                "site-packages/"
            ]):
                continue
            
            # Skip findings in temporary or build directories
            if any(pattern in file_path for pattern in [
                "dist/",
                "build/",
                "tmp/",
                "temp/",
                ".cache/"
            ]):
                continue
            
            # Skip findings in generated code
            if any(pattern in file_path for pattern in [
                "generated/",
                "auto-generated",
                ".min.js",
                ".bundle.js"
            ]):
                continue
            
            # Skip findings in test data
            if any(pattern in file_path for pattern in [
                "test/fixtures/",
                "test/data/",
                "tests/mocks/"
            ]):
                continue
            
            # Skip findings in deeply nested paths (more than 6 levels deep)
            if file_path.count("/") > 6:
                continue
            
            # Skip findings in files that are too large (likely binary or generated)
            try:
                full_path = os.path.join(self.repo_path, file_path)
                if os.path.exists(full_path) and os.path.getsize(full_path) > 1000000:  # 1MB
                    continue
            except:
                pass
            
            actionable_findings.append(finding)
        
        return actionable_findings

    def _detect_languages(self):
        """Detect programming languages used in the repository"""
        languages = {}
        extensions = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".html": "HTML",
            ".css": "CSS",
            ".java": "Java",
            ".go": "Go",
            ".rb": "Ruby",
            ".php": "PHP",
            ".c": "C",
            ".cpp": "C++",
            ".cs": "C#",
            ".swift": "Swift",
            ".kt": "Kotlin"
        }
        
        for ext, lang in extensions.items():
            count = len(list(self.repo_path.glob(f"**/*{ext}")))
            if count > 0:
                languages[lang] = count
        
        return languages

    def _detect_frameworks(self):
        """Detect frameworks used in the repository"""
        frameworks = []
        
        # Check for common frameworks by looking for key files
        framework_indicators = {
            "Flask": ["app.py", "flask", "requirements.txt"],
            "Django": ["manage.py", "django", "settings.py"],
            "React": ["react", "jsx", "package.json"],
            "Angular": ["angular.json", "ng"],
            "Vue": ["vue.config.js", "vue"],
            "Express": ["express", "app.js", "server.js"],
            "Spring": ["pom.xml", "application.properties"],
            "Rails": ["Gemfile", "config/routes.rb"]
        }
        
        for framework, indicators in framework_indicators.items():
            for indicator in indicators:
                if list(self.repo_path.glob(f"**/*{indicator}*")):
                    frameworks.append(framework)
                    break
        
        return list(set(frameworks))

    def _identify_key_components(self):
        """Identify key components of the application"""
        components = []
        
        # Check for common components
        if list(self.repo_path.glob("**/Dockerfile")) or list(self.repo_path.glob("**/docker-compose.yml")):
            components.append("Docker")
        
        if list(self.repo_path.glob("**/.github/workflows")):
            components.append("GitHub Actions")
        
        if list(self.repo_path.glob("**/kubernetes")) or list(self.repo_path.glob("**/*.yaml")):
            components.append("Kubernetes")
        
        if list(self.repo_path.glob("**/database")) or list(self.repo_path.glob("**/db")):
            components.append("Database")
        
        if list(self.repo_path.glob("**/auth")) or list(self.repo_path.glob("**/login")):
            components.append("Authentication")
        
        return components

    def _group_related_findings(self, findings):
        """Group related findings based on file path and issue type"""
        related = {}
        
        for i, finding in enumerate(findings):
            key = self._create_finding_key(finding)
            related[key] = []
            
            for j, other in enumerate(findings):
                if i == j:
                    continue
                    
                # Findings in the same file
                if finding.get("file_path") == other.get("file_path"):
                    related[key].append({
                        "id": j,
                        "title": other.get("title"),
                        "relationship": "same_file"
                    })
                
                # Findings with the same issue type
                if finding.get("title") == other.get("title"):
                    related[key].append({
                        "id": j,
                        "title": other.get("title"),
                        "file_path": other.get("file_path"),
                        "relationship": "same_issue_type"
                    })
        
        return related

    def _create_finding_key(self, finding):
        """Create a unique key for a finding"""
        return f"{finding.get('file_path')}:{finding.get('line_number')}:{finding.get('title')}"

    def _estimate_remediation_complexity(self, finding):
        """Estimate the complexity of remediating a finding"""
        # Simple heuristic based on severity and finding type
        if finding.get("severity") == "high":
            return "high"
        
        if "SQL injection" in finding.get("description", ""):
            return "medium"
        
        if "XSS" in finding.get("description", ""):
            return "medium"
        
        if "secret" in finding.get("title", "").lower():
            return "low"
        
        return "low"

    def _get_code_context(self, finding):
        """Get more context around the vulnerable code as a single code block"""
        file_path = finding.get("file_path")
        line_number = finding.get("line_number")
        
        if not file_path or not line_number or not os.path.exists(os.path.join(self.repo_path, file_path)):
            return None
        
        try:
            with open(os.path.join(self.repo_path, file_path), 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
            # Get 5 lines before and after the vulnerable line
            start = max(0, line_number - 5)
            end = min(len(lines), line_number + 5)
            
            # Create a single code block with line numbers
            code_block = []
            for i in range(start, end):
                line_content = lines[i].rstrip()
                prefix = "→ " if i+1 == line_number else "  "
                code_block.append(f"{prefix}{i+1}: {line_content}")
            
            context = {
                "code_block": "\n".join(code_block),
                "line_range": f"{start+1}-{end}",
                "vulnerable_line": line_number
            }
            
            return context
        except Exception as e:
            logger.debug(f"Error getting code context: {str(e)}")
            return None

    def _generate_remediation_example(self, finding):
        """Generate a code example for remediation based on the finding type"""
        title = finding.get("title", "").lower()
        description = finding.get("description", "").lower()
        
        # Dependency vulnerability remediation
        if "dependency vulnerability" in title:
            metadata = finding.get("metadata", {})
            pkg_name = metadata.get("package_name", "package_name")
            current_version = metadata.get("installed_version", "1.0.0")
            fixed_version = metadata.get("fixed_version", "2.0.0")
            
            if "package.json" in finding.get("file_path", ""):
                return {
                    "language": "json",
                    "before": f'  "dependencies": {{\n    "{pkg_name}": "^{current_version}"\n  }}',
                    "after": f'  "dependencies": {{\n    "{pkg_name}": "^{fixed_version}"\n  }}',
                    "explanation": f"Update {pkg_name} to version {fixed_version} or later to fix the vulnerability"
                }
            elif "requirements.txt" in finding.get("file_path", ""):
                return {
                    "language": "text",
                    "before": f"{pkg_name}=={current_version}",
                    "after": f"{pkg_name}>={fixed_version}",
                    "explanation": f"Update {pkg_name} to version {fixed_version} or later to fix the vulnerability"
                }
            else:
                return {
                    "language": "generic",
                    "before": f"Using vulnerable version: {pkg_name} {current_version}",
                    "after": f"Update to fixed version: {pkg_name} {fixed_version} or later",
                    "explanation": "Update the dependency to a non-vulnerable version"
                }
        
        # SQL Injection remediation
        if "sql" in title or "sql injection" in description:
            return {
                "language": "python",
                "before": "cursor.execute(f\"SELECT * FROM users WHERE username = '{username}'\")",
                "after": "cursor.execute(\"SELECT * FROM users WHERE username = ?\", (username,))",
                "explanation": "Use parameterized queries instead of string formatting to prevent SQL injection"
            }
        
        # Flask debug mode remediation
        if "flask" in title and "debug" in title:
            return {
                "language": "python",
                "before": "app.run(debug=True, host='0.0.0.0')",
                "after": "app.run(debug=False, host='127.0.0.1')",
                "explanation": "Disable debug mode in production and avoid exposing the server publicly"
            }
        
        # Secret in code remediation
        if "secret" in title:
            return {
                "language": "generic",
                "before": "API_KEY = \"actual-secret-key-value\"",
                "after": "API_KEY = os.environ.get(\"API_KEY\")",
                "explanation": "Store secrets in environment variables or a secure vault instead of hardcoding them"
            }
        
        return None

    def _determine_category(self, finding):
        """Determine the security category of a finding"""
        title = finding.get("title", "").lower()
        description = finding.get("description", "").lower()
        metadata = finding.get("metadata", {})
        
        # Check for dependency vulnerabilities
        if "dependency vulnerability" in title or "cve-" in title.lower():
            return "dependency"
        
        # Check for SQL injection
        if "sql" in title or "sql injection" in description:
            return "injection"
        
        # Check for XSS
        if "xss" in title or "cross-site scripting" in description:
            return "xss"
        
        # Check for authentication issues
        if "auth" in title or "password" in title or "login" in description:
            return "authentication"
        
        # Check for secrets/credentials
        if "secret" in title or "credential" in title or "api key" in description:
            return "secrets"
        
        # Check for configuration issues
        if "config" in title or "debug" in title or "host" in title:
            return "configuration"
        
        # Check for CWE in metadata
        if metadata and "cwe" in metadata:
            cwe = metadata.get("cwe", [])
            if isinstance(cwe, list) and cwe:
                cwe_str = cwe[0].lower() if isinstance(cwe[0], str) else ""
                if "injection" in cwe_str:
                    return "injection"
                if "xss" in cwe_str:
                    return "xss"
                if "auth" in cwe_str:
                    return "authentication"
                if "exposure" in cwe_str:
                    return "information_exposure"
        
        # Default category
        return "general"

    def _generate_finding_id(self, finding):
        """Generate a unique ID for a finding"""
        import hashlib
        
        # Create a string with key finding attributes
        key_str = f"{finding.get('file_path')}:{finding.get('line_number')}:{finding.get('title')}"
        
        # Generate a short hash
        hash_obj = hashlib.md5(key_str.encode())
        return hash_obj.hexdigest()[:8]

    def _extract_cwe(self, finding):
        """Extract CWE information from a finding"""
        metadata = finding.get("metadata", {})
        
        if metadata and "cwe" in metadata:
            cwe = metadata.get("cwe", [])
            if isinstance(cwe, list) and cwe:
                # Return just the CWE ID number
                cwe_str = cwe[0] if isinstance(cwe[0], str) else ""
                match = re.search(r'CWE-(\d+)', cwe_str)
                if match:
                    return int(match.group(1))
        
        # Try to determine CWE from description
        description = finding.get("description", "").lower()
        
        if "sql injection" in description:
            return 89  # CWE-89: SQL Injection
        elif "xss" in description or "cross-site scripting" in description:
            return 79  # CWE-79: Cross-site Scripting
        elif "path traversal" in description:
            return 22  # CWE-22: Path Traversal
        elif "command injection" in description:
            return 77  # CWE-77: Command Injection
        
        return None

    def _run_trivy_scan(self):
        """Run Trivy scan for dependency vulnerabilities"""
        try:
            logger.info("Running Trivy dependency scan")
            
            # Check if Trivy is installed
            try:
                result = subprocess.run(["trivy", "--version"], check=True, capture_output=True, text=True)
                logger.info(f"Trivy version: {result.stdout.strip()}")
            except (subprocess.SubprocessError, FileNotFoundError):
                logger.warning("Trivy not found. Please install Trivy for dependency scanning. Skipping Trivy scan.")
                logger.info("Installation instructions: https://aquasecurity.github.io/trivy/latest/getting-started/installation/")
                return
            
            # Create a temporary directory for Trivy output
            with tempfile.TemporaryDirectory() as temp_dir:
                output_file = os.path.join(temp_dir, "trivy-results.json")
                
                # Run Trivy with JSON output format
                logger.info(f"Scanning dependencies in {self.repo_path}")
                result = subprocess.run(
                    [
                        "trivy", "fs", "--format", "json", 
                        "--output", output_file,
                        "--severity", "HIGH,CRITICAL",  # Focus on high and critical vulnerabilities
                        "--security-checks", "vuln",    # Check for vulnerabilities
                        str(self.repo_path)
                    ],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    # Process the results
                    try:
                        with open(output_file, 'r') as f:
                            trivy_data = json.load(f)
                        self._process_trivy_findings(trivy_data)
                    except (json.JSONDecodeError, FileNotFoundError) as e:
                        logger.error(f"Failed to process Trivy results: {str(e)}")
                else:
                    logger.error(f"Trivy scan failed with exit code {result.returncode}")
                    logger.error(f"Error: {result.stderr}")
                
        except Exception as e:
            logger.error(f"Error running Trivy scan: {str(e)}")

    def _process_trivy_findings(self, trivy_data):
        """Process Trivy scan results"""
        if not trivy_data or "Results" not in trivy_data:
            logger.info("No vulnerabilities found by Trivy")
            return
        
        findings_count = 0
        
        for result in trivy_data.get("Results", []):
            target = result.get("Target", "unknown")
            target_type = result.get("Type", "unknown")
            
            # Process vulnerabilities
            for vuln in result.get("Vulnerabilities", []):
                # Map Trivy severity to our format
                severity_map = {
                    "CRITICAL": "high",
                    "HIGH": "high",
                    "MEDIUM": "medium",
                    "LOW": "low",
                    "UNKNOWN": "medium"
                }
                severity = severity_map.get(vuln.get("Severity", "UNKNOWN"), "medium")
                
                # Extract package information
                pkg_name = vuln.get("PkgName", "unknown")
                installed_version = vuln.get("InstalledVersion", "unknown")
                fixed_version = vuln.get("FixedVersion", "unknown")
                
                # Create a finding
                finding = {
                    "source": "trivy",
                    "severity": severity,
                    "title": f"Dependency Vulnerability: {vuln.get('VulnerabilityID', 'Unknown')}",
                    "description": vuln.get("Description") or vuln.get("Title", "No description provided"),
                    "file_path": self._determine_dependency_file(target, pkg_name, target_type),
                    "line_number": None,
                    "code_snippet": "",
                    "remediation": f"Update {pkg_name} from version {installed_version} to {fixed_version} or later",
                    "metadata": {
                        "vulnerability_id": vuln.get("VulnerabilityID"),
                        "package_name": pkg_name,
                        "installed_version": installed_version,
                        "fixed_version": fixed_version,
                        "references": vuln.get("References", []),
                        "cwe": vuln.get("CweIDs", [])
                    }
                }
                
                self.findings.append(finding)
                findings_count += 1
        
        if findings_count > 0:
            logger.info(f"Trivy found {findings_count} vulnerabilities in dependencies")
        else:
            logger.info("No vulnerabilities found by Trivy")

    def _determine_dependency_file(self, target, pkg_name, target_type):
        """Determine the most likely file containing the dependency"""
        # For npm packages
        if target_type == "npm":
            if os.path.exists(os.path.join(self.repo_path, "package.json")):
                return "package.json"
            # Look for nested package.json files
            pkg_files = list(self.repo_path.glob("**/package.json"))
            if pkg_files:
                return str(os.path.relpath(pkg_files[0], self.repo_path))
        
        # For Python packages
        if target_type == "pip" or pkg_name.lower() in target.lower():
            if os.path.exists(os.path.join(self.repo_path, "requirements.txt")):
                return "requirements.txt"
            if os.path.exists(os.path.join(self.repo_path, "Pipfile")):
                return "Pipfile"
            if os.path.exists(os.path.join(self.repo_path, "Pipfile.lock")):
                return "Pipfile.lock"
            if os.path.exists(os.path.join(self.repo_path, "pyproject.toml")):
                return "pyproject.toml"
        
        # For Java packages
        if target_type == "jar":
            if os.path.exists(os.path.join(self.repo_path, "pom.xml")):
                return "pom.xml"
            if os.path.exists(os.path.join(self.repo_path, "build.gradle")):
                return "build.gradle"
        
        # For Ruby packages
        if target_type == "gem":
            if os.path.exists(os.path.join(self.repo_path, "Gemfile")):
                return "Gemfile"
            if os.path.exists(os.path.join(self.repo_path, "Gemfile.lock")):
                return "Gemfile.lock"
        
        # Default to the target if we can't determine a specific file
        return target

    def _simplify_text(self, text):
        """Simplify text for comparison by removing common variations"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove common prefixes
        prefixes = ["detected ", "found ", "vulnerability: ", "warning: ", "error: "]
        for prefix in prefixes:
            if text.startswith(prefix):
                text = text[len(prefix):]
        
        # Remove punctuation and extra whitespace
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove common words that don't add meaning
        stop_words = ["the", "a", "an", "is", "are", "was", "were", "be", "been", "being", 
                     "in", "on", "at", "by", "for", "with", "about", "against", "between",
                     "into", "through", "during", "before", "after", "above", "below", 
                     "to", "from", "up", "down", "of", "off", "over", "under", "again",
                     "further", "then", "once", "here", "there", "when", "where", "why",
                     "how", "all", "any", "both", "each", "few", "more", "most", "other",
                     "some", "such", "no", "nor", "not", "only", "own", "same", "so",
                     "than", "too", "very", "can", "will", "just", "should", "now"]
        
        words = text.split()
        filtered_words = [word for word in words if word not in stop_words]
        
        # Get the most significant words (up to 10)
        significant_words = filtered_words[:10] if len(filtered_words) > 10 else filtered_words
        
        return " ".join(significant_words)

    def _select_best_finding(self, findings_group):
        """Select the best finding from a group of similar findings"""
        if len(findings_group) == 1:
            return findings_group[0]
        
        # Scoring system for findings
        def score_finding(finding):
            score = 0
            
            # Prefer findings with higher severity
            severity = finding.get("severity", "low")
            if severity == "high":
                score += 30
            elif severity == "medium":
                score += 20
            elif severity == "low":
                score += 10
            
            # Prefer findings with more complete information
            if finding.get("description") and len(finding.get("description", "")) > 50:
                score += 10
            
            if finding.get("remediation") and len(finding.get("remediation", "")) > 20:
                score += 10
            
            if finding.get("code_snippet"):
                score += 5
            
            if finding.get("line_number"):
                score += 5
            
            # Prefer findings from certain tools
            source = finding.get("source", "").lower()
            if source == "semgrep":
                score += 8  # Semgrep usually has good context
            elif source == "trivy":
                score += 7  # Trivy has good dependency info
            elif source == "bandit":
                score += 6  # Bandit is Python-specific
            
            # Prefer findings with CWE information
            if finding.get("metadata", {}).get("cwe"):
                score += 5
            
            return score
        
        # Sort findings by score (highest first)
        sorted_findings = sorted(findings_group, key=score_finding, reverse=True)
        
        # Take the highest-scoring finding
        best_finding = sorted_findings[0]
        
        # Enhance it with information from other findings
        for finding in sorted_findings[1:]:
            # Merge sources
            sources = []
            if "source" in best_finding:
                sources.append(best_finding["source"])
            if "source" in finding and finding["source"] not in sources:
                sources.append(finding["source"])
            
            if sources:
                best_finding["metadata"] = best_finding.get("metadata", {})
                best_finding["metadata"]["detected_by"] = sources
            
            # If the best finding doesn't have a remediation but another does, use it
            if not best_finding.get("remediation") and finding.get("remediation"):
                best_finding["remediation"] = finding["remediation"]
            
            # If the best finding doesn't have a code snippet but another does, use it
            if not best_finding.get("code_snippet") and finding.get("code_snippet"):
                best_finding["code_snippet"] = finding["code_snippet"]
        
        # Remove the original source field since we now have detected_by in metadata
        if "source" in best_finding:
            del best_finding["source"]
        
        return best_finding

    def calculate_security_score(self):
        """Calculate a security score from 0-100 (higher is better)"""
        if not self.findings:
            return 100  # Perfect score if no issues

        # Base weights for different severity levels
        severity_weights = {
            "high": 10,
            "medium": 5,
            "low": 2
        }

        # Calculate weighted deductions
        total_deductions = 0
        
        for finding in self.findings:
            severity = finding.get("severity", "low")
            deduction = severity_weights.get(severity, 1)
            
            # Additional deductions for critical issues
            if "injection" in finding.get("title", "").lower():
                deduction *= 1.5
            if "rce" in finding.get("title", "").lower() or "remote code execution" in finding.get("description", "").lower():
                deduction *= 2
            
            total_deductions += deduction

        # Calculate final score (inverse of deductions)
        score = max(0, 100 - total_deductions)
        return round(score, 2)

    def _get_security_rating(self, score):
        """Convert numerical score to letter rating (higher score = better grade)"""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def _get_score_summary(self, score):
        """Generate a human-readable summary of the security score"""
        if score >= 90:
            return "Excellent security posture with minimal security debt"
        elif score >= 80:
            return "Good security posture with some minor issues to address"
        elif score >= 70:
            return "Moderate security concerns that should be addressed"
        elif score >= 60:
            return "Significant security issues requiring attention"
        else:
            return "Critical security problems requiring urgent remediation"

def main():
    parser = argparse.ArgumentParser(description="Patcha Security Scanner")
    parser.add_argument("repo_path", help="Path to the repository to scan")
    parser.add_argument("--output", "-o", default="security_findings.json", 
                        help="Output file for findings (default: security_findings.json)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    parser.add_argument("--target-url", "-u", help="Target URL for DAST scanning with Nikto")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        scanner = SecurityScanner(args.repo_path, args.output)
        scanner.scan(args.target_url)
        print(f"Scan complete. Results saved to {args.output}")
    except Exception as e:
        logger.error(f"Error during scan: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()