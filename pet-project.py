import pandas as pd
import numpy as np
from pandas import Series, DataFrame

df = pd.read_csv('clean_house_prices.csv', encoding='utf-8', index_col=0)

# Функуція для визначення типу будівлі на основі року побудови
def type_buaild (building_age):
    if building_age < 5:
        return 'New building'
    elif building_age <= 25:
        return 'New housing stock'
    else:
        return 'Old housing stock'

# Видаляємо стовпець 'Id' та 'Address', оскільки вони не потрібні для аналізу
df_clear=df.drop('Id', axis=1)
df_clear=df_clear.drop('Address', axis=1)

# Змінюємо тип даних для стовпців 'build_year' та 'Price_for_m2' на цілі числа
df_clear['build_year'] = df_clear['build_year'].astype('Int64')
df_clear['Price_for_m2'] = df_clear['Price_for_m2'].astype('Int64')

#Фільтруємо дані
df_clear = df_clear[df_clear['district'] != 'Київ']

# Додаємо новий стовпець 'type_build' на основі функції type_buaild та застосовуємо фкнцію до стовпця 'building_age'
df_clear['building_age']= 2026 - df_clear['build_year']
df_clear['type_build'] = df_clear['building_age'].apply(type_buaild)

# Видаляємо аномальні значення
df_no_outliers = df_clear[
    (df_clear['Price_main'] >= 10000) & 
    (df_clear['Price_main'] <= 2000000) & 
    (df_clear['area'] >= 15)
]

# Аналізуємо дані за районами
district_stats = df_no_outliers.groupby('district').agg({
    'Price_for_m2': 'mean',
    'Price_main': 'median'
})

# Виводимо результати
print("--- 10 рядків чистого датасету ---")
print(df_no_outliers.head(10))

print("\n--- Статистика по районах ---")
print(district_stats)

# Зберігаємо очищений датасет у новий CSV файл
df_no_outliers.to_csv('final_kyiv_properties.csv', index=False, encoding='utf-8')
