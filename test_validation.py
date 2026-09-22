import pandas as pd
from sklearn.model_selection import train_test_split
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.entity.config_entity import DataValidationConfig, TrainingPipelineConfig
from networksecurity.components.data_validation import DataValidation

df = pd.read_csv("Network_Data/phisingData.csv")
train_df, test_df = train_test_split(df, test_size=0.2)
train_df.to_csv("Network_Data/train.csv", index=False)
test_df.to_csv("Network_Data/test.csv", index=False)

trainingpipelineconfig = TrainingPipelineConfig()
data_validation_config = DataValidationConfig(trainingpipelineconfig)
dataingestionartifact = DataIngestionArtifact(
    trained_file_path="Network_Data/train.csv",
    test_file_path="Network_Data/test.csv"
)

data_validation = DataValidation(dataingestionartifact, data_validation_config)
print(data_validation.initiate_data_validation())