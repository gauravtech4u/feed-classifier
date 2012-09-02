from connection import db


class CollectionWrapper( object ):

    def load_json( self, kwargs ):
        self.db_col.insert( kwargs )

    def find_one( self, kwargs ):
        return self.db_col.find_one( kwargs )

    def find( self, kwargs ):
        return self.db_col.find( kwargs )

    def save( self, **kwargs ):
        self.db_col.insert( kwargs )

    def update( self, find_dict, set_dict ):
        self.db_col.update( find_dict, set_dict )

    def create_indexes(self,args_list):
        self.db_col.create_indexes(args_list)

    def delete_all(self):
        self.db_col.remove()

    @classmethod
    def collection_names( self ):
        return db.collection_names()