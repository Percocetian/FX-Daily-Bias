import pandas as pd

# Load the data from the CSV file
pair = ('EURUSD_historical_data.csv')
df = pd.read_csv(pair)

# Convert 'Date' to datetime and sort by date
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')
df = df.sort_values(by='Date')

# Function to determine the daily bias
def determine_daily_bias(df):
    biases = []
    for i in range(1, len(df)):
        if df.iloc[i]['Price'] > df.iloc[i-1]['Price']:
            biases.append('UP')
        else:
            biases.append('DOWN')
    return biases

# Function to analyze the closing positions based on ICT DAILY BIAS
def analyze_closing_positions(df, biases):
    patterns = {
        'prev_UP_above_HIGH': 0,
        'prev_UP_below_LOW': 0,
        'prev_UP_wicked_BOTH': 0,
        'prev_UP_neither': 0,
        'prev_DOWN_above_HIGH': 0,
        'prev_DOWN_below_LOW': 0,
        'prev_DOWN_wicked_BOTH': 0,
        'prev_DOWN_neither': 0,
        'next_day_UP_after_UP': 0,
        'next_day_DOWN_after_UP': 0,
        'next_day_UP_after_DOWN': 0,
        'next_day_DOWN_after_DOWN': 0,
        'prev_UP_above_body': 0,
        'prev_UP_below_body': 0,
        'prev_DOWN_above_body': 0,
        'prev_DOWN_below_body': 0,
        'prev_UP_inside_body': 0,
        'prev_DOWN_inside_body': 0,
        'next_day_UP_after_body_up': 0,
        'next_day_DOWN_after_body_up': 0,
        'next_day_UP_after_body_down': 0,
        'next_day_DOWN_after_body_down': 0
    }

    for i in range(1, len(df) - 1):
        prev_candle = df.iloc[i - 1]
        curr_candle = df.iloc[i]
        next_candle = df.iloc[i + 1]
        bias = biases[i - 1]

        if curr_candle['Price'] > prev_candle['High']:
            if bias == 'UP':
                patterns['prev_UP_above_HIGH'] += 1
            else:
                patterns['prev_DOWN_above_HIGH'] += 1
        elif curr_candle['Price'] < prev_candle['Low']:
            if bias == 'UP':
                patterns['prev_UP_below_LOW'] += 1
            else:
                patterns['prev_DOWN_below_LOW'] += 1
        elif prev_candle['Low'] <= curr_candle['Price'] <= prev_candle['High']:
            if curr_candle['Price'] == prev_candle['High'] or curr_candle['Price'] == prev_candle['Low']:
                if bias == 'UP':
                    patterns['prev_UP_wicked_BOTH'] += 1
                else:
                    patterns['prev_DOWN_wicked_BOTH'] += 1
            else:
                if bias == 'UP':
                    patterns['prev_UP_neither'] += 1
                else:
                    patterns['prev_DOWN_neither'] += 1

        if prev_candle['Open'] <= curr_candle['Price'] <= prev_candle['Price']:
            if bias == 'UP':
                patterns['prev_UP_inside_body'] += 1
            else:
                patterns['prev_DOWN_inside_body'] += 1
        elif curr_candle['Price'] > prev_candle['Price']:
            if bias == 'UP':
                patterns['prev_UP_above_body'] += 1
            else:
                patterns['prev_DOWN_above_body'] += 1
        elif curr_candle['Price'] < prev_candle['Open']:
            if bias == 'UP':
                patterns['prev_UP_below_body'] += 1
            else:
                patterns['prev_DOWN_below_body'] += 1

        if bias == 'UP':
            if next_candle['Price'] > curr_candle['Price']:
                patterns['next_day_UP_after_UP'] += 1
            else:
                patterns['next_day_DOWN_after_UP'] += 1
            if next_candle['Price'] > prev_candle['Price']:
                patterns['next_day_UP_after_body_up'] += 1
            else:
                patterns['next_day_DOWN_after_body_up'] += 1
        else:
            if next_candle['Price'] > curr_candle['Price']:
                patterns['next_day_UP_after_DOWN'] += 1
            else:
                patterns['next_day_DOWN_after_DOWN'] += 1
            if next_candle['Price'] > prev_candle['Price']:
                patterns['next_day_UP_after_body_down'] += 1
            else:
                patterns['next_day_DOWN_after_body_down'] += 1

    return patterns

# Determine daily biases
biases = determine_daily_bias(df)

# Analyze closing positions and next day movements
patterns = analyze_closing_positions(df, biases)

print("Patterns Count:", patterns)

# Calculating probabilities
total_up = biases.count('UP')
total_down = biases.count('DOWN')

probabilities = {
    'prev_UP_above_HIGH': patterns['prev_UP_above_HIGH'] / total_up if total_up > 0 else 0,
    'prev_UP_below_LOW': patterns['prev_UP_below_LOW'] / total_up if total_up > 0 else 0,
    'prev_UP_wicked_BOTH': patterns['prev_UP_wicked_BOTH'] / total_up if total_up > 0 else 0,
    'prev_UP_neither': patterns['prev_UP_neither'] / total_up if total_up > 0 else 0,
    'prev_DOWN_above_HIGH': patterns['prev_DOWN_above_HIGH'] / total_down if total_down > 0 else 0,
    'prev_DOWN_below_LOW': patterns['prev_DOWN_below_LOW'] / total_down if total_down > 0 else 0,
    'prev_DOWN_wicked_BOTH': patterns['prev_DOWN_wicked_BOTH'] / total_down if total_down > 0 else 0,
    'prev_DOWN_neither': patterns['prev_DOWN_neither'] / total_down if total_down > 0 else 0,
    'next_day_UP_after_UP': patterns['next_day_UP_after_UP'] / total_up if total_up > 0 else 0,
    'next_day_DOWN_after_UP': patterns['next_day_DOWN_after_UP'] / total_up if total_up > 0 else 0,
    'next_day_UP_after_DOWN': patterns['next_day_UP_after_DOWN'] / total_down if total_down > 0 else 0,
    'next_day_DOWN_after_DOWN': patterns['next_day_DOWN_after_DOWN'] / total_down if total_down > 0 else 0,
    'prev_UP_above_body': patterns['prev_UP_above_body'] / total_up if total_up > 0 else 0,
    'prev_UP_below_body': patterns['prev_UP_below_body'] / total_up if total_up > 0 else 0,
    'prev_DOWN_above_body': patterns['prev_DOWN_above_body'] / total_down if total_down > 0 else 0,
    'prev_DOWN_below_body': patterns['prev_DOWN_below_body'] / total_down if total_down > 0 else 0,
    'prev_UP_inside_body': patterns['prev_UP_inside_body'] / total_up if total_up > 0 else 0,
    'prev_DOWN_inside_body': patterns['prev_DOWN_inside_body'] / total_down if total_down > 0 else 0,
    'next_day_UP_after_body_up': patterns['next_day_UP_after_body_up'] / total_up if total_up > 0 else 0,
    'next_day_DOWN_after_body_up': patterns['next_day_DOWN_after_body_up'] / total_up if total_up > 0 else 0,
    'next_day_UP_after_body_down': patterns['next_day_UP_after_body_down'] / total_down if total_down > 0 else 0,
    'next_day_DOWN_after_body_down': patterns['next_day_DOWN_after_body_down'] / total_down if total_down > 0 else 0
}

# Normalizing probabilities within each section to ensure no section exceeds 100%
sections = {
    "Closing Positions of Previous Candle": [
        'prev_UP_above_HIGH',
        'prev_UP_below_LOW',
        'prev_UP_wicked_BOTH',
        'prev_UP_neither',
        'prev_DOWN_above_HIGH',
        'prev_DOWN_below_LOW',
        'prev_DOWN_wicked_BOTH',
        'prev_DOWN_neither'
    ],
    "Next Day Closing Behavior - After Bullish Candle": [
        'next_day_UP_after_UP',
        'next_day_DOWN_after_UP'
    ],
    "Next Day Closing Behavior - After Bearish Candle": [
        'next_day_UP_after_DOWN',
        'next_day_DOWN_after_DOWN'
    ],
    "Closing Relative to Previous Candle Body": [
        'prev_UP_above_body',
        'prev_UP_below_body',
        'prev_DOWN_above_body',
        'prev_DOWN_below_body'
    ],
    "Closing Inside Previous Candle Body": [
        'prev_UP_inside_body',
        'prev_DOWN_inside_body'
    ],
    "Next Day Behavior Relative to Previous Candle Body - After Bullish Candle": [
        'next_day_UP_after_body_up',
        'next_day_DOWN_after_body_up'
    ],
    "Next Day Behavior Relative to Previous Candle Body - After Bearish Candle": [
        'next_day_UP_after_body_down',
        'next_day_DOWN_after_body_down'
    ]
}

descriptions = {
    'prev_UP_above_HIGH': "The probability of closing above the high of the previous bullish candle is {:.2f}%",
    'prev_UP_below_LOW': "The probability of closing below the low of the previous bullish candle is {:.2f}%",
    'prev_UP_wicked_BOTH': "The probability of wicking both above and below the previous bullish candle is {:.2f}%",
    'prev_UP_neither': "The probability of closing neither above nor below the previous bullish candle is {:.2f}%",
    'prev_DOWN_above_HIGH': "The probability of closing above the high of the previous bearish candle is {:.2f}%",
    'prev_DOWN_below_LOW': "The probability of closing below the low of the previous bearish candle is {:.2f}%",
    'prev_DOWN_wicked_BOTH': "The probability of wicking both above and below the previous bearish candle is {:.2f}%",
    'prev_DOWN_neither': "The probability of closing neither above nor below the previous bearish candle is {:.2f}%",
    'next_day_UP_after_UP': "The probability of the next day closing higher after a bullish candle is {:.2f}%",
    'next_day_DOWN_after_UP': "The probability of the next day closing lower after a bullish candle is {:.2f}%",
    'next_day_UP_after_DOWN': "The probability of the next day closing higher after a bearish candle is {:.2f}%",
    'next_day_DOWN_after_DOWN': "The probability of the next day closing lower after a bearish candle is {:.2f}%",
    'prev_UP_above_body': "The probability of closing above the body of the previous bullish candle is {:.2f}%",
    'prev_UP_below_body': "The probability of closing below the body of the previous bullish candle is {:.2f}%",
    'prev_DOWN_above_body': "The probability of closing above the body of the previous bearish candle is {:.2f}%",
    'prev_DOWN_below_body': "The probability of closing below the body of the previous bearish candle is {:.2f}%",
    'prev_UP_inside_body': "The probability of closing inside the body of the previous bullish candle is {:.2f}%",
    'prev_DOWN_inside_body': "The probability of closing inside the body of the previous bearish candle is {:.2f}%",
    'next_day_UP_after_body_up': "The probability of the next day closing higher after closing above the body of a bullish candle is {:.2f}%",
    'next_day_DOWN_after_body_up': "The probability of the next day closing lower after closing above the body of a bullish candle is {:.2f}%",
    'next_day_UP_after_body_down': "The probability of the next day closing higher after closing below the body of a bearish candle is {:.2f}%",
    'next_day_DOWN_after_body_down': "The probability of the next day closing lower after closing below the body of a bearish candle is {:.2f}%"
}

print("\nProbabilities:")

for section_name, pattern_list in sections.items():
    section_sum = sum(probabilities[pattern] for pattern in pattern_list)
    print(f"\n{section_name}:")
    for pattern in pattern_list:
        probability = probabilities.get(pattern, 0)
        normalized_prob = (probability / section_sum) * 100 if section_sum > 0 else 0
        count = patterns.get(pattern, 0)
        print(f"'{pattern}': {count} - {descriptions.get(pattern, 'Unknown pattern').format(normalized_prob)}")
    print()