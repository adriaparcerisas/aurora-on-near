#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import pandas as pd
import numpy as np
from shroomdk import ShroomDK
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.ticker as ticker
import numpy as np
import plotly.express as px
sdk = ShroomDK("7bfe27b2-e726-4d8d-b519-03abc6447728")
st.cache(suppress_st_warning=True)


# In[19]:


st.title('Aurora Near illumination')


# In[20]:


st.markdown('Aurora is a solution for executing Ethereum smart contracts on the Near blockchain. We can think like an EVM for Near Protocol, which allows Near to interact with Ethereum smart contracts, it is to say, like a Layer-2 platform.')



# In[5]:


st.markdown('Because of during the past months, the Ethereum Layer-2 platforms such as Optimism, Arbitrum and Polygon expeerimented a huge growth, the intention of this analysis is to provide information about the current status of Aurora inside the Near Protocol network in terms of activity by providing metrics such as:')
st.write('- New users')
st.write('- Active users')
st.write('- Executed transactions')
st.write('- Generated fees')
st.write('- Gas used')
st.write('- New contracts')
st.write('- Active contracts')
st.write('')


# In[10]:


sql = f"""
with
  t1 as (
  select
  distinct tx_signer,
  min(block_timestamp) as debut
from near.core.fact_transactions
where tx_status = 'Success' and tx_receiver='aurora'
group by 1
  ),
  t2 as (
  SELECT
  distinct tx_signer,debut from t1 where debut >=CURRENT_DATE-INTERVAL '1 WEEK'
  )
  select
  trunc(debut,'hour') as date,
  count(distinct tx_signer) as new_users,
  sum(new_users) over (order by date) as cum_new_users
  from t2
  group by 1
order by 1 asc
"""

sql2 = f"""
with
  t1 as (
  select
  distinct tx_signer,
  min(block_timestamp) as debut
from near.core.fact_transactions
where tx_status = 'Success' and tx_receiver='aurora'
group by 1
  ),
  t2 as (
  SELECT
  distinct tx_signer,debut from t1 where debut >=CURRENT_DATE-INTERVAL '2 WEEKS'
  )
  select
  trunc(debut,'day') as date,
  count(distinct tx_signer) as new_users,
  sum(new_users) over (order by date) as cum_new_users
  from t2
  group by 1
order by 1 asc
"""

sql3 = f"""
with
  t1 as (
  select
  distinct tx_signer,
  min(block_timestamp) as debut
from near.core.fact_transactions
where tx_status = 'Success' and tx_receiver='aurora'
group by 1
  ),
  t2 as (
  SELECT
  distinct tx_signer,debut from t1 where debut >=CURRENT_DATE-INTERVAL '3 MONTHS'
  )
  select
  trunc(debut,'week') as date,
  count(distinct tx_signer) as new_users,
  sum(new_users) over (order by date) as cum_new_users
  from t2
  group by 1
order by 1 asc
"""

sql4="""
SELECT
*,
ROUND((active_users - active_users_prev)/active_users_prev * 100,2) AS pct_diff_active,
ROUND((number_transactions - number_transactions_prev)/number_transactions_prev * 100,2) AS pct_diff_transactions,
ROUND((txn_fees - txn_fees_prev)/txn_fees_prev * 100,2) AS pct_diff_txn_fees
FROM
(
SELECT
*,
LAG(active_users,1) OVER (ORDER BY date) active_users_prev,
LAG(number_transactions,1) OVER (ORDER BY date) number_transactions_prev,
LAG(txn_fees) OVER (ORDER BY date) txn_fees_prev
FROM
(
SELECT
  tr.*
  FROM
  	(
    SELECT
    DATE_TRUNC('hour',block_timestamp::date) AS date,
    DATE_TRUNC('hour', block_timestamp::date - 1) AS date_prev,
    COUNT(DISTINCT TX_SIGNER) AS active_users,
    sum(active_users) over (order by date) as cum_active_users,
    COUNT(DISTINCT TX_HASH) AS number_transactions,
    SUM(TRANSACTION_FEE/POW(10,24)) AS txn_fees
    FROM near.core.fact_transactions AS tr
  	WHERE date < CURRENT_DATE and block_timestamp::date>=CURRENT_DATE-INTERVAL '1 WEEK' and tx_receiver='aurora.pool.near'
    GROUP BY date, date_prev
	) AS tr
)
)
ORDER BY date DESC
"""

sql5="""
SELECT
*,
ROUND((active_users - active_users_prev)/active_users_prev * 100,2) AS pct_diff_active,
ROUND((number_transactions - number_transactions_prev)/number_transactions_prev * 100,2) AS pct_diff_transactions,
ROUND((txn_fees - txn_fees_prev)/txn_fees_prev * 100,2) AS pct_diff_txn_fees
FROM
(
SELECT
*,
LAG(active_users,1) OVER (ORDER BY date) active_users_prev,
LAG(number_transactions,1) OVER (ORDER BY date) number_transactions_prev,
LAG(txn_fees) OVER (ORDER BY date) txn_fees_prev
FROM
(
SELECT
  tr.*
  FROM
  	(
    SELECT
    DATE_TRUNC('day',block_timestamp::date) AS date,
    DATE_TRUNC('day', block_timestamp::date - 1) AS date_prev,
    COUNT(DISTINCT TX_SIGNER) AS active_users,
    sum(active_users) over (order by date) as cum_active_users,
    COUNT(DISTINCT TX_HASH) AS number_transactions,
    SUM(TRANSACTION_FEE/POW(10,24)) AS txn_fees
    FROM near.core.fact_transactions AS tr
  	WHERE date < CURRENT_DATE and block_timestamp::date>=CURRENT_DATE-INTERVAL '2 WEEKS' and tx_receiver='aurora.pool.near'
    GROUP BY date, date_prev
	) AS tr
)
)
ORDER BY date DESC
"""

sql6="""
SELECT
*,
ROUND((active_users - active_users_prev)/active_users_prev * 100,2) AS pct_diff_active,
ROUND((number_transactions - number_transactions_prev)/number_transactions_prev * 100,2) AS pct_diff_transactions,
ROUND((txn_fees - txn_fees_prev)/txn_fees_prev * 100,2) AS pct_diff_txn_fees
FROM
(
SELECT
*,
LAG(active_users,1) OVER (ORDER BY date) active_users_prev,
LAG(number_transactions,1) OVER (ORDER BY date) number_transactions_prev,
LAG(txn_fees) OVER (ORDER BY date) txn_fees_prev
FROM
(
SELECT
  tr.*
  FROM
  	(
    SELECT
    DATE_TRUNC('week',block_timestamp::date) AS date,
    DATE_TRUNC('week', block_timestamp::date - 1) AS date_prev,
    COUNT(DISTINCT TX_SIGNER) AS active_users,
    sum(active_users) over (order by date) as cum_active_users,
    COUNT(DISTINCT TX_HASH) AS number_transactions,
    SUM(TRANSACTION_FEE/POW(10,24)) AS txn_fees
    FROM near.core.fact_transactions AS tr
  	WHERE date < CURRENT_DATE and block_timestamp::date>=CURRENT_DATE-INTERVAL '3 MONTHS' and tx_receiver='aurora.pool.near'
    GROUP BY date, date_prev
	) AS tr
)
)
ORDER BY date DESC
"""

# In[11]:


st.experimental_memo(ttl=1000000)
@st.cache
def compute(a):
    results=sdk.query(a)
    return results

results = compute(sql)
df = pd.DataFrame(results.records)
df.info()

results2 = compute(sql2)
df2 = pd.DataFrame(results2.records)
df2.info()

results3 = compute(sql3)
df3 = pd.DataFrame(results3.records)
df3.info()

results4 = compute(sql4)
df4 = pd.DataFrame(results4.records)
df4.info()

results5 = compute(sql5)
df5 = pd.DataFrame(results5.records)
df5.info()

results6 = compute(sql6)
df6 = pd.DataFrame(results6.records)
df6.info()

# In[22]:

st.subheader('New and active Aurora users')
st.write('The most important metric for transparency is the activity on the network in terms of users usage. So, the first metric to be analyzed are the new and active users over the past weeks on Near.')
st.write('In concrete, the following charts shows:')
st.write('- Last week new users (hourly and cumulative)')
st.write('- Last 2 weeks new users (daily and cumulative)')
st.write('- Last 3 months new users (weekly and cumulative)')
st.write('')

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['new_users'],
                name='# of users',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['cum_new_users'],
                name='# of users',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig1.update_layout(
    title='New Aurora users',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Hourly new Aurora users", secondary_y=False)
fig1.update_yaxes(title_text="Total new Aurora users", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df2['date'],
                y=df2['new_users'],
                name='# of users',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df2['date'],
                y=df2['cum_new_users'],
                name='# of users',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig2.update_layout(
    title='New Aurora users',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Daily new Aurora users", secondary_y=False)
fig2.update_yaxes(title_text="Total new Aurora users", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])
fig3.add_trace(go.Bar(x=df3['date'],
                y=df3['new_users'],
                name='# of users',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df3['date'],
                y=df3['cum_new_users'],
                name='# of users',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig3.update_layout(
    title='New Aurora users',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Weekly new Aurora users", secondary_y=False)
fig3.update_yaxes(title_text="Total new Aurora users", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Hourly new users", "Daily new users", "Weekly new users"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# Create figure with secondary y-axis
fig4 = make_subplots(specs=[[{"secondary_y": True}]])

fig4.add_trace(go.Bar(x=df4['date'],
                y=df4['active_users'],
                name='# of users',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig4.add_trace(go.Line(x=df4['date'],
                y=df4['cum_active_users'],
                name='# of users',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig4.update_layout(
    title='Active Aurora users',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig4.update_yaxes(title_text="Hourly active Aurora users", secondary_y=False)
fig4.update_yaxes(title_text="Total active Aurora users", secondary_y=True)

# Create figure with secondary y-axis
fig5 = make_subplots(specs=[[{"secondary_y": True}]])

fig5.add_trace(go.Bar(x=df5['date'],
                y=df5['active_users'],
                name='# of users',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig5.add_trace(go.Line(x=df5['date'],
                y=df5['cum_active_users'],
                name='# of users',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig5.update_layout(
    title='Active Aurora users',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig5.update_yaxes(title_text="Daily active Aurora users", secondary_y=False)
fig5.update_yaxes(title_text="Total active Aurora users", secondary_y=True)


# Create figure with secondary y-axis
fig6 = make_subplots(specs=[[{"secondary_y": True}]])

fig6.add_trace(go.Bar(x=df6['date'],
                y=df6['active_users'],
                name='# of users',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig6.add_trace(go.Line(x=df6['date'],
                y=df6['cum_active_users'],
                name='# of users',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig6.update_layout(
    title='Active Aurora users',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig6.update_yaxes(title_text="Weekly active Aurora users", secondary_y=False)
fig6.update_yaxes(title_text="Total active Aurora users", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Hourly active users", "Daily active users", "Weekly active users"])

with tab1:
    st.plotly_chart(fig4, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig5, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig6, theme="streamlit", use_container_width=True)



sql="""
Select
  trunc(block_timestamp,'hour') as date,
  count(distinct tx_hash) as txs,
  sum(txs) over (order by date) as cum_txs
  From near.core.fact_transactions
  Where block_timestamp::date >=current_date - INTERVAL '1 WEEK' and tx_receiver='aurora'
  Group by 1
order by 1 ASC
"""

sql2="""
Select
  trunc(block_timestamp,'day') as date,
  count(distinct tx_hash) as txs,
  sum(txs) over (order by date) as cum_txs
  From near.core.fact_transactions
  Where block_timestamp::date >=current_date - INTERVAL '2 WEEKS' and tx_receiver='aurora'
  Group by 1
order by 1 ASC
"""

sql3="""
Select
  trunc(block_timestamp,'week') as date,
  count(distinct tx_hash) as txs,
  sum(txs) over (order by date) as cum_txs
  From near.core.fact_transactions
  Where block_timestamp::date >=current_date - INTERVAL '3 MONTHS' and tx_receiver='aurora'
  Group by 1
order by 1 ASC
"""

sql4="""
WITH
    near as (
Select
  trunc(block_timestamp,'hour') as date,
  count(distinct tx_hash) as txs,
  txs/1440 as tpm
  From near.core.fact_transactions
  Where block_timestamp::date >=current_date - INTERVAL '1 WEEK' and tx_receiver='aurora'
  Group by 1
order by 1 ASC
  ),
  near_fail as (
  Select
  trunc(block_timestamp,'hour') as date,
  count(distinct tx_hash) as failed_txs
  From near.core.fact_transactions
  Where block_timestamp::date >=CURRENT_DATE - INTERVAL '1 WEEK' and tx_receiver='aurora'
  and tx_status<>'Success'
  Group by date
order by date ASC
  )
  SELECT
  x.date,
  txs,
  failed_txs,
  txs-failed_txs as succeeded_txs,
  (failed_txs/txs)*100 as pcg_failed,
  (succeeded_txs/txs)*100 as pcg_succeeded
  from near x, near_fail y where x.date=y.date
"""

sql5="""
WITH
    near as (
Select
  trunc(block_timestamp,'day') as date,
  count(distinct tx_hash) as txs,
  txs/1440 as tpm
  From near.core.fact_transactions
  Where block_timestamp::date >=current_date - INTERVAL '2 WEEKS' and tx_receiver='aurora'
  Group by 1
order by 1 ASC
  ),
  near_fail as (
  Select
  trunc(block_timestamp,'day') as date,
  count(distinct tx_hash) as failed_txs
  From near.core.fact_transactions
  Where block_timestamp::date >=CURRENT_DATE - INTERVAL '2 WEEKS'  and tx_receiver='aurora'
  and tx_status<>'Success'
  Group by date
order by date ASC
  )
  SELECT
  x.date,
  txs,
  failed_txs,
  txs-failed_txs as succeeded_txs,
  (failed_txs/txs)*100 as pcg_failed,
  (succeeded_txs/txs)*100 as pcg_succeeded
  from near x, near_fail y where x.date=y.date
"""

sql6="""
WITH
    near as (
Select
  trunc(block_timestamp,'week') as date,
  count(distinct tx_hash) as txs,
  txs/1440 as tpm
  From near.core.fact_transactions
  Where block_timestamp::date >=current_date - INTERVAL '3 MONTHS' and tx_receiver='aurora'
  Group by 1
order by 1 ASC
  ),
  near_fail as (
  Select
  trunc(block_timestamp,'week') as date,
  count(distinct tx_hash) as failed_txs
  From near.core.fact_transactions
  Where block_timestamp::date >=CURRENT_DATE - INTERVAL '3 MONTHS'  and tx_receiver='aurora'
  and tx_status<>'Success'
  Group by date
order by date ASC
  )
  SELECT
  x.date,
  txs,
  failed_txs,
  txs-failed_txs as succeeded_txs,
  (failed_txs/txs)*100 as pcg_failed,
  (succeeded_txs/txs)*100 as pcg_succeeded
  from near x, near_fail y where x.date=y.date
"""



st.experimental_memo(ttl=1000000)
@st.cache
def compute2(a):
    results=sdk.query(a)
    return results

results = compute2(sql)
df = pd.DataFrame(results.records)
df.info()

results2 = compute2(sql2)
df2 = pd.DataFrame(results2.records)
df2.info()

results3 = compute2(sql3)
df3 = pd.DataFrame(results3.records)
df3.info()

results4 = compute2(sql4)
df4 = pd.DataFrame(results4.records)
df4.info()

results5 = compute2(sql5)
df5 = pd.DataFrame(results5.records)
df5.info()

results6 = compute2(sql6)
df6 = pd.DataFrame(results6.records)
df6.info()

# In[22]:

st.subheader('Executed Aurora transactions')
st.write('One of the useful metrics to see if the network is healthy used is the amount of transactions being carried out by users. So, the next metric we are gonna analyze is the number of transactions being executed on Near.')
st.write('In concrete, the following charts shows:')
st.write('- Last week transactions (hourly and cumulative)')
st.write('- Last 2 weeks transactions (daily and cumulative)')
st.write('- Last 3 months transactions (weekly and cumulative)')
st.write('')

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['txs'],
                name='# of transactions',
                marker_color='rgb(153, 250, 185)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['cum_txs'],
                name='# of transactions',
                marker_color='rgb(13, 154, 60)'
                , yaxis='y2'))

fig1.update_layout(
    title='Executed Aurora transactions',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)



# Set y-axes titles
fig1.update_yaxes(title_text="Hourly Aurora transactions", secondary_y=False)
fig1.update_yaxes(title_text="Total Aurora transactions", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df2['date'],
                y=df2['txs'],
                name='# of transactions',
                marker_color='rgb(153, 250, 185)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df2['date'],
                y=df2['cum_txs'],
                name='# of transactions',
                marker_color='rgb(13, 154, 60)'
                , yaxis='y2'))

fig2.update_layout(
    title='Aurora transactions',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Daily Aurora transactions", secondary_y=False)
fig2.update_yaxes(title_text="Total Aurora transactions", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])
fig3.add_trace(go.Bar(x=df3['date'],
                y=df3['txs'],
                name='# of transactions',
                marker_color='rgb(153, 250, 185)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df3['date'],
                y=df3['cum_txs'],
                name='# of transactions',
                marker_color='rgb(13, 154, 60)'
                , yaxis='y2'))

fig3.update_layout(
    title='Aurora transactions',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Weekly Aurora transactions", secondary_y=False)
fig3.update_yaxes(title_text="Total Aurora transactions", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Hourly transactions", "Daily transactions", "Weekly transactions"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# Create figure with secondary y-axis
fig4 = make_subplots(specs=[[{"secondary_y": True}]])

fig4.add_trace(go.Bar(x=df4['date'],
                y=df4['succeeded_txs'],
                name='# of succeeded transactions',
                marker_color='rgb(46, 203, 100)'
                , yaxis='y'))
fig4.add_trace(go.Bar(x=df4['date'],
                y=df4['failed_txs'],
                name='# of failed transactions',
                marker_color='rgb(249, 58, 58)'
                , yaxis='y'))

fig4.update_layout(
    title='Aurora transactions by type',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig4.update_yaxes(title_text="Hourly Aurora transactions by type", secondary_y=False)

# Create figure with secondary y-axis
fig5 = make_subplots(specs=[[{"secondary_y": True}]])

fig5.add_trace(go.Bar(x=df5['date'],
                y=df5['succeeded_txs'],
                name='# of succeeded transactions',
                marker_color='rgb(46, 203, 100)'
                , yaxis='y'))
fig5.add_trace(go.Bar(x=df5['date'],
                y=df5['failed_txs'],
                name='# of failed transactions',
                marker_color='rgb(249, 58, 58)'
                , yaxis='y'))

fig5.update_layout(
    title='Aurora transactions by type',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig5.update_yaxes(title_text="Daily Aurora transactions by type", secondary_y=False)
fig5.update_yaxes(title_text="Total Aurora transactions by type", secondary_y=True)

# Create figure with secondary y-axis
fig6 = make_subplots(specs=[[{"secondary_y": True}]])

fig6.add_trace(go.Bar(x=df6['date'],
                y=df6['succeeded_txs'],
                name='# of succeeded transactions',
                marker_color='rgb(46, 203, 100)'
                , yaxis='y'))
fig6.add_trace(go.Bar(x=df6['date'],
                y=df6['failed_txs'],
                name='# of failed transactions',
                marker_color='rgb(249, 58, 58)'
                , yaxis='y'))

fig6.update_layout(
    title='Aurora transactions by type',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig4.update_yaxes(title_text=" Aurora Weekly transactions by type", secondary_y=False)
fig4.update_yaxes(title_text="Total Aurora transactions by type", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Hourly transactions", "Daily transactions", "Weekly transactions"])

with tab1:
    st.plotly_chart(fig4, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig5, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig6, theme="streamlit", use_container_width=True)


# In[ ]:


sql="""
select
  trunc(block_timestamp,'hour') as date,
  sum(TRANSACTION_FEE/1e24) as fees,
  sum(fees) over (order by date) as cum_fees,
  avg(TRANSACTION_FEE/1e24) as avg_tx_fee
  from  near.core.fact_transactions x
  join near.price.fact_prices y on trunc(x.block_timestamp,'hour')=trunc(y.timestamp,'hour')
  where x.block_timestamp > getdate() - interval '1 WEEK' and symbol='wNEAR' and tx_receiver='aurora'
  group by 1
"""

sql2="""
select
  trunc(block_timestamp,'day') as date,
  sum(TRANSACTION_FEE/1e24) as fees,
  sum(fees) over (order by date) as cum_fees,
  avg(TRANSACTION_FEE/1e24) as avg_tx_fee
  from  near.core.fact_transactions x
  join near.price.fact_prices y on trunc(x.block_timestamp,'hour')=trunc(y.timestamp,'hour')
  where x.block_timestamp > getdate() - interval '2 WEEKS' and symbol='wNEAR' and tx_receiver='aurora'
  group by 1
"""

sql3="""
select
  trunc(block_timestamp,'week') as date,
  sum(TRANSACTION_FEE/1e24) as fees,
  sum(fees) over (order by date) as cum_fees,
  avg(TRANSACTION_FEE/1e24) as avg_tx_fee
  from  near.core.fact_transactions x
  join near.price.fact_prices y on trunc(x.block_timestamp,'hour')=trunc(y.timestamp,'hour')
  where x.block_timestamp > getdate() - interval '3 MONTHS' and symbol='wNEAR' and tx_receiver='aurora'
  group by 1
"""

sql4="""
select
  trunc(block_timestamp,'hour') as date,
  sum(gas_used/1e18) as fees,
  sum(fees) over (order by date) as cum_fees,
  avg(gas_used/1e18) as avg_tx_fee
  from  near.core.fact_transactions x
  join near.price.fact_prices y on trunc(x.block_timestamp,'hour')=trunc(y.timestamp,'hour')
  where x.block_timestamp > getdate() - interval '1 WEEK' and symbol='wNEAR' and tx_receiver='aurora'
  group by 1
"""

sql5="""
select
  trunc(block_timestamp,'day') as date,
  sum(gas_used/1e18) as fees,
  sum(fees) over (order by date) as cum_fees,
  avg(gas_used/1e18) as avg_tx_fee
  from  near.core.fact_transactions x
  join near.price.fact_prices y on trunc(x.block_timestamp,'hour')=trunc(y.timestamp,'hour')
  where x.block_timestamp > getdate() - interval '2 WEEKS' and symbol='wNEAR' and tx_receiver='aurora'
  group by 1
"""

sql6="""
select
  trunc(block_timestamp,'week') as date,
  sum(gas_used/1e18) as fees,
  sum(fees) over (order by date) as cum_fees,
  avg(gas_used/1e18) as avg_tx_fee
  from  near.core.fact_transactions x
  join near.price.fact_prices y on trunc(x.block_timestamp,'hour')=trunc(y.timestamp,'hour')
  where x.block_timestamp > getdate() - interval '3 MONTHS' and symbol='wNEAR' and tx_receiver='aurora'
  group by 1
"""



st.experimental_memo(ttl=1000000)
@st.cache
def compute(a):
    results=sdk.query(a)
    return results

results = compute(sql)
df = pd.DataFrame(results.records)
df.info()

results2 = compute(sql2)
df2 = pd.DataFrame(results2.records)
df2.info()

results3 = compute(sql3)
df3 = pd.DataFrame(results3.records)
df3.info()

results4 = compute(sql4)
df4 = pd.DataFrame(results4.records)
df4.info()

results5 = compute(sql5)
df5 = pd.DataFrame(results5.records)
df5.info()

results6 = compute(sql6)
df6 = pd.DataFrame(results6.records)
df6.info()

# In[22]:

st.subheader('Fees (NEAR) and used gas (Peta)')
st.write('The amount a user paid in fees for each transaction is important to the developemtn and success of a network. So, if the network congestion increase and the fees started to increase, it will be a moment when users started to do less transactions and the activity on the network will decrease, so its important to evaluate as well not only the gas price but also the amount of fees paid per transactions. So, the next metric we are gonna analyze is the amount of fees generated on Near and the gas spent.')
st.write('In concrete, the following charts show:')
st.write('- Last week fees and gas spent (hourly and cumulative)')
st.write('- Last 2 weeks fees and gas spent (daily and cumulative)')
st.write('- Last 3 months fees and gas spent (weekly and cumulative)')
st.write('- Last week average fees and gas spent (hourly)')
st.write('- Last 2 weeks average fees and gas spent (daily)')
st.write('- Last 3 months average fees and gas spent (weekly)')
st.write('')

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['fees'],
                name='NEAR',
                marker_color='rgb(253, 160, 160)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['cum_fees'],
                name='NEAR',
                marker_color='rgb(243, 21, 5)'
                , yaxis='y2'))

fig1.update_layout(
    title='Aurora fees',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)



# Set y-axes titles
fig1.update_yaxes(title_text="Hourly Aurora fees", secondary_y=False)
fig1.update_yaxes(title_text="Total Aurora fees", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df2['date'],
                y=df2['fees'],
                name='NEAR',
                marker_color='rgb(253, 160, 160)'
                , yaxis='y'))

fig2.update_layout(
    title='Aurora fees',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Daily Aurora fees", secondary_y=False)
fig2.update_yaxes(title_text="Total Aurora fees", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])
fig3.add_trace(go.Bar(x=df3['date'],
                y=df3['fees'],
                name='NEAR',
                marker_color='rgb(253, 160, 160)'
                , yaxis='y'))

fig3.update_layout(
    title='Aurora fees',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Weekly Aurora fees", secondary_y=False)
fig3.update_yaxes(title_text="Total Aurora fees", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Hourly fees", "Daily fees", "Weekly fees"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)



import plotly.express as px

# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1 = px.area(df, x="date", y="avg_tx_fee",color_discrete_sequence=px.colors.qualitative.Light24)

fig1.update_layout(
    title='Aurora average transaction fees',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)



# Set y-axes titles
fig1.update_yaxes(title_text="Hourly transaction fee", secondary_y=False)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2 = px.area(df2, x="date", y="avg_tx_fee",color_discrete_sequence=px.colors.qualitative.Light24)


fig2.update_layout(
    title='Aurora average transaction fees',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)



# Set y-axes titles
fig2.update_yaxes(title_text="Daily transaction fee", secondary_y=False)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3 = px.area(df3, x="date", y="avg_tx_fee", color_discrete_sequence=px.colors.qualitative.Light24)


fig3.update_layout(
    title='Aurora average transaction fees',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)



# Set y-axes titles
fig3.update_yaxes(title_text="Weekly transaction fee", secondary_y=False)

tab1, tab2, tab3 = st.tabs(["Hourly average fees", "Daily average fees", "Weekly average fees"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)






# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df4['date'],
                y=df4['fees'],
                name='NEAR',
                marker_color='rgb(253, 160, 160)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df4['date'],
                y=df4['cum_fees'],
                name='NEAR',
                marker_color='rgb(240, 21, 5)'
                , yaxis='y2'))

fig1.update_layout(
    title='Near gas used (Peta)',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)



# Set y-axes titles
fig1.update_yaxes(title_text="Hourly gas used (Peta)", secondary_y=False)
fig1.update_yaxes(title_text="Total gas used (Peta)", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df5['date'],
                y=df5['fees'],
                name='NEAR',
                marker_color='rgb(253, 160, 160)'
                , yaxis='y'))

fig2.update_layout(
    title='Near gas used (Peta)',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Daily gas used (Peta)", secondary_y=False)
fig2.update_yaxes(title_text="Total gas used (Peta)", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])
fig3.add_trace(go.Bar(x=df6['date'],
                y=df6['fees'],
                name='NEAR',
                marker_color='rgb(253, 160, 160)'
                , yaxis='y'))

fig3.update_layout(
    title='Near gas used (Peta)',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Weekly gas used (Peta)", secondary_y=False)
fig3.update_yaxes(title_text="Total gas used (Peta)", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Hourly gas used", "Daily gas used", "Weekly gas used"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)






# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1 = px.area(df4, x="date", y="avg_tx_fee",color_discrete_sequence=px.colors.qualitative.Light24)


fig1.update_layout(
    title='Aurora average gas used (Peta)',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)



# Set y-axes titles
fig1.update_yaxes(title_text="Hourly gas used (Peta)", secondary_y=False)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2 = px.area(df5, x="date", y="avg_tx_fee",color_discrete_sequence=px.colors.qualitative.Light24)


fig2.update_layout(
    title='Near gas used (Peta)',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)



# Set y-axes titles
fig2.update_yaxes(title_text="Daily gas used (Peta)", secondary_y=False)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3 = px.area(df6, x="date", y="avg_tx_fee",color_discrete_sequence=px.colors.qualitative.Light24)


fig3.update_layout(
    title='Near gas used (Peta)',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)



# Set y-axes titles
fig3.update_yaxes(title_text="Weekly gas used (Peta)", secondary_y=False)

tab1, tab2, tab3 = st.tabs(["Hourly gas used", "Daily gas used", "Weekly gas used"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[15]:


sql = f"""
SELECT
trunc(first_date,'hour') as date,
count(distinct receiver_id ) as new_contracts,
  sum(new_contracts) over (order by date) as cum_new_contracts
from (select
  x.receiver_id,
  min(x.block_timestamp) as first_date
from near.core.fact_actions_events x
join near.core.fact_receipts y on x.tx_hash=y.tx_hash
where action_name = 'DeployContract'
  group by 1) where first_date >= CURRENT_DATE - INTERVAL '1 WEEK'
group by 1
order by 1 asc
"""

sql2 = f"""
SELECT
trunc(first_date,'day') as date,
count(distinct receiver_id ) as new_contracts,
  sum(new_contracts) over (order by date) as cum_new_contracts
from (select
  x.receiver_id,
  min(x.block_timestamp) as first_date
from near.core.fact_actions_events x
join near.core.fact_receipts y on x.tx_hash=y.tx_hash
where action_name = 'DeployContract'
  group by 1) where first_date >= CURRENT_DATE - INTERVAL '2 WEEKS'
group by 1
order by 1 asc
"""

sql3 = f"""
SELECT
trunc(first_date,'week') as date,
count(distinct receiver_id ) as new_contracts,
  sum(new_contracts) over (order by date) as cum_new_contracts
from (select
  x.receiver_id,
  min(x.block_timestamp) as first_date
from near.core.fact_actions_events x
join near.core.fact_receipts y on x.tx_hash=y.tx_hash
where action_name = 'DeployContract'
  group by 1) where first_date >= CURRENT_DATE - INTERVAL '3 MONTHS'
group by 1
order by 1 asc
"""

sql4="""
SELECT
	date_trunc('hour', call.block_timestamp) as date,
  case when split(split(rc.status_value,':')[0],'{')[1] ilike '%Failure%' then 'Fail execution'
  else 'Successful execution' end as type,
    COUNT(DISTINCT tr.tx_hash) as smart_contracts,
  sum(smart_contracts) over (partition by type order by date) as cum_smart_contracts
FROM near.core.fact_actions_events_function_call call
INNER JOIN near.core.fact_transactions tr
ON call.TX_HASH = tr.TX_HASH
INNER JOIN near.core.fact_receipts as rc
ON tr.TX_HASH=rc.TX_HASH
	WHERE ACTION_NAME = 'FunctionCall'
    AND METHOD_NAME <> 'new'
  	AND date >=CURRENT_DATE-INTERVAL '1 WEEK' and tr.tx_receiver='aurora'
group by 1,2 order by 1 asc,2 desc
"""

sql5="""
SELECT
	date_trunc('day', call.block_timestamp) as date,
  case when split(split(rc.status_value,':')[0],'{')[1] ilike '%Failure%' then 'Fail execution'
  else 'Successful execution' end as type,
    COUNT(DISTINCT tr.tx_hash) as smart_contracts,
  sum(smart_contracts) over (partition by type order by date) as cum_smart_contracts
FROM near.core.fact_actions_events_function_call call
INNER JOIN near.core.fact_transactions tr
ON call.TX_HASH = tr.TX_HASH
INNER JOIN near.core.fact_receipts as rc
ON tr.TX_HASH=rc.TX_HASH
	WHERE ACTION_NAME = 'FunctionCall'
    AND METHOD_NAME <> 'new'
  	AND date >=CURRENT_DATE-INTERVAL '2 WEEKS' and tr.tx_receiver='aurora'
group by 1,2 order by 1 asc,2 desc
"""

sql6="""
SELECT
	date_trunc('week', call.block_timestamp) as date,
  case when split(split(rc.status_value,':')[0],'{')[1] ilike '%Failure%' then 'Fail execution'
  else 'Successful execution' end as type,
    COUNT(DISTINCT tr.tx_hash) as smart_contracts,
  sum(smart_contracts) over (partition by type order by date) as cum_smart_contracts
FROM near.core.fact_actions_events_function_call call
INNER JOIN near.core.fact_transactions tr
ON call.TX_HASH = tr.TX_HASH
INNER JOIN near.core.fact_receipts as rc
ON tr.TX_HASH=rc.TX_HASH
	WHERE ACTION_NAME = 'FunctionCall'
    AND METHOD_NAME <> 'new'
  	AND date >=CURRENT_DATE-INTERVAL '3 MONTHS' and tr.tx_receiver='aurora'
group by 1,2 order by 1 asc,2 desc
"""


st.experimental_memo(ttl=1000000)
@st.cache
def compute(a):
    data=sdk.query(a)
    return data

results = compute(sql)
df = pd.DataFrame(results.records)
df.info()

results2 = compute(sql2)
df2 = pd.DataFrame(results2.records)
df2.info()

results3 = compute(sql3)
df3 = pd.DataFrame(results3.records)
df3.info()

results4 = compute(sql4)
df4 = pd.DataFrame(results4.records)
df4.info()

results5 = compute(sql5)
df5 = pd.DataFrame(results5.records)
df5.info()

results6 = compute(sql6)
df6 = pd.DataFrame(results6.records)
df6.info()

# In[22]:

st.subheader('Activity on Aurora contracts')
st.write('The final metric to take into account is the amount of new and active contracts on the ecosystem. If the amount of new contracts increase, it would say that the network is growing and then, in expansion. So, its important to calculate this metric as well as the active contracts right now to see if the ecosystem is consistent.')
st.write('In concrete, the following charts show:')
st.write('- Last week new and active contracts (hourly and cumulative)')
st.write('- Last 2 weeks new and active contracts (daily and cumulative)')
st.write('- Last 3 months new and active contracts (weekly and cumulative)')
st.write('')

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Create figure with secondary y-axis

import plotly.express as px

fig4 = px.area(df4, x="date", y="smart_contracts", color="type", color_discrete_sequence=px.colors.qualitative.Dark2)
fig4.update_layout(
    title='Activity on Aurora contracts',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)


fig5 = px.area(df5, x="date", y="smart_contracts", color="type", color_discrete_sequence=px.colors.qualitative.Dark2)
fig5.update_layout(
    title='Activity on Aurora contracts',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

fig6 = px.area(df6, x="date", y="smart_contracts", color="type", color_discrete_sequence=px.colors.qualitative.Dark2)
fig6.update_layout(
    title='Activity on Aurora contracts',
    xaxis_tickfont_size=14,
    yaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

tab1, tab2, tab3 = st.tabs(["Hourly interactions contracts", "Daily interactions contracts", "Weekly interactions contracts"])

with tab1:
    st.plotly_chart(fig4, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig5, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig6, theme="streamlit", use_container_width=True)

st.subheader('Conclusions')
st.markdown('Following the structure of the Near Foundation Weekly Transparency Report and using Flipside Crypto and MetricsDAO data to study Aurora, I have been able to develop a tool that tracks the recent Aurora activity in a more user-friendly and clean way.')
st.markdown('The most interesting thing I have found is the higher amount of failed transactions that are occurring when users interacts with Aurora contract. In fact, there are some moments when the amount of failed transactions is higher than the success transactions!')
st.markdown('Furhtermore, even the activity seems remained constant and users used to interact with Aurora smart contracts, the amount of failed smart contract interactions is also higher.')
st.write('')
st.markdown('This app has been done by **_Adrià Parcerisas_**, a PhD Biomedical Engineer related to Machine Learning and Artificial intelligence technical projects for data analysis and research, as well as dive deep on-chain data analysis about cryptocurrency projects. You can find me on [Twitter](https://twitter.com/adriaparcerisas)')
st.write('')
st.markdown('The full sources used to develop this app can be found to the following link: [Github link](https://github.com/adriaparcerisas/aurora-on-near)')
st.markdown('_Powered by [Flipside Crypto](https://flipsidecrypto.xyz) and [MetricsDAO](https://metricsdao.notion.site)_')


# In[ ]:
