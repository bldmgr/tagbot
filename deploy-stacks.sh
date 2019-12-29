#!/bin/bash

declare -a REGIONS_DEFAULT=("us-east-1" "us-east-2" "us-west-1" "us-west-2" "ap-northeast-1" "ap-south-1" "ap-southeast-1" "ap-southeast-2" "ca-central-1" "cn-north-1" "cn-northwest-1" "eu-central-1" "eu-west-1" "eu-west-2" "sa-east-1")
declare -a AWS_SERVICES=("ec2" "rds" "s3" "dynamodb" "redshift")

if [ $# -eq 0 ]; then
    echo ""
    echo "No arguments provided"
    echo ""
    echo "Usage:"
    echo "  deploy-stacks.sh [options]"
    echo ""
    echo "  Initial setup, run deploy-stacks.sh with the create-infra action."
    echo ""
    echo "Options:"
    echo ""
    echo "  --account or -a         :AWS account profile (see ~/.aws/credentials)"
    echo "  --region or -r          :AWS region, default is us-east-1"
    echo "  --action or -ac         :Action that you want to perform on the CloudFormation stack, actions:"
    echo "                                  o create-infra"
    echo "                                  o delete-infra"
    echo "                                  o create-stack - also functions as update-stack"
    echo "                                  o delete-stack"
    echo "                                  o create-all-services"
    echo "                                  o delete-all-services"
    echo "  --awsservice or -as     :AWS service to perform action on, services:"
    echo "                                  o rds"
    echo "                                  o ec2"
    echo "                                  o s3"
    echo "                                  o dynamodb"
    echo "                                  o redshift"
    echo ""
    echo "Example:"
    echo "  Setup infrastructure:"
    echo "    ./deploy-stacks.sh -a <aws_account> -r us-east-1 -ac create-infra"
    echo ""
    echo "  Setup a single service, EC2 for instance:"
    echo "    ./deploy-stacks.sh -a <aws_account> -r us-east-1 -ac create-stack -as ec2"
    echo ""
    echo "  Setup all services:"
    echo "    ./deploy-stacks.sh -a <aws_account> -r us-east-1 -ac create-all-services"
    echo ""
    exit 1
fi

while (( $# > 1 )); do
	key="$1"
	case $key in
    -ac|--action)
      ACTION="$2"
      shift # past argument
      ;;
		-a|--account)
			ACCOUNT="$2"
			shift # past argument
			;;
		-as|--awsservice)
      SERVICE="$2"
      shift # past argument
      ;;
		-r|--region)
      REGION="$2"
      shift # past argument
      ;;
	esac
	shift # past argument or value
done

CFACTION=${ACTION:-"create-stack"}
REGIONS=${REGION:-${REGIONS_DEFAULT[@]}}
PROFILE=${ACCOUNT:-"default"}
SAM_TEMPLATE=$SERVICE"_sam.yaml"
SAM_PACKAGE=$SERVICE"_sam_package.yaml"
STACKNAME="AutoTag-"$SERVICE
S3BUCKET="auto-tag-cf-data"

for region in $REGIONS; do
	    
	case $CFACTION in
	  create-infra)
	    echo Creating S3 buckets for AutoTag infrastructure in region "$region"
	    aws cloudformation package --template-file s3_infra.yaml --output-template-file s3_infra_package.yaml --s3-bucket "$S3BUCKET" --region "$REGIONS" --profile "$PROFILE"
	    aws cloudformation deploy --template-file s3_infra_package.yaml --stack-name AutoTag-Infra --capabilities CAPABILITY_IAM --region "$REGIONS" --profile "$PROFILE"
	  ;;
	  delete-infra)
	    echo Deleting AutoTag infrasture stack. THIS WILL FAIL IF ANY S3 BUCKETS CONTAIN DATA.
	    aws cloudformation delete-stack --stack-name AutoTag-Infra --region "$REGIONS" --profile "$PROFILE"
	  ;;
		create-stack)
		  echo Creating stack for region "$region"
		  make build
			aws cloudformation package --template-file "$SAM_TEMPLATE" --s3-bucket "$S3BUCKET" --output-template-file "$SAM_PACKAGE"
			aws cloudformation deploy --template-file "$SAM_PACKAGE" --stack-name "$STACKNAME" --capabilities CAPABILITY_IAM --region "$REGIONS" --profile "$PROFILE"
		;;
    delete-stack)
			echo Deleting stack for region "$region"
			aws cloudformation delete-stack --stack-name "$STACKNAME" --region "$REGIONS" --profile "$PROFILE"
		;;
		create-all-services)
		  make build
		  for service in "${AWS_SERVICES[@]}"; do
				echo Creating stack for "$service" in region "$region"
				aws cloudformation package --template-file "$service""_sam.yaml" --s3-bucket "$S3BUCKET" --output-template-file "$service""_sam_package.yaml"
				aws cloudformation deploy --template-file "$service""_sam_package.yaml" --stack-name "AutoTag-""$service" --capabilities CAPABILITY_IAM --region "$REGIONS" --profile "$PROFILE"
			done
		;;
		delete-all-services)
		  for service in "${AWS_SERVICES[@]}"; do
				echo Deleting stack for "$service" in region "$region"
				aws cloudformation delete-stack --stack-name AutoTag-"$service" --region "$REGIONS" --profile "$PROFILE"
			done
		;;

	esac

done