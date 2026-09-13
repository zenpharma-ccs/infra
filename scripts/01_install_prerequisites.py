import os
import subprocess
import sys
from datetime import datetime

DEFAULT_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
CYAN = "\033[0;36m"
NC = "\033[0m"

def _ts():
    return datetime.now().strftime("%H:%M:%S")

def log(msg): print(f"{GREEN}[{_ts()}] OK {msg}{NC}")
def warn(msg): print(f"{YELLOW}[{_ts()}] !! |{msg}{NC}")
def info(msg): print(f"{CYAN}[{_ts()}]")
def die(msg): 
    print(f"{RED}[{_ts()}] ERR {msg}{NC}", file=sys.stderr)
    sys.exit(1)
    
def run_cmd(args, ok_fail=False, capture=False):
    if capture:
        result = subprocess.run(args, capture_output=True, text=True)
        return result.stdout.strip(), result.returncode
    
    result = subprocess.run(args)
    if result.returncode != 0 and not ok_fail:
        die(f"Command failed: {' '.join(str(a) for a in args)}")
    
    return None, result.returncode

def prompt(var_name, label, example, default=""):
    current = os.environ.get(var_name, "")
    
    if current:
        info(f"Using {var_name}={current} (pre-set in environment, skipping prompt)")
        return current
    
    print()
    print(f"{CYAN} {label}{NC}")
    print(f"  Example : {example}")
    
    if default:
        print(f"  Default : {default}")
        raw = input("  Your value [press Enter to use defaults]: ").strip()
    else:
        raw = input("  Your value: ").strip()
        
    value = raw if raw else default
    if not value:
        die(f"'{label}' is required and cannot be empty.")
        
    log(f" {var_name} = {value}")
    
    return value

# Verify required tools are installed
print()
print("Checking required tools...")
for tool in ["kubectl", "helm", "aws"]:
    rc = subprocess.run(["which", tool], capture_output=True).returncode
    if rc != 0:
        die(f"{tool} not found. Install it before running this script.")
        
log("kubectl, helm,and aws CLI found")

#  Collect scripts

print()
print("=============================================")
print("    Zen Pharma -- Pre-requisites Installer")
print("=============================================")
print()
print(" This script installs AWS Load Balancer Controller, ArgoCD, and")
print(" External Secrets Operator on your EKS cluster using Helm")
print()
print(" You will be asked for 4 values:")
print("   1. EKS cluster name             - from Terraform outputs or AWS console")
print("   2. AWS Region                   - where your cluster is running")
print("   3. VPC ID                       - VPC where the cluster lives (auto-fetched if blank)")
print("   4. ALB controller role ARN      - IAM role ARN for the ALB controller")
print("      (arn:aws:iam::<account-id>:role/<project>-<env>-alb-controller-role)")
print()

CLUSTER_NAME            = prompt("CLUSTER_NAME",          "EKS cluster name",
                                 "pharma-dev-cluster",    "pharma-dev-cluster")
AWS_REGION              = prompt("AWS_REGION",            "AWS region where the cluster is deployed",
                                 "us-east-1",             "us-east-1")
ALB_CONTROLLER_ROLE     = prompt("ALB_CONTROLLER_ROLE",   "IAM role ARN for the AWS Load Balancer Controller",
                                 "arn:aws:iam::<aws-account-id>:role/pharma-dev-alb-controller-role",
                                 "arn:aws:iam::873135413040:role/pharma-dev-alb-controller-role")

default_gitops = os.path.join(DEFAULT_PROJECT_ROOT, "gitops")
GITOPS_PATH    = prompt("GITOPS_PATH",               "Local path to your gitops repo",
                        default_gitops,              default_gitops)

# Auto-fetch VPC ID from EKS cluster if not set in environment
VPC_ID = os.environ.get("VPC_ID", "")

if not VPC_ID:
    info(f"Auto fetching VPC ID for cluster '{CLUSTER_NAME}'...")
    VPC_ID, rc = run_cmd(
        ["aws", "eks", "describe-cluster", "--name", CLUSTER_NAME,
         "--region", AWS_REGION,
         "--query", "cluster.resourcesVpcConfig.vpcId",
         "--output", "text"],
        capture=True, ok_fail=True
    )
    if rc == 0 and VPC_ID != "None":
        log(f"VPC ID auto-detected: {VPC_ID}")
    else:
        VPC_ID = prompt("VPC_ID", "VPC ID where the EKS cluster runs", "vpc-cxxxxxxxxxxxxxxxx")

print()
print(" ----Configuration Summary ---------------------")
print(f"    Cluster         : {CLUSTER_NAME}")
print(f"    Region          : {AWS_REGION}")
print(f"    VPC ID          : {VPC_ID}")
print(f"    ALB role ARN    : {ALB_CONTROLLER_ROLE}")
print(" -----------------------------------------------")
print()
confirm = input("   Proceed with installation?  [Y/n]: ").strip() or "Y"

if confirm.upper() != "Y":
    print("Aborted.")
    sys.exit(0)
    
print()

# Configure kubectl

info(f"Updating kubeconfig for cluster '{CLUSTER_NAME}' in '{AWS_REGION}'...")
_, rc = run_cmd(
    ["aws", "eks", "update-kubeconfig", "--region", AWS_REGION, "--name", CLUSTER_NAME],
    ok_fail=True
)

if rc != 0:
    warn("kubeconfig update failed - continuing with existing context")

ctx, _ = run_cmd(["kubectl", "config", "current-context"], capture=True)
log(f"kubectl context: {ctx}")

# Add Helm repositories

print()
info("Adding Helm repositories")

for name, url in [
    ("eks",                 "https://aws.github.io/eks-charts"),
    ("external-secrets",    "https://charts.external-secrets.io"),
    ("argo",                "https://argoproj.github.io/argo-helm")
]:
    run_cmd(["helm", "repo", "add", name, url, "--force-update"], ok_fail=True)

run_cmd(["helm", "repo", "update"])
log("Helm repos updated")

# Step 1 - AWS Load Balancer Controller

print()
print("-------------------------------------------------------------")
print("    Step s of 3: AWS Load Balancer Controller")

    
