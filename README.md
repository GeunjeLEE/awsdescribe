## Infra Architecture

## App Architecture

- web
    - django
    - 로컬에서 가동 시 .env 필요
- db(django backend & task result backend)
    - mysql 5.7
- broker
    - redis
- asynchronous task queue
    - python celery
- periodic tasks scheduler
    - python celery beat
- service daemon
    - python supervisor

