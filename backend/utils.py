from collections import Counter
from datetime import datetime, timedelta

import pandas as pd


def get_geolocation(ip_address, geoip_reader):
    try:
        response = geoip_reader.city(ip_address)
        if ip_address == '127.0.0.1':
            return 'localhost', 'localhost'
        city = response.city.name or "Unknown"
        country = response.country.name or "Unknown"
        return city, country
    except Exception:
        return "Unknown", "Unknown"


def init_question_data(question):
    result = {}
    data = question.get('data', {})
    title = data.get('text')
    if title:
        result['title'] = title
    result['type'] = question['type']
    if question['type'] in ['single', 'multiple']:
        result['answers'] = {option: 0 for option in data.get('options', [])}
    elif question['type'] == 'text':
        result['text_lengths'] = []
        result['text_responses'] = []
    return result


def finalize_question_data(data, total_responses):
    if 'text_lengths' in data:
        data['average_text_length'] = (
            sum(data['text_lengths']) / len(data['text_lengths'])
            if data['text_lengths'] else 0
        )
        text_response_counter = Counter(data['text_responses'])
        top_text_responses = text_response_counter.most_common(3)

        data['top_3_text_responses'] = [{
            'response': response,
            'count': count,
            'percentage': (count / total_responses) * 100 if total_responses > 0 else 0
        } for response, count in top_text_responses]

        del data['text_lengths']
        del data['text_responses']

    else:
        data['answer_percentages'] = {
            option: (count / total_responses) * 100 if total_responses > 0 else 0
            for option, count in data['answers'].items()
        }


def process_timestamps(timestamps):
    if not timestamps:
        return {
            date.strftime('%Y-%m-%d'): {'count': 0, 'percentage': 0.0}
            for date in pd.date_range(end=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                                      periods=8,
                                      tz='UTC')
        }

    dates = []
    for ts in timestamps:
        if ts is not None:
            try:
                date = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                dates.append(date)
            except ValueError:
                continue

    df = pd.DataFrame({'date': dates})
    df['date'] = df['date'].dt.tz_convert('UTC').dt.floor('D')

    end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = end_date - timedelta(days=7)
    all_dates = pd.date_range(start=start_date, end=end_date, tz='UTC')
    date_counts = df['date'].value_counts().reindex(all_dates, fill_value=0).sort_index()

    total_responses_per_day = date_counts.sum()

    if total_responses_per_day > 0:
        percentages = (date_counts / total_responses_per_day) * 100
    else:
        percentages = pd.Series([0] * len(all_dates), index=all_dates)

    aggregated_data = {
        date.strftime('%Y-%m-%d'): {'count': int(count), 'percentage': float(perc)}
        for date, count, perc in zip(all_dates, date_counts, percentages)
    }

    return aggregated_data
