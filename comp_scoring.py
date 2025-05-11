import pandas as pd

pd.set_option('display.min_rows', 50)


def calc_comp_score(row):
    points = 0
    optional_fields = ["Additives", "Dietary preferences", "Producer Information", "Brand"]
    for index, value in row.items():
        if index in optional_fields:
            pass
        if pd.isna(value) or (isinstance(value, str) and value.strip() == ""):
            pass
        else:
            points += 1
    score = (points / (25 - len(optional_fields)) * 100)
    return score


if __name__ == "__main__":
    df = pd.read_csv('Data Processing Specialist Dataset.csv')

    df['comp_score'] = df.apply(calc_comp_score, axis=1)

    print(df)

    # Filter rows where the comp_score is 100
    df_filtered = df[df['comp_score'] == 100.0]

    # Display the filtered DataFrame
    print(df_filtered)

    df.to_csv("result.csv")
