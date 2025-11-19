import os
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
import joblib
from datetime import datetime
from ml.prepared_data import prepared_data
from utils.logger import log as logger


class MushroomsModel:
    """Обучение модели классификации грибов"""    
    def __init__(self, filename):
        """Инициализация модели

        Args:
            filename: Входной файл .csv/.zip
        """        
        self.df = pd.read_csv(filename)
        self.scaler = MinMaxScaler()
        self.model = RandomForestClassifier(random_state=42, n_estimators=150, min_samples_split=10)
        self.pipeline = None
    
    def preprocess_data(self):
        """Препроцессинг данных"""        
        try:
            df = prepared_data(self.df)
            # делим датасет на целевую переменную(target) и независимые переменные(признаки)
            X = df.drop('class', axis=1)
            y = df['class']
            cat = [i for i in X.select_dtypes(include='object').columns]
            numeric_transformer = Pipeline(steps=[
                ('scaler', self.scaler)
            ])
            categorical_transformer = Pipeline(steps=[
                ('o_encoder', OneHotEncoder(handle_unknown='ignore'))
            ])
            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', numeric_transformer, ["square-mushroom"]),
                    ('cat', categorical_transformer, cat),
                    ])
            pipeline = Pipeline(steps=[
                ('preprocessor', preprocessor),
                ('classifier', self.model)
                ])
            # отделяем выборку на тренировочную и тестовую
            X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.25)
            pipeline.fit(X_train, y_train)
            self.pipeline = pipeline
        except Exception as e:
            logger.error(f"❌Возникла ошибка при препроцессинге: {e}")

    def fit_model(self):
        """Обучение и сохранение модели"""        
        try:
            artifact = {
                "model": self.pipeline,
                "trained_at": datetime.now().isoformat()

            }
            filename = "mushrooms_model.pkl"
            if os.path.exists(filename):
                logger.warning(f"Файл {filename} уже существует и будет перезаписан")
            joblib.dump(artifact, filename)
            logger.info("💾Модель успешно обучена и сохранена в корневом каталоге проекта")
        except Exception as e:
            logger.error(f"❌Возникла ошибка при сохранении модели в расширении .pkl: {e}")
