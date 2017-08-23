variable "region" {}
variable "bucket" {}
variable "tfstate" {}
variable "project-name" {}

terraform {
  required_version = ">= 0.10.2"
  backend "s3" {}
}

provider "aws" {
  profile = "default"
  region = "${var.region}"
}

data "terraform_remote_state" "main-state" {
  backend = "s3"
  config {
    bucket = "${var.bucket}"
    key    = "${var.tfstate}"
    region = "${var.region}"
    profile = "default"
  }
}