import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error
import pickle

# Создаем датасет ноутбуков
data = {
    'brand': ['Apple']*8 + ['Dell']*8 + ['HP']*8 + ['Lenovo']*8 + ['Asus']*8 + ['Acer']*8,
    'model': [
        # Apple
        'MacBook Air M1', 'MacBook Pro 13"', 'MacBook Pro 16"', 'MacBook Air M2',
        'iMac 24"', 'Mac Mini', 'Mac Studio', 'Mac Pro',
        # Dell
        'XPS 13', 'XPS 15', 'Inspiron 15', 'Latitude 14',
        'Alienware m15', 'Vostro 15', 'Precision 3560', 'G15',
        # HP
        'Pavilion 15', 'Envy x360', 'Spectre x360', 'Omen 15',
        'EliteBook 840', 'ProBook 450', 'ZBook Fury', 'Victus 16',
        # Lenovo
        'ThinkPad X1', 'Yoga Slim 7', 'Legion 5', 'IdeaPad 3',
        'ThinkBook 14', 'Legion 7', 'Yoga 9i', 'ThinkPad P15',
        # Asus
        'ZenBook 14', 'ROG Zephyrus', 'VivoBook 15', 'TUF Gaming',
        'ExpertBook', 'ROG Strix', 'ProArt StudioBook', 'Chromebook',
        # Acer
        'Swift 3', 'Nitro 5', 'Aspire 5', 'Predator Helios',
        'Spin 5', 'ConceptD 3', 'TravelMate P4', 'Chromebook 314'
    ],
    'ram': np.random.choice([4, 8, 16, 32], 48),
    'storage': np.random.choice([256, 512, 1024, 2048], 48),
    'screen_size': np.round(np.random.uniform(13.0, 17.0, 48), 1),
    'price': np.random.randint(500, 3500, 48)
}

# Создаем DataFrame
df = pd.DataFrame(data)

# Разделяем данные
X = df[['brand', 'model', 'ram', 'storage', 'screen_size']]
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создаем пайплайн
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['brand', 'model']),
        ('num', 'passthrough', ['ram', 'storage', 'screen_size'])
    ])

model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Обучаем модель
model.fit(X_train, y_train)

# Оценка модели
y_pred = model.predict(X_test)
print(f"\nMean Absolute Error: ${mean_absolute_error(y_test, y_pred):.2f}")

# Сохраняем модель
with open('laptop_price_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("\nModel successfully saved as laptop_price_model.pkl")

# Пример предсказания
sample_laptop = pd.DataFrame([{
    'brand': 'Apple',
    'model': 'MacBook Pro 16"',
    'ram': 32,
    'storage': 1024,
    'screen_size': 16.2
}])
predicted_price = model.predict(sample_laptop)
print(f"\nPredicted price for Apple MacBook Pro 16\": ${predicted_price[0]:.2f}")
