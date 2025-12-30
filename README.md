# Notification Service – Backend Challenge

Backend microservice built with **FastAPI** + **PostgreSQL** that exposes a REST API
to manage **users** and their **notifications**.

- Auth with **JWT Bearer tokens**
- Protected routes for notifications
- CI with **CircleCI**
- Coverage reporting with **Coveralls**

---

## Deployed App at Heroku

- **Swagger (OpenAPI docs):**  
  [https://challenge-notification-a633a6dac8ad.herokuapp.com/docs](https://challenge-notification-a633a6dac8ad.herokuapp.com/docs)

---

## Badges

[![CircleCI](https://dl.circleci.com/status-badge/img/circleci/8UaiykmR7N7WoqrsjC7KCL/U7nKyJ9cdRMXgq46PTBHgr/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/circleci/8UaiykmR7N7WoqrsjC7KCL/U7nKyJ9cdRMXgq46PTBHgr/tree/main)

[![Coverage Status](https://coveralls.io/repos/github/jrostagno/challenge-back-01/badge.svg?branch=main)](https://coveralls.io/github/jrostagno/challenge-back-01?branch=main)

---

## Features

### Users

- Create new users
- Login (JWT)

### Notifications (protected)

- Create notification
- Update notification
- Delete notification
- Get notification by id
- Get all notifications

---

## Tech Stack

- **Python**: 3.12
- **FastAPI**
- **SQLAlchemy**
- **PostgreSQL**
- **Pytest**
- **Docker / Docker Compose**
- **CircleCI**
- **Coveralls**

---

## Pre-Requisites

- Docker installed without SUDO Permission
- Docker compose installed without SUDO
- Ports free: 8000 and 5432

## How to run the APP

```
chmod +x ./up_dev.sh
./up_dev.sh
```

## How to run the tests

```
chmod +x ./up_test.sh
./up_test.sh
```

## Database Migrations

This project uses **Alembic** to manage database schema migrations.

### Run migrations

```bash
alembic upgrade head
```

## External Delivery Service (Mock Microservice)

This project includes a second microservice called delivery-service, used to simulate an external notification delivery provider.

It is implemented as a separate FastAPI application and is started automatically when running the project using Docker.

The Notification API communicates with this service when a notification is created, in order to simulate real-world message delivery (email / SMS / push).

### What this service does

-Receives delivery requests from the main API

-Applies basic channel-specific delivery rules (SMS, email, push)

-Returns a delivery result (sent / error)

-Acts as an external dependency for integration testing

This enables:

-Testing real communication between services

-Simulating provider success / failure scenarios

-Mocking the dependency in automated tests

### How it runs

The service is built and started automatically via Docker Compose:

```bash
app (port 8000)
delivery-service (port 8001)
postgres
```

The main API communicates internally using:

```bash
http://delivery-service:8001/deliver
```

In local mode, no additional setup is required — simply run:

```bash
./up_dev.sh
```

## Areas to improve

- Move test data to external fixtures or factory modules
- Generic method should be used to mock endpoints
- Error handling could be improved (I.E handle already existing user error)
- Add seed data for easier local testing

## Decisions made

Clean Architecture
Chosen to keep the business logic independent from frameworks and infrastructure, allowing easier future changes and better testability.

SQLAlchemy ORM
Used for database interaction due to its flexibility, maturity, and strong integration with FastAPI.

Docker
Ensures portability and allows the reviewer to run the project without installing dependencies locally.

Pytest
Used for testing due to its simplicity, readability, and strong ecosystem in Python.

Integration tests focus
Tests are written at the API level to validate real behavior instead of isolated units.

## Environment variables

Environment variables must be defined before running the app.

An example file is provided:

.env.example

## Route

- Local: [API Swagger](http://localhost:8000/docs)

### Formatting & Linting

```bash
black .
ruff check .
```

## Env vars should be defined

To find an example of the values you can use .env.example
