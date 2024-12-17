import pandas as pd
ethnicity_map = {
 '/m/0dryh9k': 'Indian',
 '/m/0x67': 'Black',
 '/m/041rx': 'Jewish',
 '/m/02w7gg': 'English',
 '/m/033tf_': 'Irish_Americans',
 '/m/0xnvg': 'Italian_Americans',
 '/m/02ctzb': 'White_people',
 '/m/07hwkr': 'White_Americans',
 '/m/07bch9': 'Scottish_Americans',
 '/m/03bkbh': 'Irish_people',
 '/m/0d7wh': 'British',
 '/m/03ts0c': 'French',
 '/m/0222qb': 'Italians',
 '/m/01rv7x': 'Tamil'
}
# Takes as input a dataframe, which contains a column 'actor_ethnicity'. Returns a dataframe where the values in it have been
# mapped to the map seen above. If no match in map, return "other"
# If passed with one_hot = True, also one-hot
def decode_ethnicity(df, one_hot = True):
    df['actor_ethnicity'] = df['actor_ethnicity'].map(ethnicity_map).fillna("Other")
    df = pd.get_dummies(df, columns=['actor_ethnicity'], drop_first=True)
    return df