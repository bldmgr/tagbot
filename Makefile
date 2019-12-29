common = boto3wrapper.py utils.py
lambda_ec2 = ec2_function.py
lambda_rds = rds_function.py
lambda_s3 = s3_function.py
lambda_dynamodb_cw = dynamodb_cloudwatch_function.py
lambda_dynamodb_sfn = dynamodb_sfn_function.py
lambda_redshift = redshift_function.py
lambda_sfn_redshift = redshift_sfn_function.py

default:
	@echo
	@echo 'Usage:'
	@echo
	@echo '    make build      package Lambda code for AWS deployment'
	@echo '    make install    install the package in a virtual environment'
	@echo '    make lint       lint check the code'
	@echo '    make test       run the test suite'
	@echo '    make clean      cleanup all temporary files'
	@echo

install:
	pip3 install virtualenv
	cd lambda; virtualenv -p python3 venv;\
	. venv/bin/activate;\
	venv/bin/pip install placebo;\
	venv/bin/pip install httmock;\
	venv/bin/pip install boto3;\
	venv/bin/pip install pylint;\

lint:
	cd lambda; venv/bin/pylint --rcfile ../.pylintrc *.py;\

build:
	@rm -rf build/
	@mkdir -p build/ec2
	@mkdir -p build/rds
	@mkdir -p build/s3
	@mkdir -p build/dynamodb
	@mkdir -p build/redshift
	cd lambda;\
	zip -r ../build/ec2/ec2.zip $(lambda_ec2) $(common);\
	zip -r ../build/rds/rds.zip $(lambda_rds) $(common);\
	zip -r ../build/s3/s3.zip $(lambda_s3) $(common);\
	zip -r ../build/dynamodb/dynamodb_cw.zip $(lambda_dynamodb_cw) $(common);\
	zip -r ../build/dynamodb/dynamodb_sfn.zip $(lambda_dynamodb_sfn) $(common);\
	zip -r ../build/redshift/redshift.zip $(lambda_redshift) $(common);\
	zip -r ../build/redshift/redshift_sfn.zip $(lambda_sfn_redshift) $(common);\

test: install lint
	cd lambda; venv/bin/python3 -m unittest -v;\

clean:
	@rm -rf lambda/venv/
	@rm -rf __pycache__/
	@rm -rf build/
	@rm -rf *_package.yaml

.PHONY: test build clean lint install