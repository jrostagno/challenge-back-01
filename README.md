# Notification service Backend Challenge

You have to build a microservice that exposes a REST api with two different
tables, users and states. Both tables should be open to creation, deletion,
or update. Every request must only accept this `Content-type: application/json`.

## Deployed App Running on HEROKU

### Badges

[![CircleCI](https://dl.circleci.com/status-badge/img/circleci/8UaiykmR7N7WoqrsjC7KCL/U7nKyJ9cdRMXgq46PTBHgr/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/circleci/8UaiykmR7N7WoqrsjC7KCL/U7nKyJ9cdRMXgq46PTBHgr/tree/main)

[![Coverage Status](https://coveralls.io/repos/github/jrostagno/challenge-back-01/badge.svg?branch=main)](https://coveralls.io/github/jrostagno/challenge-back-01?branch=main)

### How to run locally coveralls

```
COVERALLS_REPO_TOKEN=gLskLgZ58OYgHYPem2MLSnox65zICVe8t npm run test:cov
```

### Features

- Create new Users
- Login
- Create Notifiaction
- Edit Notification
- Delete Notification
- Get Notification by id
- Gel all Notifications

## Pre-Requisites

- Docker installed without SUDO Permission
- Docker compose installed without SUDO
- Ports free: 3000 and 5432

## How to run the APP

```
chmod 711 ./up_dev.sh
./up_dev.sh
```

## How to run the tests

```
chmod 711 ./up_test.sh
./up_test.sh
```

## Areas to improve

- Data should be moved from tests to an external file
- Generic method should be used to mock endpoints
- Error handling could be improved (I.E handle already existing user error)
- A Seed migration would be useful to have an already working app with data
- The ORM is being used with Synchronize instead of migrations. Migrations would be the best option
- Deployment could be done

## Errors to be fixed

- Docker app is not running properly

## Techs

- Nest: 11
- Node: Node20.11.1
- TypeORM
- Postgres

## Decisions made

- Clean Architecture: To be able to handle further changes in the future in a proper way.
- TypeORM: Because it is the already integrated ORM in the Nest Framework and it is the most popular ORM so it is easy to find fixes and people that know how to use it
- Docker: To make portable
- Jest/Testing/E2E: Jest is the most used testing framework of JS. Same argument as above. E2E testing was done because it is useless to always test every single part. That's why if the controller provide the proper answer the test has passed.

## Route

- Local: [API Swagger](http://localhost:8000/docs)

## Env vars should be defined

To find an example of the values you can use .env.example
