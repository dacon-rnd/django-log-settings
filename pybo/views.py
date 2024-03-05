import logging

from django.http import HttpResponse

logger = logging.getLogger('pybo')

def index(request):
    logger.debug('d hello')
    logger.info('i hello')
    return HttpResponse('Hello World')