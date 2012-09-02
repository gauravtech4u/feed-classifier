from wrapper import CollectionWrapper


class QuerySet(CollectionWrapper):
    """A set of results returned from a query. Wraps a MongoDB cursor,
providing :class:`~mongoengine.Document` objects as the results.
"""
    def __init__( self, db_col ):
        self.db_col=db_col

    def update(self,**kwargs):

        self.db_col.update( {'_id':self._id} , {"$set":kwargs} )


class QuerySetManager(object):

    def __init__(self,db_col):
        self.db_col=db_col

    def filter(self,**kwargs):

        data_list=self.db_col.find( kwargs )
        result_list = QueryList(self.db_col,kwargs)
        for data_dict in data_list:
            obj=QuerySet(self.db_col)
            for col_name,col_value in data_dict.items():
                setattr(obj,col_name,col_value)
            result_list.append(obj)
        return result_list

    def all(self):
        data_list=self.db_col.find( {} )
        result_list = QueryList(self.db_col)
        for data_dict in data_list:
            obj=QuerySet(self.db_col)
            for col_name,col_value in data_dict.items():
                obj.__setattr__(col_name,col_value)
            result_list.append(obj)
        return result_list

    def get(self,**kwargs):
        obj=QuerySet(self.db_col)
        data_dict=self.db_col.find_one( kwargs )
        result_list = []
        for col_name,col_value in data_dict.items():
            obj.__setattr__(col_name,col_value)
        result_list.append(obj)
        return result_list



class QueryList(list,QuerySetManager):
    def __init__(self,db_col,kwargs={}):
        self.kwargs=kwargs
        self.db_col=db_col

    def update(self,**kwargs):
        obj=QuerySet(self.db_col)
        self.db_col.update( self.kwargs , {"$set":kwargs} )

