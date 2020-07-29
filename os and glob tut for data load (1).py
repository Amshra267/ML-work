#!/usr/bin/env python
# coding: utf-8

# In[18]:


# loading  modules
import os
import glob
import numpy as np


# In[2]:


# getting current directory of working
os.getcwd()


# In[4]:


# can list all the items using os.listdir() command
os.listdir()


# In[13]:


# we can use glob to files of the same pattern using UNIX type rules


print('#no1.\n')
# putting complete path returns that path

files1 = glob.glob('submission1.csv')

for file in files1:
    print(file)

print('\nend #no1.\n')    
print('start #no2.\n')
#using * operation this will return all files or folders in current directory

files2 = glob.glob('*')

for file in files2:
    print(file)
    
print('\nend #no2.\n')    
print('start #no3.\n')
# using *[0-9] returns range of files with this paths in 0-9 digits

files3 = glob.glob('*[0-9].*')

for file in files3:
    print(file)
    
print('\n end #no3.\n')    
    


# In[14]:


# recursive method can also be used to find subdirectories

# Returns a list of names in list files. 
print("Using glob.glob()") 
files4 = glob.glob('**/*.*',  
                   recursive = True) 
for file in files4: 
    print(file) 
  


# In[25]:


# printing the no.of file with extension
for i,file in enumerate(files1):
    print('{}:{}'.format(i,file))
    
    # using os.path.basename to extract name of file
    name = os.path.basename(file)  
    print(name)
    
    # now apply os.path.splittext to split name and extension
    split = os.path.splitext(name)[0]
    print(split)
    # printing individual letter
    for letter in split:
        print(letter)


# In[ ]:





# In[ ]:




