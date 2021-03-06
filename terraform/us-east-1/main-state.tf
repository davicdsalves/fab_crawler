variable "region" {}
variable "bucket" {}
variable "tfstate" {}
variable "vpc_id" {}
variable "ssh_release_ip" {}
variable "instances_key_name" {}
variable "subnet_id" {}

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

module "securitygroup" {
  source = "./modules/securitygroup"
  vpc_id = "${var.vpc_id}"
  ssh_release_ip = "${var.ssh_release_ip}"
}

module "app_instances" {
  source = "./modules/instances"
  key_name = "${var.instances_key_name}"
  sg_admin_id = "${module.securitygroup.sg_pdf_worker}"
  subnet_id = "${var.subnet_id}"
}