## Overview

This repository contains the services and utilities that need to run asynchronously.

This allows decoupling between unrelated parts of the application.

While inserting questions and answers, as long as the API is able to capture the question and answer data, it's job is over.
The translation to different supported languages should happen asynchronously.


## Services

- Translation
- Email Sending
