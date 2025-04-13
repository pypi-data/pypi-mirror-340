import argparse
import logging
import sys
from .scanner import SecurityScanner

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("patcha")

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