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

dest="s3://$bucket_name/$bucket_dir"
dest="${dest%/}"

# Pages and stylesheets change with every deploy and are covered by the
# CloudFront invalidation below, so browsers revalidate them often. Images keep
# their bytes across deploys, so they are cached for 30 days.
aws s3 cp $build_path "$dest" --recursive \
  --exclude "*assets/img/*" \
  --cache-control "public, max-age=600"

if [ -d "$build_path/assets/img" ]; then
  aws s3 cp $build_path/assets/img "$dest/assets/img" --recursive \
    --cache-control "public, max-age=2592000"
fi

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