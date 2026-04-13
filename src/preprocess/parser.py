"""
parser.py — WhatsApp chat preprocessing engine.

Handles:
  • Multiple export formats (12-hour / 24-hour, DD/MM/YYYY, MM/DD/YY)
  • Derived time columns
  • Response-time computation
  • Urdu / noise-character stripping
"""
from __future__ import annotations

import re
import pandas as pd
from typing import Optional


# ── Regex helpers ──────────────────────────────────────────────────────────────
_TIMESTAMP_PATTERN = re.compile(
    r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s?[apAP][mM])?\s\s-\s'
)

_DATE_FORMATS = [
    '%m/%d/%y, %H:%M  - ',
    '%d/%m/%Y, %H:%M  - ',
    '%m/%d/%Y, %H:%M  - ',
    '%d/%m/%y, %H:%M  - ',
    '%m/%d/%y, %I:%M %p  - ',
    '%d/%m/%Y, %I:%M %p  - ',
]


def _remove_urdu(text: str) -> str:
    """Strip Urdu/Arabic Unicode characters that break font rendering."""
    return re.sub(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+', '', text)


def _clean_timestamp(raw: str) -> str:
    """Normalise narrow no-break space and other whitespace variants."""
    return raw.replace('\u202f', ' ').replace('\u00a0', ' ')


def _parse_date(date_str: str) -> Optional[pd.Timestamp]:
    for fmt in _DATE_FORMATS:
        try:
            return pd.to_datetime(date_str, format=fmt)
        except ValueError:
            continue
    return pd.NaT


def _split_user_message(raw_message: str):
    """Return (user, message) tuple from a raw WhatsApp message body."""
    parts = re.split(r'([\w\W]+?):\s', raw_message, maxsplit=1)
    if len(parts) >= 3:
        return parts[1], ''.join(parts[2:])
    return 'group_notification', raw_message


def preprocess(raw_data: str) -> pd.DataFrame:
    """
    Parse a raw WhatsApp chat export string into a clean DataFrame.

    Returns
    -------
    pd.DataFrame with columns:
        date, users, messages, year, month, day, hour, minute,
        weekday_name, only_dates, period
    """
    # Remove stray AM/PM tokens from 12-hour exports already baked into the pattern
    raw_data = re.sub(r'\b(?:am|pm)\b', '', raw_data, flags=re.IGNORECASE)

    raw_dates    = _TIMESTAMP_PATTERN.findall(raw_data)
    raw_messages = _TIMESTAMP_PATTERN.split(raw_data)[1:]

    if not raw_dates:
        raise ValueError(
            "No WhatsApp timestamps found. "
            "Please upload a valid WhatsApp .txt export."
        )

    cleaned_dates = [_clean_timestamp(d) for d in raw_dates]

    df = pd.DataFrame({
        'raw_message': raw_messages,
        'raw_date':    cleaned_dates,
    })

    df['date'] = df['raw_date'].apply(_parse_date)
    df.dropna(subset=['date'], inplace=True)

    # Split user / message
    parsed = df['raw_message'].apply(_split_user_message)
    df['users']    = [p[0] for p in parsed]
    df['messages'] = [p[1] for p in parsed]

    df.drop(columns=['raw_message', 'raw_date'], inplace=True)

    # ── Derived columns ────────────────────────────────────────────────────────
    df['year']         = df['date'].dt.year
    df['month']        = df['date'].dt.month_name()
    df['month_num']    = df['date'].dt.month
    df['day']          = df['date'].dt.day
    df['hour']         = df['date'].dt.hour
    df['minute']       = df['date'].dt.minute
    df['weekday_name'] = df['date'].dt.day_name()
    df['only_dates']   = df['date'].dt.date

    # Hour-period label e.g. "22-23"
    df['period'] = df['hour'].apply(
        lambda h: f"00-01" if h == 0 else (f"{h}-00" if h == 23 else f"{h}-{h+1}")
    )

    # Clean message text
    df['messages'] = df['messages'].apply(_remove_urdu)

    df.reset_index(drop=True, inplace=True)
    return df


def compute_response_times(df: pd.DataFrame) -> pd.Series:
    """
    Average response time (minutes) per user.
    Only counts cross-user replies; ignores gaps > 24 h.
    """
    real = df[df['users'] != 'group_notification'].sort_values('date').copy()
    real['prev_user'] = real['users'].shift(1)
    real['prev_time'] = real['date'].shift(1)

    resp = real[real['users'] != real['prev_user']].copy()
    resp['resp_min'] = (resp['date'] - resp['prev_time']).dt.total_seconds() / 60
    resp = resp[(resp['resp_min'] >= 0) & (resp['resp_min'] <= 1440)]

    return resp.groupby('users')['resp_min'].mean().round(1)
