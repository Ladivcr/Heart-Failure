import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt 

@st.cache(persist=True)
def load_data():
    data = pd.read_csv('heart_failure_clinical_records_dataset.csv')
    
    return data


#@st.cache(persist=True)
def plot_sentiment(choise):
    count = n_data[choise].value_counts()
    #count = df['airline_sentiment'].value_counts()
    count = pd.DataFrame({'Sentiment':count.index, 'Tweets':count.values.flatten()})
    return count


#DATA_URL = ('heart_failure_clinical_records_dataset.csv')

data=load_data()

st.sidebar.header('Heart Failure')
st.subheader('Datos a utilizar')
st.sidebar.subheader('Filtros')

start_a,end_a = st.sidebar.select_slider('Edad a filtrar:',options=sorted(list(data['age'])),value=(min(data['age']),max(data['age'])))

st.title("Heart Failure")

n_data=data[(data['age']>=start_a)&(data['age']<=end_a)]
#print(min(data['age']))
#print(max(data['age']))


left_col, right_col =st.sidebar.beta_columns(2)

with left_col:
    b_left = st.checkbox("Muerto", True)

with right_col:
    b_right = st.checkbox("Vivo", True)


###################GRAFICAS
if not (b_left | b_right):
    n_data=n_data[n_data['sex']==300]
else:
    n_data=n_data[((n_data['DEATH_EVENT']==1)==b_left) | ((n_data['DEATH_EVENT']==0)==b_right)]

st.write(n_data)

st.sidebar.subheader('Visualizacion')

#select = st.sidebar.selectbox('Visualization type', ['Bar plot', 'Pie chart'], key='1')

#st.sidebar.write('Death_event vs:')

choice = st.sidebar.multiselect('Death_event vs:', tuple(data.drop('DEATH_EVENT',axis=1).columns),['age','ejection_fraction','serum_creatinine','time'])
st.subheader("Death_event VS")
breakdown_type = st.sidebar.selectbox('Visualization type', ['Pie chart', 'Bar plot', ], key='3')

if len(n_data)>0:
    if len(choice) > 0:
        cor=n_data[choice]
        cor['DEATH_EVENT']=data['DEATH_EVENT']
        R=cor.corr()
        fig_c=plt.figure()
        sns.heatmap(R,annot=True)
        st.pyplot(fig_c)

        fig_3 = make_subplots(rows=1, cols=len(choice), subplot_titles=choice)
        if breakdown_type == 'Bar plot':
            for i in range(1):
                for j in range(len(choice)):
                    fig_3.add_trace(
                        go.Bar(x=plot_sentiment(choice[j]).Sentiment, y=plot_sentiment(choice[j]).Tweets, showlegend=False),
                        row=i+1, col=j+1
                    )
            fig_3.update_layout(height=600, width=800)
            st.plotly_chart(fig_3)
        else:
            fig_3 = make_subplots(rows=1, cols=len(choice), specs=[[{'type':'domain'}]*len(choice)], subplot_titles=choice)
            for i in range(1):
                for j in range(len(choice)):
                    fig_3.add_trace(
                        go.Pie(labels=plot_sentiment(choice[j]).Sentiment, values=plot_sentiment(choice[j]).Tweets, showlegend=True),
                        i+1, j+1
                    )
            fig_3.update_layout(height=600, width=800)
            st.plotly_chart(fig_3)

else:
    st.write('Datos insuficientes')

#################Matriz correlacion


#st.subheader('Matriz de correlacion')

#if len(n_data)>0:
#    eval = n_data[['age','ejection_fraction','serum_creatinine','time', 'DEATH_EVENT']]

#    R_eval=eval.corr()
#    sns.heatmap(R_eval, annot = True)
    #cor=plt.figure()
#    st.pyplot()    




##################kmeans :D
st.subheader('K-means')
st.sidebar.subheader('K-means')
st.write('Para calcular k-means utilizamos las columnas age,ejection_fraction,serum_creatinine y time'
)
st.write('Los mejores resultados se obtienen con K=5')
k = st.sidebar.slider('K:',1,10,5)


if len(n_data)>0:
    eval = n_data[['age','ejection_fraction','serum_creatinine','time', 'DEATH_EVENT']]


    result = KMeans(n_clusters=k,init='random',max_iter=200).fit(eval.drop('DEATH_EVENT',axis=1))

    cluster_result = list(result.labels_)
    eval = eval.assign(Cluster_group = cluster_result)

    #graficamos las 3 dimensiones mas importantes

    X = np.array(eval[['ejection_fraction','serum_creatinine','time']])

    labels=np.array(eval['Cluster_group'])
    plt.style.use('classic')

    y = np.array(eval['DEATH_EVENT'])

    fig_k = plt.figure()
    ax=Axes3D(fig_k)
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=labels,s=60)

    #st.plotly_chart(ax)
    st.pyplot(fig_k)

else:
    st.write('Datos insuficientes')
