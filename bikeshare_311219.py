import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

# global definitions
city_bike = ['chicago', 'new york city', 'washington']
month_bike = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
day_bike = ['monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday', 'all']
Month_dict = {1: 'january', 2: 'february',
              3: 'march', 4: 'april', 5: 'may', 6: 'june'}  # Dictionary for giving the month name instead of index
choice_list = ['yes', 'no']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Udacity: TO DO: get user input for city (chicago, new york city, washington).
    # The information for the user input is printed instead of a string in the input-statement
    # (else: the string would always be printed if the user input is invalid)
    print(
        '\n*** let the exploration begin, but where? In chicago, new york city or washington?\nJust type in the name:')
    while True:
        # The user gets the opportunity to make any input for city.
        # No information string is given for the user (input()) because the info is already printed outside the loop
        # .lower() is used to avoid any invalid inputs due to large and lower case of the valid cities
        city = input().lower()
        # help from https://stackoverflow.com/questions/30267420/while-loop-to-check-for-valid-user-input
        if city not in city_bike:
            print(
                '\n*** Sorry, I didn\'t catch that city. Choose one of these: {}'.format(city_bike))

        else:
            break

    # Udacity  TO DO: get user input for month (all, january, february, ... , june)
    print(
        '\n*** please choose one month or all: january, february, march, april, may, june, all:')
    while True:
        # The user gets the opportunity to make any input for month.
        month = input().lower()
        if month not in month_bike:
            print(
                '\n*** Sorry, I didn\'t catch that month. Choose one of these: \n{}'.format(month_bike))
        else:
            break

    # Udacity TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print(
        '\n*** almost done: choose one weekday or all: monday, tuesday, wednesday, thursday, friday, saturday, sunday, all:')
    while True:
        # The user gets the opportunity to make any input for a weekday
        weekday = input().lower()
        if weekday not in day_bike:
            print(
                '\n*** Sorry, I didn\'t catch that weekday. Choose one of these:\n{}'.format(day_bike))
        else:
            break

    print('-'*40)
    return city, month, weekday


def load_data(city, month, weekday):
    """
        Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the weekday to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # Loads data for the specified city and filters by month and day if applicable.
    df = pd.read_csv(CITY_DATA[city])

    # Udacity Lösungsblock Practice Problem 3:
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and weekday from Start Time to create new columns
    # independent of user input
    df['month'] = df['Start Time'].dt.month
    # dt.weekday_name: Return a titlecased version of the weekday-string
    df['weekday'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # Udacity: use the index of the months list to get the corresponding int
        # Laura: output wird eine Funktion mit input als Argument weitergegeben. January (rechts) wird 1 (links) zugewiesen
        month = month_bike.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by weekday if applicable
    if weekday != 'all':
        # filter by weekday to create the new dataframe
        # title() must be used for the user input because the data of the new column "weekday" is titlecased (due to dt.weekday_name)
        # the new dataframe just has the data filtered by the weekday in the corresponding month of the city
        df = df[df['weekday'] == weekday.title()]

    return df


def show_data(df):
    """
    Asks user to see 5 (more) lines of raw data
    """

    print('Do you want to see 5 lines of raw data? Enter yes or no:')

    # iterating_index
    i = 0

    while True:
        # The user gets the opportunity to make any input for a weekday
        choice = input().lower()
        if choice not in choice_list:
            print(
                '\n*** Sorry, I didn\'t catch that. Choose one of these: {}'.format(choice_list))
        elif choice == 'no':
            break
        elif choice == 'yes':
            print(df.iloc[i:i+5, :])
            # iterating index is incremented after print(). first print, then increment for the next iteration if relevant
            i += 5
            print('\nWould you like to see 5 more lines ? Enter yes or no.\n')

    # no return here because the raw data is just visualized for the user instead of changing the dataframe


def drop_nan(df):
    """
    drops off the Nan values of the dataframe
    optional (decomment): 
    displays the number of NaN-values to get any idea about data quality
    helpful for coder's testing purposes
    """
    # this functions is to get a better overview over # NaN
    # just for testing purposes
    # x = df.isna().sum()
    # print('Number of NaN values:\n{}'.format(x))

    df = df.dropna(axis=0)

    # this print statement is just for validation to get a better overview after dropping
    # print('\nDataFrame after NaN-dropping: \n{}'.format(df))

    # dataframe is updated for further analysis. return is necessary
    return df


def time_stats(df):
    """
    Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')

    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    popular_month = Month_dict[popular_month].title()

    print('Most frequent month of bike travel: {}'.format(popular_month))

    # TO DO: display the most common weekday
    popular_weekday = df['weekday'].mode()[0]
    print('Most frequent weekday of bike travel: {}'.format(popular_weekday))

    # TO DO: display the most common start hour
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]

    print('Most frequent Start Hour: {}'.format(popular_hour))


    print("\nThis took {} seconds.".format(
        round(time.time() - start_time, 4)))
    print('-'*40)

    # no return here because the same dataframe after NaN-dropping is used for analysis


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print('Most commonly used start station: {}'.format(popular_start))

    # TO DO: display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print('Most commonly used end station: {}'.format(popular_end))

    # TO DO: display most frequent combination of start station and end station trip
    # help from https://stackoverflow.com/questions/53037698/how-can-i-find-the-most-frequent-two-column-combination-in-a-dataframe-in-python
    popular_route = df.groupby(
        ['Start Station', 'End Station']).size().idxmax()
    print('Most commonly used biking route: {}'.format(popular_route))

    print("\nThis took {} seconds.".format(
        round(time.time() - start_time, 4)))
    print('-'*40)

    # no return here because the same dataframe after NaN-dropping is used for analysis


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    tot_time = df['Trip Duration'].sum()
    # {:,}: this turns the total time into a thousands-mark decimal
    print('The total travel time: {:,} seconds'.format(round(tot_time, 4)))

    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('The mean travel time: {:,} seconds'.format(round(mean_time, 4)))

    print("\nThis took {} seconds.".format(
        round(time.time() - start_time, 4)))
    print('-'*40)

    # no return here because the same dataframe after NaN-dropping is used for analysis


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats... Let\'s get an overview over:\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Number per user type:\n{}'.format(user_types))

    if city != 'washington':
        # TO DO: Display counts of gender
        gender = df['Gender'].value_counts()
        print('\nNumber per gender:\n{}'.format(gender))

        # TO DO: Display earliest, most recent, and most common year of birth
        earliest_yearbirth = int(df['Birth Year'].min())
        print('\nThe oldest bike user was born in: {}'.format(earliest_yearbirth))
        latest_yearbirth = int(df['Birth Year'].max())
        print('The youngest bike user was born in: {}'.format(latest_yearbirth))
        most_yearbirth = int(df['Birth Year'].mode()[0])
        print('Most common year of birth is: {}'.format(most_yearbirth))

        print("\nThis took {} seconds.".format(
            round(time.time() - start_time, 4)))
        print('-'*40)
    else:
        print('\nSorry dude, we don\'t have any information about gender and year of birth of washington\'s bikers')

    # no return here because the same dataframe after NaN-dropping is used for analysis


def main():

    while True:
        # city, month, weekday = get_filters()
        # default values for faster testing of analysis-functions
        city = 'washington'
        month = 'all'
        weekday = 'all'

        # print filters for an user's overview
        print('\n*** your filters: {} (city), {} (month in 2017), {} (weekday)\n'.format(city,
                                                                                         month, weekday))
        # update the dataframe. The huge dataframe is reduced by relevant city, month, weekday:
        df = load_data(city, month, weekday)
        show_data(df)
        # update the dataframe. NaN are dropped off
        df = drop_nan(df)

        print('-'*40, '\nAlright, let\'s get started with the analysis.')

        start_time = time.time()
        # no update of dataframe necessary because the same dataframe is used for different analysis. the dataframe is not changed after an analysis.
        time_stats(df)
        # no update of dataframe necessary because the same dataframe is used for different analysis. the dataframe is not changed after an analysis.
        station_stats(df)
        # no update of dataframe necessary because the same dataframe is used for different analysis. the dataframe is not changed after an analysis.
        trip_duration_stats(df)
        # no update of dataframe necessary because the same dataframe is used for different analysis. the dataframe is not changed after an analysis.
        user_stats(df, city)

        print("\nThis analysis took in total {} seconds.\n".format(
            round(time.time() - start_time, 4)), '-'*40)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
