# Complaza Backend Stack

## Cloudformation Template
### Input
- From Frontend: Cognito, S3 bucket 
- From ML: Sagemaker endpoint, Opensearch

### Output
- API Gateway endpoint

### Resources created
Lambda functions:
LF0: Call ML endpoint to return product names
LF1: Call 3rd party APIs to fullfil search and save to user's search history