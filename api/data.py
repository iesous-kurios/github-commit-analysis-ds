import pandas as pd
import numpy as np


def cleanCounts(df):
    '''Remove {totalCount: } from the counts columns to the data is cleaner
       and {login: from author column'''
    df['author'] = df['author'].str.replace("{'login':", '')
    for i in df.columns:
        if df[i].dtypes == 'O':
            df[i] = df[i].str.replace("{'totalCount':", '')
            df[i] = df[i].str.replace('}', '')
    return df

def findTimeToClose(df):
    '''Generate feature showing the time it takes from pull request opening
       to pull request being either merged or closed.'''
    df['closedAt'] = pd.to_datetime(df['closedAt'], infer_datetime_format=True)
    df['createdAt'] = pd.to_datetime(df['createdAt'], infer_datetime_format=True)
    df['timeToClosure'] = df['closedAt'] - df['createdAt']
    return df