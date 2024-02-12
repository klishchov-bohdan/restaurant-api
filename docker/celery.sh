#!/bin/bash


if [[ "${1}" == "celery" ]]; then
  celery -A app.background.tasks:worker worker -l INFO &
  celery -A app.background.tasks:worker beat -l INFO
elif [[ "${1}" == "flower" ]]; then
  celery -A app.background.tasks:worker flower
fi
