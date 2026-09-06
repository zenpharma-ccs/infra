terraform {
    backend "s3" {
        bucket = "zenpharma-terraform-state-ccs"
        key = "envs/dev/terraform.tfstate"
        region = "us-east-1"
        encrypt = true
        use_lockfile = true
    }
}