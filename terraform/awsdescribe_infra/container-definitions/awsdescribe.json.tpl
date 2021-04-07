[
  {
    "essential": true,
    "name": "dajngo",
    "image": "foo",
    "entryPoint": ["sh","-c"],
    "command": ["python manage.py migrate && supervisord -c ./supervisord.conf"],
    "cpu": 0,
    "memory": null,
    "memoryReservation": null,
    "portMappings": [
      {
        "containerPort": 8000,
        "hostPort": 8000,
        "protocol": "tcp"
      }
    ],
    "environment": ${container_df_env_values},
    "secrets" : ${container_df_env_secret_values}
  },
  {
    "essential": false,
    "name": "redis",
    "image": "foo",
    "cpu": 0,
    "memory": null,
    "memoryReservation": null,
    "portMappings": [
      {
        "containerPort": 6379,
        "hostPort": 6379,
        "protocol": "tcp"
      }
    ]
  }
]
