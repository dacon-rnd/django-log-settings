# django settings and logging test
* application
  - 예제 프로젝트 생성(pybo)
      ``` 
      $ django-admin startapp pybo 
      ```
  - `pybo/views.py` 코드
    ``` 
    logger = logging.getLogger('pybo')

    def index(request):
      logger.debug('d hello')
      logger.info('i hello')
      return HttpResponse('Hello World')
    ```
  - `config/urls.py` 코드
    ```
    urlpatterns = [
      path('admin/', admin.site.urls),
      path('pybo/', views.index),
    ] 
    ```
* 설정 파일 수정
  - create settings
    ```
    $ mkdir config/settings
    $ mv config/settings.py config/settings/base.py
    ```
  - `config/settings/base.py`에 아래 코드 추가
    ``` 
    # 로깅설정
    LOGGING = {
      'version': 1,
      'disable_existing_loggers': False,
      'filters': {
        'require_debug_false': {
          '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
          '()': 'django.utils.log.RequireDebugTrue',
        },
      },
      'formatters': {
        'django.server': {
          '()': 'django.utils.log.ServerFormatter',
          'format': '[{server_time}] {message}',
          'style': '{',
        },
        'standard': {
          'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
      },
      'handlers': {
        'console': {
          'level': 'DEBUG',
          'filters': ['require_debug_true'],
          'class': 'logging.StreamHandler',
        },
        'django.server': {
          'level': 'INFO',
          'class': 'logging.StreamHandler',
          'formatter': 'django.server',
        },
        'mail_admins': {
          'level': 'ERROR',
          'filters': ['require_debug_false'],
          'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
          'level': 'INFO',
          # 'filters': ['require_debug_false'],
          'class': 'logging.handlers.RotatingFileHandler',
          'filename': BASE_DIR / 'logs/mysite.log',
          'maxBytes': 1024*1024*5,  # 5 MB
          'backupCount': 5,
          'formatter': 'standard',
        },
      },
      'loggers': {
        'django': {
          'handlers': ['console', 'mail_admins', 'file'],
          'level': 'INFO',
        },
        'django.server': {
          'handlers': ['django.server'],
          'level': 'INFO',
          'propagate': False,
        },
        'pybo': {
          'handlers': ['file', 'console'],
          'level': 'INFO',
          'propagate': False,
        }
      }
    }
    ```
  - 위 세팅 중요한 부분 설명
    - console 설정
      - `DEBUG`
    - file 설정
      - `INFO`
    - pybo 설정
      - `INFO`
  - `config/settings/dev.py` 설정
    ``` 
    from .base import *

    LOGGING['loggers']['pybo']['level'] = 'DEBUG' 
    ```
  - `config/settings/prod.py` 설정
    ``` 
    from .base import *

    LOGGING['loggers']['pybo']['level'] = 'INFO' 
    ```
  - dev 테스트
    - console에 `INFO`와 `DEBUG` 메시지 확인
    - file에 `INFO` 메시지 확인
    ``` 
    $ python manage.py runserver --settings=config.settings.dev
    ```
  - prod 테스트
    - console에 `INFO` 메시지 확인
    - file에 `INFO` 메시지 확인 
    ``` 
    $ python manage.py runserver --settings=config.settings.prod
    ```