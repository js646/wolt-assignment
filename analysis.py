import pandas as pd
import re

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 5)
pd.set_option('display.width', 1280)

if __name__ == "__main__":
    df = pd.read_csv('Data Processing Specialist Dataset.csv')

    def extract_allergens(entry):
        if pd.isna(entry) or entry.strip() == "":
            return []
        entry = entry.lower()
        entry = re.sub(r"[.]", "", entry)
        entry = "" if entry == "-" else entry
        parts = re.split(r",", entry)
        return [p.strip() for p in parts if p.strip()]

    df['Allergen_List'] = df['Allergens '].apply(extract_allergens)

    exploded = df.explode('Allergen_List')

    allergen_groups = exploded.groupby('Allergen_List').agg({
        'Name ': lambda x: list(pd.Series(x).dropna().unique()),  # Liste der Produktnamen
    })

    total_products = df['Name '].count()

    allergen_groups['Count'] = allergen_groups['Name '].apply(len)
    allergen_groups['% Share'] = (allergen_groups['Count'] / total_products * 100).round(1)

    allergen_groups = allergen_groups.reset_index().rename(
        columns={'Allergen_List': 'Allergen', 'Name ': 'Products'}).sort_values(by='Count', ascending=False)

    print(allergen_groups)
