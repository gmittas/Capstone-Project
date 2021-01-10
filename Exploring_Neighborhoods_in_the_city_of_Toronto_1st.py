#!/usr/bin/env python
# coding: utf-8

# <h1 align=center><font size = 5>Segmenting and Clustering Neighborhoods in Toronto_Part 1</font></h1>

# ## Problem 1
# 
# Use the Notebook to build the code to scrape the following Wikipedia page, https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M, in order to obtain the data that is in the table of postal codes and to transform the data into a pandas dataframe.
# 
# To create the above dataframe:
# 
# - The dataframe will consist of three columns: PostalCode, Borough, and Neighborhood
# - Only process the cells that have an assigned borough. Ignore cells with a borough that is Not assigned.
# - More than one neighborhood can exist in one postal code area. For example, in the table on the Wikipedia page, you will notice that - M5A is listed twice and has two neighborhoods: Harbourfront and Regent Park. These two rows will be combined into one row with the - neighborhoods separated with a comma as shown in row 11 in the above table.
# - If a cell has a borough but a Not assigned neighborhood, then the neighborhood will be the same as the borough. So for the 9th cell in the table on the Wikipedia page, the value of the Borough and the Neighborhood columns will be Queen's Park.
# - Clean your Notebook and add Markdown cells to explain your work and any assumptions you are making.
# - In the last cell of your notebook, use the .shape method to print the number of rows of your dataframe.

# In[1]:


from bs4 import BeautifulSoup
import requests
import pandas as pd


# ###### Scrape the List of postal codes of Canada

# In[2]:


List_url = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M"
source = requests.get(List_url).text


# In[3]:


soup = BeautifulSoup(source, 'xml')


# In[4]:


table=soup.find('table')


# In[5]:


#dataframe will consist of three columns: PostalCode, Borough, and Neighborhood
column_names = ['Postalcode','Borough','Neighborhood']
df = pd.DataFrame(columns = column_names)


# In[6]:


# Search all the postcode, borough, neighborhood 
for tr_cell in table.find_all('tr'):
    row_data=[]
    for td_cell in tr_cell.find_all('td'):
        row_data.append(td_cell.text.strip())
    if len(row_data)==3:
        df.loc[len(df)] = row_data


# In[7]:


df.head()


# ###### Data Cleaning
# remove rows where Borough is 'Not assigned'

# In[9]:


df=df[df['Borough']!='Not assigned']


# In[11]:


df[df['Neighborhood']=='Not assigned']=df['Borough']
df.head()


# In[13]:


temp_df=df.groupby('Postalcode')['Neighborhood'].apply(lambda x: "%s" % ', '.join(x))
temp_df=temp_df.reset_index(drop=False)
temp_df.rename(columns={'Neighborhood':'Neighborhood_joined'},inplace=True)


# In[14]:


df_merge = pd.merge(df, temp_df, on='Postalcode')


# In[16]:


df_merge.drop(['Neighborhood'],axis=1,inplace=True)


# In[17]:


df_merge.drop_duplicates(inplace=True)


# In[18]:


df_merge.rename(columns={'Neighborhood_joined':'Neighborhood'},inplace=True)


# In[19]:


df_merge.head()


# In[20]:


df_merge.shape


# In[ ]:




