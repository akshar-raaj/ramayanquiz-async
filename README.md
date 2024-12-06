## Overview

Powers the asynchronous services and utilities needed for [RamayanQuiz](http://ramayanquiz.com/).

This allows decoupling unrelated parts of the application and provide better separation of concern.

## Tech Stack

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![RabbitMQ](https://img.shields.io/badge/Rabbitmq-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white) ![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)

| Category | Choice |
|----------|--------|
| Language | Python, a powerful duck-typed language that allows RAD |
| Message Broker | RabbitMQ, a powerful and versatile message broker supporting exchanges and queues |
| OpenAI | OpenAI API to perform translation to different languages |

## Setup

Copy `.env.example` to `.env` and fill the relevant values.

    $ cp .env.example .env

Build the Docker image

    $ docker build -t ramayanquiz-async .

Run the Docker container

    $ docker run --name ramayanquiz-async -v .:/app ramayanquiz-async

Any message sent to RabbitMQ queue `translate-hindi` would be recieved by the receiver and worked upon.

## Services

- Translation
- Email Sending

### Translation

Questions have a field `question` which contains English Text. It needs to be translated to Hindi in Devanagari script, and similarly to Telugu in Telugu Lipi.
OpenAI API is being used to perform this translation and the translated text is being persisted back into the database.
