## Infra Architecture
<img width="883" alt="KakaoTalk_20210124_160900930" src="https://user-images.githubusercontent.com/19552819/105623961-4eb11980-5e61-11eb-8f7d-b7f0aa9caf82.png">

## App Architecture
<img width="818" alt="KakaoTalk_20210124_160900930_01" src="https://user-images.githubusercontent.com/19552819/105623963-4fe24680-5e61-11eb-948e-2df552ed4731.png">

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

