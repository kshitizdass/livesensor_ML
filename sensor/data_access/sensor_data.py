import sys
import pandas as pd
import numpy as np
import json
from sensor.configuration.mongodb_db_connection import MongoDBClient

from sensor.constant.database import DATABASE_NAME

from sensor.exception import SensorException

from typing import Optional

class SensorData:
    """This class will help to export entire mongo db record as pandas DataFrame"""

    def __init__(self):
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise SensorException(e,sys)

    def save_csv_file(self,file_path,collection_name:str,database_name:Optional[str] = None):
        try:
            data_frame = pd.read_csv(file_path)
            data_frame.reset_index(drop=True,inplace=True)
            records = list(json.load(data_frame.T.to_json()).values())

            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]

            collection.insert_many(records)
            return len(records)

        except Exception as e:
            pass

    def export_collection_as_dataframe(self,collection_name:str,database_name:Optional[str]=None) ->pd.DataFrame:
        """export entire colelction as dataframe and return pd.dataframe of the collection"""

        try:
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]
        
            df = pd.DataFrame(list(collection.find()))        

            if"_id" in df.columns.to_list():
                df=df.drop(columns=["_id"],axis=1)   
 
            df.replace({"na":np.nan},inplace=True)

            return df
        

        except Exception as e:
            raise SensorException(e,sys)