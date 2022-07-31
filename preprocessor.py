import re
import pandas as pd

def preprocess(data_rashi):
    pattern_1 = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[a-zA-Z]+\s-\s'

    messages = re.split(pattern_1, data_rashi)[1:]

    pattern_2 = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s'
    dates=re.findall(pattern_2,data_rashi)

    df = pd.DataFrame({'user_messages': messages, 'message_dates': dates})
    df['message_dates'] = pd.to_datetime(df['message_dates'])
    df.rename(columns={'message_dates': 'dates'}, inplace=True)
    users = []
    messages = []
    for message in df['user_messages']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group notification')
            messages.append(entry[0])
    df['user'] = users
    df['messages'] = messages
    df.drop(columns=['user_messages'], inplace=True)
    df['year'] = df['dates'].dt.year
    df['month'] = df['dates'].dt.month_name()
    df['month_num'] = df['dates'].dt.month
    df['only_date'] = df['dates'].dt.date
    df['day_name'] = df['dates'].dt.day_name()
    df['day'] = df['dates'].dt.day
    df['hour'] = df['dates'].dt.hour
    df['minute'] = df['dates'].dt.minute
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    return df
