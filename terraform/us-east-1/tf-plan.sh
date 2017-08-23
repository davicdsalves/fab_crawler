#!/usr/bin/env bash
set -o errexit

FILE='terraform.tfvars'
BUCKET=$(grep -w bucket ${FILE} | awk -F"\"" '{print $2}')
REGION=$(grep -w region ${FILE} | awk -F"\"" '{print $2}')

echo "bucket[${BUCKET}], region[${REGION}]"

terraform init -backend=true -get=true -backend-config key=terraform.tfstate \
  -backend-config bucket=${BUCKET} \
  -backend-config profile=default \
  -backend-config region=${REGION}