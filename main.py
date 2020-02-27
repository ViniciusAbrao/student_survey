# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 10:10:04 2020

@author: vinic_000
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

data=pd.read_csv('data.csv')
data=data.fillna(0)
data=data.rename(columns={"question":"student"})
data=data.set_index('student')
data=data.T
print(data.head())

#question 6 
data=data.rename(columns={24:"theory_test"})
data=data.rename(columns={25:"practice_test"})
data=data.rename(columns={26:"individual_project"})
data=data.rename(columns={27:"project_in_group"})
data=data.rename(columns={28:"homework"})
data=data.rename(columns={29:"classroom_workgroups"})
columns_list=["theory_test","practice_test","individual_project","project_in_group",
              "homework","classroom_workgroups"]
answer_list=["worst_method","unfavorable", "minor_contribution","favorable",
             "major_contribution","best_method"]
n=data["theory_test"].size
question_six=[]
answer_six=[]
for column in columns_list:
    for i in range(n):
        question_six.append(column)
        answer_six.append(data[column][i])  
df = pd.DataFrame(list(zip(question_six,answer_six)),columns=['question_six','answer_six']) 
df = df[df.answer_six != 0]
plt.figure(figsize=[8,6])
ax=sb.countplot(x='answer_six',hue='question_six',data=df)
plt.xticks(range(7),answer_list,rotation=15)
plt.xlabel('')

#question 9 
columns_list=["anyone","neither","structural/autom","thermal_fluids",
              "maintenance","machining","management","materials","not_known","another"]
question_nine=data[data.columns[40:50]]
plt.figure(figsize=[8,6])
answer_nine=question_nine.sum()
base_color = sb.color_palette()[0]
sb.barplot(columns_list,answer_nine, color= base_color)
plt.xticks(rotation=18)

#question 10
columns_list=["neither","structural/autom","thermal_fluids",
              "machining","management","materials","math/physics"]
question_ten=data[data.columns[50:57]]
plt.figure(figsize=[8,6])
answer_ten=question_ten.sum()
sb.barplot(columns_list,answer_ten, color= base_color)
plt.xticks(rotation=18)

#question 12
data=data.rename(columns={60:"number_disciplines"})
answer_twelve=data[data.number_disciplines != 0]
plt.figure(figsize=[8,6])
plt.hist(data=answer_twelve, x='number_disciplines')
plt.xticks(rotation=18)