from connection import db
from queryset import QuerySetManager
from wrapper import CollectionWrapper

class CollectionMapping( CollectionWrapper ):

    db_col=None

    def __init__( self, model ):
        self.db_col = db[model]
        self.objects=QuerySetManager(self.db_col)



class CollectionContentType( CollectionWrapper ):

    def __init__( self ):
        self.db_col = db['mongo_content']
        self.objects=QuerySetManager(self.db_col)

    def collection_keys( self, collection_name ):
        self.db_col.find( {'collection_name':collection_name} ).key_names