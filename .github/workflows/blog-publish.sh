#!/bin/bash -l

# Based on pukonu/action-deploy-webapp-aws@v.1.2.2

set -e

# check configuration

err=0

build_path=$1
bucket_name=$2
bucket_dir=$3
distribution_invalidation_path=$4
empty_bucket=$5
aws_region=AWS_REGION

ls -l $build_path

if [ -z "$AWS_ACCESS_KEY_ID" ]; then
  echo "AWS_ACCESS_KEY_ID was not found. Set this in your github secrets"
  err=1
fi

if [ -z "$AWS_SECRET_ACCESS_KEY" ]; then
  echo "AWS_SECRET_ACCESS_KEY was not found. Set this in your github secrets"
  err=1
fi

#if [ -z "$aws_region" ]; then
#  echo "Specify an AWS region"
#  err=1
#fi

if [ -z "$bucket_name" ]; then
  echo "Specify a bucket you will like to deploy to"
  err=1
fi

if [ $err -eq 1 ]; then
  exit 1
fi

output="AWS OUTPUT"
echo "::set-output name=aws-deploy-output::$output"

if [ "$empty_bucket" == "true" ]; then
  aws s3 rm s3://$bucket_name/$bucket_dir --recursive
fi

aws s3 cp $build_path s3://$bucket_name/$bucket_dir --recursive

if [ -z "$DISTRIBUTION_ID" ]; then
  echo "Skipping cloudfront invalidation..."
else

  if [ -z "$distribution_invalidation_path" ]; then
    echo "Specify the invalidation path. e.g. /* or /production/*"
    exit 1
  fi

  echo "Invalidating cloudfront..."
  aws cloudfront create-invalidation --distribution-id $DISTRIBUTION_ID --paths "$distribution_invalidation_path"
fi