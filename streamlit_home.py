import streamlit as st

import pandas as pd
import numpy as np
import os

import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title='Big Data Sytem Findings', 
    layout='wide'
)

st.markdown(
"""
<style>
div[data-testid="stSidebarNav"] {display: none;}
.stButton > button {
    text-align: center;
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>
""", 
unsafe_allow_html=True)

df_users_st = pd.read_csv(os.path.join(os.getcwd(), 'users_comprehensive.csv'))
users_list = [user.lower() for user in df_users_st['user_id'].values.tolist()]
df_events_stream = pd.read_csv(os.path.join(os.getcwd(), 'stream_results.csv'))
df_streams_batch = pd.read_csv(os.path.join(os.getcwd(), 'sample_stream_events.csv'))

st.title('Company Data Access Dashboard')
st.divider()

# Distribution of Requests per Hour

df_streams_batch['event_time'] = pd.to_datetime(df_streams_batch['event_time'])
events_hour = df_streams_batch[['event_id', 'event_time']].copy()
events_hour['hour'] = events_hour['event_time'].apply(lambda x: x.hour)

daily_requests = events_hour.groupby(by='hour').agg({
    'event_id': 'count'
}).rename(columns={
    'event_id':'total_events'
})

top_col1, top_col2 = st.columns([0.7, 0.3], vertical_alignment='center')
with top_col1:
    st.markdown("<h3 style='text-align: center;'>Distribution of Events per Hour</h3>", unsafe_allow_html=True) 
    fig, ax = plt.subplots(figsize=(18, 6))
    sns.lineplot(x=daily_requests.index, y=daily_requests['total_events'], marker='o', color='red', ax=ax)
    ax.axhline(daily_requests['total_events'].mean(), color='green', linestyle='--')
    plt.text(x=0, y=200, s=f'mean: {round(daily_requests['total_events'].mean(), 2)}')
    plt.xticks(range(min(daily_requests.index), max(daily_requests.index)+1, 1))
    st.pyplot(fig)

with top_col2:
    with st.container(border=True): 
        # Alert Distribution

        st.markdown("<h3 style='text-align: center;'>Number of Alerts</h3>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(4,3))
        counts = df_events_stream['alert'].value_counts()
        sns.barplot(x=counts.index, y=counts.values, hue=counts.index, width=0.6, palette='viridis', ax=ax)
        for val in ax.containers:
            label=[v.get_height() for v in val]
            ax.bar_label(val, label=label, label_type='edge')
        ax.set_ylim(top=85000)
        st.pyplot(fig)

st.divider()

with st.container(border=True):
    st.markdown(f"<h3 style='text-align: center;'>User Distribution</h3>", unsafe_allow_html=True)
    st.divider()
    col1, col2 = st.columns([0.2, 0.8])

    # Get User Details
    with col1:
        st.markdown("<h3>Get User Details</h3>", unsafe_allow_html=True)
        user_id = st.text_input(label='Insert User ID', placeholder='U00XX...')
        if user_id:
            if user_id.lower() in users_list:
                st.write(f'{user_id} Found!')

                user = df_users_st[df_users_st['user_id']==user_id.upper()].iloc[0]
                df_shown = pd.DataFrame({
                    '.': df_users_st.columns,
                    'Details': list(map(lambda x: round(float(x), 2) if type(x) in (np.float64, np.int64) else x, user.values.tolist()))
                })
                df_shown['Details'] = df_shown['Details'].astype(str)
                st.dataframe(df_shown, height='content', hide_index=True)
            else:
                st.write(f'Try Again! {user_id} Not Found!')


    # 5 Most Active Users & Most Used Assets

    df_most_active_users = df_streams_batch['user_id'].value_counts().head(5)
    df_most_used_assets = df_streams_batch['asset_id'].value_counts().head(5)
    dataframes = {
        'Most Active Users': df_most_active_users,
        'Most Used Assets': df_most_used_assets,
    }
    color = ['green', 'blue']

    with col2:
        col1_top_5, col2_top_5 = st.columns(2)
        col3_user, col4_user = st.columns(2)

        with col1_top_5:
            with st.container(border=True, height=400):
                item = 'Most Active Users'
                st.markdown(f"<h5 style='text-align: center;'>5 {item}</h5>", unsafe_allow_html=True)
                fig, ax = plt.subplots(figsize=(8, 5))
                sns.barplot(x=dataframes[item].index, y=dataframes[item].values, color=color[0], ax=ax)
                for val in ax.containers:
                    label=[v.get_height() for v in val]
                    ax.bar_label(val, label=label, label_type='edge')
                plt.tight_layout()
                st.pyplot(fig)

        with col2_top_5:
            with st.container(border=True, height=400):
                item = 'Most Used Assets'
                st.markdown(f"<h5 style='text-align: center;'>5 {item}</h5>", unsafe_allow_html=True)
                fig, ax = plt.subplots(figsize=(8, 5))
                sns.barplot(x=dataframes[item].index, y=dataframes[item].values, color=color[1], ax=ax)
                for val in ax.containers:
                    label=[v.get_height() for v in val]
                    ax.bar_label(val, label=label, label_type='edge')
                plt.tight_layout()
                st.pyplot(fig)

        with col3_user:
            with st.container(border=True, height=400):
                st.markdown("<h5 style='text-align: center'>Distribution of User Location</h5>", unsafe_allow_html=True)
                fig, ax = plt.subplots(figsize=(8, 4))
                count = df_users_st['location'].value_counts()
                ax = sns.barplot(x=count.index, y=count.values, color='teal')
                for val in ax.containers:
                    label=[v.get_height() for v in val]
                    ax.bar_label(val, label=label, label_type='edge')
                plt.title(f'Distribution of User Location')
                st.pyplot(fig)

        with col4_user:
            with st.container(border=True, height=400):
                st.markdown("<h5 style='text-align: center'>Distribution of User Role</h5>", unsafe_allow_html=True)
                fig, ax = plt.subplots(figsize=(8, 4))
                count = df_users_st['role'].value_counts()
                ax = sns.barplot(x=count.index, y=count.values, color='orange')
                for val in ax.containers:
                    label=[v.get_height() for v in val]
                    ax.bar_label(val, label=label, label_type='edge')
                st.pyplot(fig)
