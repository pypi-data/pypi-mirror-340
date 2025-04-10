from delta import DeltaTable
from pyspark.sql import DataFrame
from pyspark.sql.functions import lit, last

from ..data_sinks.base import BaseDataSink
from ..validators.lakehouse_path_validator import LakehousePathValidator

class DeltaTableDataSink(BaseDataSink):
    @classmethod
    def create(cls, delta_location: str, schema=None, input_spark=None, input_validator=None) -> 'DeltaTableDataSink':
        if input_validator:
            validator = input_validator
        else:
            validator = LakehousePathValidator()
        path_is_valid = validator.validate(delta_location)
        if not path_is_valid:
            raise ValueError(f"Invalid path: {delta_location}. Please use the following structure: {validator.path_examples()}")
        return cls(delta_location, schema, input_spark)

    def __init__(self, delta_location: str, schema=None, input_spark=None) -> None:
        self.delta_location = delta_location
        self.schema = schema
        self.spark = input_spark

    def put(self, df: DataFrame) -> None:
        df.write.format('delta').option('mergeSchema', "true").mode('append').save(self.delta_location)

    def get_schema(self):
        return self.schema

    def upsert(self, df: DataFrame, merge_key='id') -> None:
        """
        Perform upsert operation using a merge key (default: 'id')
        Updates all columns except the merge key
        """
        if not df.columns:
            raise ValueError("DataFrame cannot be empty")
            
        if merge_key not in df.columns:
            raise ValueError(f"Merge key '{merge_key}' not found in DataFrame columns: {df.columns}")
            
        # Ensure no null values in merge key column
        null_keys = df.filter(df[merge_key].isNull()).count()
        if null_keys > 0:
            raise ValueError(f"Found {null_keys} null values in merge key column '{merge_key}'")

        schema = self.schema if self.schema else df.schema

        # Create table if it doesn't exist
        try:
            delta_table = DeltaTable.forPath(self.spark, self.delta_location)
            # Verify merge key exists in target table
            target_cols = self.spark.read.format("delta").load(self.delta_location).columns
            if merge_key not in target_cols:
                raise ValueError(f"Merge key '{merge_key}' not found in target table columns: {target_cols}")
        except Exception as e:
            if "not a Delta table" in str(e):
                # First write - create table
                df.write.format('delta').mode('overwrite').save(self.delta_location)
                delta_table = DeltaTable.forPath(self.spark, self.delta_location)
            else:
                raise e

        # Create update dict for all columns except merge key
        update_dict = {
            f"current.{col}": f"new.{col}" 
            for col in df.columns 
            if col != merge_key
        }
        
        if not update_dict:
            raise ValueError(f"No columns to update. DataFrame only contains merge key '{merge_key}'")

        # Perform merge operation
        try:
            (delta_table.alias("current")
             .merge(
                source=df.alias("new"),
                condition=f"current.{merge_key} = new.{merge_key}"
             )
             .whenMatchedUpdate(
                set=update_dict
             )
             .whenNotMatchedInsertAll()
             .execute())
            
            # Verify the operation
            result_count = self.spark.read.format("delta").load(self.delta_location).count()
            if result_count == 0:
                raise ValueError("Upsert resulted in empty table")
                
        except Exception as e:
            raise ValueError(f"Upsert operation failed: {str(e)}")
