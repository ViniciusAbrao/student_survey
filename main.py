# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 10:10:04 2020

@author: vinic_000
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np
import statsmodels.api as sm;
from patsy import dmatrices
from statsmodels.stats.outliers_influence import variance_inflation_factor

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
plt.legend(title='')
plt.title('Which are the valuation method that most contributes to your learning?')

#question 9 
columns_list=["anyone","neither","structural/autom","thermal_fluids",
              "maintenance","machining","management","materials","not_known","another"]
question_nine=data[data.columns[40:50]]
plt.figure(figsize=[8,6])
answer_nine=question_nine.sum()
base_color = sb.color_palette()[0]
sb.barplot(columns_list,answer_nine, color= base_color)
plt.xticks(rotation=18)
plt.ylabel('count')
plt.title('What are your favorite areas in Mechanical Engineering?')

#question 10
columns_list=["neither","structural/autom","thermal_fluids",
              "machining","management","materials","math/physics"]
question_ten=data[data.columns[50:57]]
plt.figure(figsize=[8,6])
answer_ten=question_ten.sum()
sb.barplot(columns_list,answer_ten, color= base_color)
plt.xticks(rotation=18)
plt.ylabel('count')
plt.title('Which courses do you had lower performance?')

#question 12
data=data.rename(columns={60:"number_disciplines"})
answer_twelve=data[data.number_disciplines != 0]
plt.figure(figsize=[8,6])
bins=np.arange(4.5,11.5,1)
plt.hist(data=answer_twelve, x='number_disciplines', bins=bins, rwidth=0.7)
plt.xlabel('number_of_disciplines')
plt.ylabel('count')
plt.title('How many courses do you have in a semester?')

#question 11
#mark_both=data[data[data.columns[58]]+data[data.columns[57]]==2]
#mark_none=data[data[data.columns[58]]+data[data.columns[57]]==0]
def absolute_value(val):
    a  = np.round(val)
    return a
columns_list=["yes","no"]
#mark none or both yes/no
question_eleven=data.drop(['student 7', 'student 79', 'student 89']) 
plt.figure(figsize=[8,6])
plt.pie(question_eleven[58].value_counts(),labels=columns_list,startangle=90,
        autopct=absolute_value)   
plt.title('Do you have problem to manage your time for studying?')

#question 16
legend_list=["1-I feel good.",
              "2-I don't feel good, but it does not affect my studies performance.",
              "3-I don't feel good, and it does affect my studies performance.",
              "4-I need help."]
columns_list=['1','2','3','4']
question_sixteen=data[data.columns[72:76]]
plt.figure(figsize=[8,6])
answer_sixteen=question_sixteen.sum()
sb.barplot(columns_list,answer_sixteen, color= base_color)
plt.xticks(rotation=18)
plt.ylabel('count')
plt.legend(legend_list)
plt.grid(axis="y")
plt.title('How emotionally stable are you?')

#question 18
data=data.rename(columns={4:"lowPerformance"})
data=data.rename(columns={5:"dntLikeCourse"})
data=data.rename(columns={6:"time_research"})
data=data.rename(columns={7:"time_homework"})
data=data.rename(columns={8:"time_recreation"})
data=data.rename(columns={9:"dntLikeMechanics"})
data=data.rename(columns={10:"attentionInClass"})
data=data.rename(columns={11:"missMotivation"})
data=data.rename(columns={12:"healthfamily"})
data=data.rename(columns={13:"TeacherMethod"})
data=data.rename(columns={82:"thought_givingUp"})
data["intercept"]=1
problems=data[["lowPerformance","dntLikeCourse","time_research","time_homework","time_recreation",
                 "dntLikeMechanics","attentionInClass","missMotivation","healthfamily",
                 "TeacherMethod","thought_givingUp"]]
plt.figure(figsize=[8,6])
sb.heatmap(problems.corr(),annot=True)
plt.ylabel('')
plt.xlabel('')

#multiple linear regression
lm=sm.OLS(data['thought_givingUp'],data[['intercept',"lowPerformance","dntLikeCourse","time_research","time_homework","time_recreation",
                  "dntLikeMechanics","attentionInClass","missMotivation","healthfamily",
                  "TeacherMethod",]])
results=lm.fit()
print(results.summary())

#question 17
legend_list=["1-1x per week.",
              "2-2x or more per week.",
              "3-Sometimes.",
              "4-Never."]
columns_list=['1','2','3','4']
question_seventeen=data[data.columns[76:80]]
plt.figure(figsize=[8,6])
answer_seventeen=question_seventeen.sum()
sb.barplot(columns_list,answer_seventeen, color= base_color)
plt.ylabel('count')

plt.legend(legend_list)
plt.grid(axis="y")
plt.title('How often do you go parties/recreation?')

print('Have you thought about giving up?')
print(data["thought_givingUp"].sum()/n)

#pairplot
#sb.pairplot(problems)

#vif
y, X = dmatrices('thought_givingUp ~ healthfamily + lowPerformance + dntLikeCourse + time_research + \
                 time_homework + time_recreation + dntLikeMechanics + attentionInClass + \
                     missMotivation + TeacherMethod ', data, return_type = 'dataframe')

vif = pd.DataFrame()
vif["VIF Factor"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
vif["features"] = X.columns 
print(vif)