import pandas as pd
# from documentcloud import DocumentCloud

# DC_CLIENT = DocumentCloud()

def download_doc(row, client):
    case_pdf = client.documents.get(row['DocID']).pdf
    with open(row['FileName'], 'wb') as outfile:
        outfile.write(case_pdf)


cops = pd.read_csv('nypd-discipline.csv')

cops['Name'] = cops['NameNo'].str.extract('([^/]*) /', expand=False)
cops['DocID'] = cops['URL'].str.extract('documents/([0-9]*)-', expand=False)
cops['LastName'] = cops['Name'].str.extract('[a-zA-Z]+ (.+)$', expand=False)
cops['FirstName'] = cops['Name'].str.extract('([a-zA-Z]+) .+', expand=False)

# Those two outliers
cops.loc[cops['LastName'].str.startswith('LEAH ', na=False), 'FirstName'] = cops.apply(
        lambda row: '{} LEAH'.format(row['FirstName']), axis=1)
cops['LastName'] = cops['LastName'].str.replace('LEAH ', '')
cops.loc[pd.isnull(cops['LastName']), 'LastName'] = cops['Name']
        
cops['FileName'] = cops.apply(
        lambda row: '{last}-{first}-{caseno}.pdf'.format(last=row['LastName'],
                                                         first=row['FirstName'],
                                                         caseno=row['Case']), axis=1)
cops['FileName'] = cops['FileName'].str.replace(r'[/\\]', '-')
cops['FileName'] = cops['FileName'].str.replace('__', '_')

cops.to_csv('cleaned-nypd-discipline.csv', index=False)

# for idx, row in cops.iterrows():
    # download_doc(row, DC_CLIENT)

nycds_cases = pd.read_csv('all-cases-2-years.csv')
nycds_cases = nycds_cases.loc[~pd.isnull(nycds_cases['Arrest Officer'])]

pat = r"(?P<last>.*), (?P<first>.*)"
repl = lambda m: "{} {}".format(m.group('first'), m.group('last'))
nycds_cases['arrest_officer'] = nycds_cases['Arrest Officer'].str.replace(pat, repl)

nycds_cases.to_csv('formatted-nycds-cases.csv', index=False)

