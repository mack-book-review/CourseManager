import psycopg2 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 

con = psycopg2.connect("user=postgres port=5432")

def sql_to_df(sql_query):
    return pd.read_sql_query(sql_query,con)

query1 = """
        SELECT COUNT(*) AS count,courses.name AS course_name FROM course_registrations
        LEFT JOIN courses ON course_id = courses.id
        GROUP BY courses.name
        ORDER BY Count DESC;
        """

def get_students_per_class_graph():        
    dataframe = sql_to_df(query1)
    fig,axes = plt.subplots(figsize=(10,5))
    axes.set_title("Students Enrolled Per Class",fontsize=14)

    xpos = np.arange(len(dataframe))

    axes.bar(xpos,dataframe["count"],width=0.30)
    axes.set_xticks(xpos)
    axes.set_xticklabels(dataframe["course_name"])

    axes.set_ylabel("Count",fontsize=12)
    axes.set_xlabel("Course Name",fontsize=5)

    plt.setp(axes.get_xticklabels(),rotation=90)
    plt.show()
