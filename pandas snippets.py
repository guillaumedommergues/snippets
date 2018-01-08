# Notes on how to use the pandas library
# The online documentation is wonderful. There are plenty of great blogs and tutorials to learn
# This is meant as a cheatcheet for my colleagues as these are the most common operations in our current positions


# read an excel file
data=pd.read_excel("data.xlsx", sheetname="Sheet1") #sheet_name on more recent pandas versions

# get general info about the dataframe
print (data.info())

# convert the type of a column
data['Fare'] = data['Fare'].astype(int)

# normalizing variables
features_to_normalize = ['Distance', 'Duration', 'Fare']
# Store scalings in a dictionary so we can convert back later
scaled_features = {}
for each in features_to_normalize:
    mean, std = data[each].mean(), data[each].std()
    scaled_features[each] = [mean, std]
    data.loc[:, each] = (data[each] - mean)/std

# aggregate variables
nsf=nsf.groupby(by=["Distance","Duration"]).agg({"Fare":"sum"})
nsf=nsf.reset_index()

# Split off random 10% of the data for testing
np.random.seed(21)
sample = np.random.choice(data.index, size=int(len(data)*0.9), replace=False)
data, test_data = data.ix[sample], data.drop(sample)

# Split into features and targets
features, targets = data.drop('Target', axis=1), data['Target']
features_test, targets_test = test_data.drop('Target', axis=1), test_data['Target']

# export data to excel
data.to_excel("data.xlsx") 

# export several dataframes df1,df2,df3 to several worksheets
from pandas import ExcelWriter
def save_xls(list_dfs,names, xls_path):
    writer = ExcelWriter(xls_path)
    for n, df in enumerate(list_dfs):
        df.to_excel(writer,names[n])
    writer.save()
list_dfs=[df1,df2,df3]
names=['df1','df2','df3']
xls_path="data.xlsx"
save_xls(list_dfs, xls_path) 



