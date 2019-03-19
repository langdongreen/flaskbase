import logging
from functools import wraps

log = logging.getLogger(__name__)

    
def log_error(d):
    '''Log any exceptions'''
         
    def decorated_function(*args, **kwargs):
     
        try:
         
            return d(*args, **kwargs)
         
        except Exception as e:
         
            if log:
         
                log.exception(e)
         
            raise
      
    return d


