import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

FILTER_MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
FILTER_DAYS_OF_WEEK = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = None
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington?\n").lower()
        if city not in CITY_DATA.keys():
            print("\nWe only support exploring data for Chicago, New York City, or Washington. Please try again.\n")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)

    print("\n")
    filter_option = None
    while True:
        filter_option = input("Would you like to filter the data by month, day, both or none?\n").lower()
        if filter_option not in ["month", "day", "both", "none"]:
            print("\nInvalid input. Please try again.\n")
            continue
        else:
            break
    
    
    month = None

    if filter_option in ["month", "both"]:
        print("\n")
        
        while True:
            month = input("Which month - January, February, March, April, May, June or all?\n").lower()
            if month not in FILTER_MONTHS and month != 'all':
                print("\nThe input month is invalid. Please try again.\n")
                continue
            else:
                break


    # get user input for day of week (all, monday, tuesday, ... sunday)

    day = None
    if filter_option in ["day", "both"]:
        print("\n")
        
        while True:
            day = input("Which day do you want to filter - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all?\n").lower()
            if day not in FILTER_DAYS_OF_WEEK and day != 'all':
                print("\nThe input day is invalid. Please try again.\n")
                continue
            else:
                break


    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # do data filter by month
    if month and month != 'all':
        filter_month = FILTER_MONTHS.index(month) + 1

        df = df[df['month'] == filter_month]

    # do data filter by day of week
    if day and day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour

    # display the most common month
    popular_month = df['month'].mode()[0]
    print(f'Most common month: {FILTER_MONTHS[popular_month -1].title()}')

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print(f'Most common day of week: {FILTER_DAYS_OF_WEEK[popular_day].title()}')

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print(f'Most common hour: {popular_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().idxmax()
    print(f'Most common start station: {popular_start_station}')

    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts().idxmax()
    print(f'Most common end station: {popular_end_station}')

    # display most frequent combination of start station and end station trip
    popular_trip = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('Most frequent combination of start station and end station trip\n')
    print(popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum() / 3600.0
    print(f'Total travel time in hour: {total_duration}')

    # display mean travel time
    mean_duration = df['Trip Duration'].mean() / 3600.0
    print(f'Mean travel time in hour: {mean_duration}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_count = df['User Type'].value_counts()
    print(f'Counts of user types:\n{user_types_count}')
    print("\n")

    if city != 'washington':
        # Display counts of gender
        user_genders_count = df['Gender'].value_counts()
        print(f'Counts of user genders:\n{user_genders_count}')
        print("\n")

        # Display earliest, most recent, and most common year of birth
        earliest_year_of_birth = int(df['Birth Year'].min())
        latest_year_of_birth = int(df['Birth Year'].max())
        most_common_year_of_birth = int(df['Birth Year'].value_counts().idxmax())

        print(f'Earliest year of birth: {earliest_year_of_birth}')
        print(f'Latest year of birth: {latest_year_of_birth}')
        print(f'Most common year of birth: {most_common_year_of_birth}')
        print("\n")

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def show_raw_data(df):
    """Displays raw data on bikeshare. 5 more rows for each press"""
    option = input("Would you like to see raw data? - Yes/Enter or No\n").lower()
    x = 0
    while option != "no":
        x += 5
        print(df.head(x))
        option = option = input("Would you like to see raw data? - Yes/Enter or No\n").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
