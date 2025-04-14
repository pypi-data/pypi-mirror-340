# SerwerSMS.pl Python Client API
Python client for remote communication with SerwerSMS.pl API v2

Attention. The current version works based on the API token.

In order to authorize via an API Token, it must be generated on the Customer Panel side in the Interface Settings → HTTPS API → API Tokens menu. The authorization header format follows the Bearer token format.

#### Example usage
```python
import sys
import json

from serwersms import SerwerSMS

api = SerwerSMS('token')

try:

    params = {
        'test': 'true',
        'details': 'true'
    }

    response = api.message.send_sms('500600700', 'Test message', 'INFORMACJA', params)

    result = json.loads(response)

    if 'items' not in result:
        raise Exception('Empty items')

    for item in result['items']:
        print(item['id'] + ' - ' + item['phone'] + ' - ' + item['status'])
        
except Exception:

    print('ERROR: ', sys.exc_info()[1])
```

#### Sending SMS
```python
api = SerwerSMS('token')

try:

    params = {
        'details': 'true'
    }

    response = api.message.send_sms('500600700', 'Test message', 'INFORMACJA', params)
    
    print(response)
    
except Exception:

    print('ERROR: ', sys.exc_info()[1])
```

#### Sending personalized SMS
```python
api = SerwerSMS('token')

try:

    messages = []

    message1 = {
        'phone': '500600700',
        'text': 'First message'
    }
    
    messages.append(message1)

    message2 = {
        'phone': '600700800',
        'text': 'Second  message'
    }
    
    messages.append(message2)

    params = {
        'details': 'true'
    }

    response = api.message.send_personalized(messages, 'INFORMACJA', params)
    
    print(response)
    
except Exception:

    print('ERROR: ', sys.exc_info()[1])
```

#### Downloading delivery reports
```python
api = SerwerSMS('token')

try:

    params = {
        'id': 'aca3944055'
    }
    
    response = api.message.reports(params)
    
    print(response)
    
except Exception:

    print('ERROR: ', sys.exc_info()[1])
```

#### Downloading incoming messages
```python
api = SerwerSMS('token')

try:

    params = {
        'phone': '500600700'
    }
    response = api.message.recived('ndi',params)
    
    print(response)
    
except Exception:

    print('ERROR: ', sys.exc_info()[1])
```

## Requirements
Python 3.5.*

## Documentation
http://dev.serwersms.pl

## API Console
http://apiconsole.serwersms.pl
