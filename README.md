## Infra Architecture
<img width="885" alt="KakaoTalk_20210124_144102088" src="https://user-images.githubusercontent.com/19552819/105622318-ef004180-5e53-11eb-8d95-35dacc79bc99.png">

## App Architecture
<img width="820" alt="KakaoTalk_20210124_144102088_01" src="https://user-images.githubusercontent.com/19552819/105622319-f0316e80-5e53-11eb-8197-ca0bb588cdf6.png">

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

