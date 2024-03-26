# Barista Order Service


## Get Started
```
cp .env.example .env
make dev  # starts postgres, order-service in docker compose

# api docs for order service at
localhost:8000/docs
```

```
# Run app locally
poetry install
poetry run uvicorn --app-dir=order-service main:app --reload
```

![FlowChart](static/baristaOrderServiceDiagram.png "System Diagram")

## Overview

Order service handles taking orders via a REST endpoint.
POST /order
{
    "coffee_type": "latte | cappuccino | american | ...",
    "quantity": 1
}

After order is created, the order will be sent to coffee-service to be made. Depending on the coffee type, the time to create can vary (as noted in barista-service/menu.py)

Once coffee is made, a PUT request is made to the order to update it's order status to COMPLETED.

## TODOs

Improvements to make:

1. Add notification service to send email to users when coffee is ready.
2. Update order status to IN_PROGRESS when barista-service starts
3. Show example of running with multiple barista-service
4. Add simple frontend to make order
5. Fix user input validation
6. Expose API to show list of avaliable coffee/quantity. Support ran out of supplies
7. Add unit tests
