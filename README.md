# Complaza Backend Stack

## Backend Resources

### Lambda functions:
- LF0: Call ML endpoint to return product names
- LF1: Call 3rd party APIs to fullfil search and save to user's search history
- LF2: Interaction with the wishlist table
- LF3: Return search history
- LF4: Get price and update price history
- LF5: Get product details and price history
### Databases:
- SearchHistoryTable (uid, datetime, imgKey, q)
- ProductTable (id, created, image, link, name, price, retailer)
- WishlistTable (uid, pid, created)
- PriceHistoryTable (pid, date, price)
### API gateway
### CodePipeline (CI/CD)
### OpenSearch
### SageMaker (ML model)

## Cloudformation Template
### Input
- From Frontend: Cognito, S3 bucket 
- From ML: SageMaker endpoint, OpenSearch endpoint
- External API key

### Output
- API Gateway endpoint

### Structure
<img width="993" alt="resources" src="https://user-images.githubusercontent.com/49623311/164880659-f330aab4-5ede-4293-9fc5-d6b182a3ce97.png">
