# CRM-API
CRM API is an application that allows you to create, get, update and delete customers.
Change 1

# Functions available
These are the five options available:
- **Create new customer**
- **Get one customer**
- **Get all customers**
- **Update a customer**
- **Delete a customer**

# How to run CRM-API
- Go to Terminal
- Introduce the following command: docker build -t exchange github.com/eavilesmo/CRM-API#main
- Introduce the following command: docker run --publish 8000:5000 exchange
- Introduce the following command: curl localhost:8000
- Navigate to: http://127.0.0.1:8000
