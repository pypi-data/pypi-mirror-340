Influenzanet API Library
=====

influenzanet.api is a python library to work with influenzanet API

## Installation

```python
pip install influenzanet.api
```

## Contents

- `ManagementAPIClient` : is the main class handling connection and operations of the platform's Management API

### Paginated Helpers

Some helpers class are provided to handle the pagination and iter over fetched results using for ... in

- `ParticpantStatePaginaged` : call `get_participant_state_paginated` with pagi 

```python

from influenzanet.api import ManagementAPIClient, ParticpantStatePaginaged

client = ManagementAPIClient('https://admin.example.com', credentials)

pager = ParticpantStatePaginaged(client, page_size=5, study_key='my_study')

# By default, intial page is 1, but it's possible to change it using
# pager.page = 10 # start from page 10 (you must be sure of the page count...)

for result in pager:
    print("Fetched page %d with %d" % (result.page, len(result)))
    for item in result:
        print(item)
```


