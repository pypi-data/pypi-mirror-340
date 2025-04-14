
from .management_api import ManagementAPIClient, ApiError, ReponseMeta
from typing import Optional,Dict
class ResultError(ValueError):
    def __init__(self, message, result):
        super(ValueError, self).__init__(message)
        self.result = result


class PaginatedResult:
    """
        Holds results of an iteration of paginated request
    """
    def __init__(self, page, items):
        self.page = page
        self.items = items

    def __iter__(self):
        return iter(self.items)
    
    def __len__(self)->int:
        return len(self.items)
    

class PaginatedRequest:
    """
    PaginatedRequest handle pagination fetching logic for paginated methods 
    It implements the iterator methods to be usable in for loop
    """

    def __init__(self, client:ManagementAPIClient, page:int, page_size: int):
        self.client = client
        self.page = page
        self.page_size = page_size
        self.page_count = None
        self.total_count = None
        self.field_page = 'page'
        self.field_page_size = 'pageSize'
        self.field_page_count = 'pageCount'
        self.field_items = 'items'
        self.field_total = 'itemCount'
        self.use_pagination_object = False

    def fetch(self):
        """
            This method must be implemented by child to call the actual client method
        """
        raise NotImplementedError()

    def next(self):
        if self.page_count is None:
            return True
        if self.page > self.page_count:
            return False
        return True
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.next():
            return self.run()
        else:
            raise StopIteration()

    def check_field(self, field, data:Dict):
        if field not in data:
            print("Known keys", data.keys())
            raise ResultError("Result doenst contains '%s' field" % (field), data)

    def run(self):
        """
            Run paginated query for a page
        """
        r = self.fetch()
        if not isinstance(r, dict):
            raise ResultError("Result is not a dictionnary", r)
        if self.use_pagination_object:
            pagination = r['pagination']
        else:
            pagination = r
        
        current = pagination[self.field_page]
        
        self.check_field(self.field_page, pagination)
        self.check_field(self.field_items, r)

        fetched_count = len(r[self.field_items])

        if self.page_count is None:
            if self.field_page_count in pagination:
                page_count = pagination[self.field_page_count]
            else:
                # For some query the page_count is not provided if there is only one page
                if fetched_count == 0:
                    page_count = current
                else:
                    raise ResultError("Result doenst contains '%s' field" % (self.field_page_count), r)
        
            self.page_count = page_count
        
        if self.field_total in pagination:
            total = pagination[self.field_total]
            if self.total_count is None:
                self.total_count = total
        results = PaginatedResult(current, r[self.field_items])
        self.page = current + 1
        return results


class ParticpantStatePaginaged(PaginatedRequest):

    def __init__(self, client: ManagementAPIClient, page_size: int, study_key:str, query:dict=None, sorted_by:dict=None ):
        super().__init__(client, 1, page_size)
        self.study_key = study_key
        self.query = query
        self.sorted_by = sorted_by
    
    def fetch(self):
        return self.client.get_participant_state_paginated(self.study_key, self.page, self.page_size, self.query, self.sorted_by)
    
class SurveyResponseJSONPaginated(PaginatedRequest):

    def __init__(self, client:ManagementAPIClient, 
            page_size:int, 
            study_key: str, 
            survey_key: str, 
            **kwargs):
        super().__init__(client, 1, page_size)
        self.use_pagination_object = True
        self.field_page = 'page'
        self.field_page_size = 'page_size'
        self.field_page_count = 'page_count'
        self.field_total = 'item_count'
        self.field_items = 'responses'
        self.study_key = study_key
        self.survey_key = survey_key
        self.args = kwargs
    
    def fetch(self):
        return self.client.get_survey_responses_json_paginated(self.study_key, self.survey_key, page=self.page, page_size=self.page_size, **self.args)
    