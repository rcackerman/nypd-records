import pandas as pd
from documentcloud import DocumentCloud

COPS = pd.read_csv('nypd-discipline.csv')

COPS['Name'] = COPS['NameNo'].str.extract('([^/]*) /', expand=False)
COPS['DocID'] = COPS['URL'].str.extract('documents/([0-9]*)-', expand=False)
COPS['LastName'] = COPS['Name'].str.extract('[a-zA-Z]+ (.+)$', expand=False)
COPS['FirstName'] = COPS['Name'].str.extract('([a-zA-Z]+) .+', expand=False)

# Those two outliers
COPS.loc[COPS['LastName'].str.startswith('LEAH ', na=False), 'FirstName'] = COPS.apply(
        lambda row: '{} LEAH'.format(row['FirstName']), axis=1)
COPS['LastName'] = COPS['LastName'].str.replace('LEAH ', '')
COPS.loc[pd.isnull(COPS['LastName']), 'LastName'] = COPS['Name']
        
COPS['FileName'] = COPS.apply(
        lambda row: '{last}-{first}-{caseno}.pdf'.format(last=row['LastName'],
                                                         first=row['FirstName'],
                                                         caseno=row['Case']), axis=1)
