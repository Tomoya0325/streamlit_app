import streamlit as st
import pandas as pd
import plotly.express as px
import time

with st.spinner("読み込み中..."):
    time.sleep(2)

st.success('読み込みに成功しました')
st.button('再読み込み')

st.divider()
st.title('学校に関するデータ')
st.divider()

st.subheader('概要')
st.write('このアプリはe-Statから得られた学校基本調査を利用し、学校種別ごとの学生数や学校数の推移、設置区分別の比較を可視化するためのものです。')
st.divider()

st.subheader('目的')
st.write('主に学校数や学生数の変化、設置区分での学生数の差を表とグラフの両方で把握することを目的としています。')
st.divider()

st.subheader('使い方')
st.write('最初はサイドバーの項目がすべて選択された状態から始まります。絞り込みたい場合は選択を外してください。そして、中央にあるタブの「表」を押すと「年度別」「設置区分別」の表を見ることができ、「グラフ」を押すと、「学生数推移」「学校数推移」「設置区分比較」のグラフを見ることができます。')
st.divider()

st.subheader('注意点')
st.write('複数選択をすべて外してしまうとエラーが起きるので注意してください。')
st.divider()

st.subheader('データの確認')
st.write('学校基本調査は、全国の学校を対象に学校数や在学者数などを毎年調査し、教育行政や将来の教育計画に活用される基礎資料を提供する統計調査です。')

df1 = pd.read_csv('hi0001_2025.csv')
df2 = pd.read_csv('hi0001_2025_2.csv')

with st.sidebar:
    school = st.selectbox('学校種を1つ選択してください',
                         df1['学校種'].unique())
    st.divider()
    years = st.multiselect('年度を選択してください（複数選択可）',
                           df1['年度'].unique(),
                           default=df1['年度'].unique())
    st.divider()
    category = st.multiselect('設置区分を選択してください（複数選択可）',
                             df2['設置区分'].unique(),
                             default=df2['設置区分'].unique())

df_year = df1[df1['学校種'] == school]

if years:
    df_year = df_year[df_year['年度'].isin(years)]
    df_category = df2[df2['学校種'] == school]
if category:
    df_category = df_category[df_category['設置区分'].isin(category)]

tab_table, tab_graph = st.tabs(['表', 'グラフ'])

with tab_table:
    table_type_year, table_type_category = st.tabs(['年度別', '設置区分別'])
    
    with table_type_year:
        st.dataframe(df_year)
    with table_type_category:
        st.dataframe(df_category)

with tab_graph:
    g_tab1, g_tab2, g_tab3 = st.tabs(['学生数推移', '学校数推移', '設置区分比較'])
    
    with g_tab1:
        fig1 = px.line(df_year, x='年度',
                       y='学生数(単位:人)',
                       markers=True,
                       title='年度ごとの学生数の推移'
                       
                       )
        st.plotly_chart(fig1)
        st.write('年々学生数は増加していることがグラフから読み取れます。')

    with g_tab2:
        fig2 = px.line(df_year,
                       x='年度',
                       y='学校数(単位:校)',
                       markers=True,
                       title='年度ごとの学校数の推移'
                       )
        st.plotly_chart(fig2)
        st.write('ここ数年で学校数は1年で約3校ずつ増加し続けていたが、令和7年になると令和6年から1校減少したことが読み取れる。')

    with g_tab3:
        fig3 = px.bar(df_category,
                      x='設置区分',
                      y='学生数(単位:人)',
                      title='設置区分別の人数比較'
                      )
        st.plotly_chart(fig3)
        st.write('学生数は私立がダントツで多く、その次に国立、公立となっていることが読み取れる。')