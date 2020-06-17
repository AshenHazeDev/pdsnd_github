import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # The section gathers user input for the city to be investigated and rejects all invalid entries.


    while True:
        try:
            city = input('Please enter a city (Chicago, New York City or Washington): ').lower()
        except:
            print('\nPlease enter a valid entry. \n')
            continue
        if city in CITY_DATA:
            break
        else:
            print('\nPlease enter a valid entry. \n')
            continue


    # This section gets the month or all filter and rejects any invalid entries.
    while True:
        try:
            month = input('Please enter a month (all, january, february, ... , june): ').lower()
        except:
            print('\nPlease enter a valid entry. \n')
            continue
        if month in months:
            break
        elif month == 'all':
            break
        else:
            print('\nPlease enter a valid entry. \n')
            continue

    # This collects the day filter and rejects invalid input.
    while True:
        try:
            day = input('Please enter a month (all, monday, tuesday, ... sunday): ').lower()
        except:
            print('\nPlease enter a valid entry. \n')
            continue
        if day in days:
            break
        elif day == 'all':
            break
        else:
            print('\nPlease enter a valid entry. \n')
            continue


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

    # loads the appropriate csv based off of the user's selection
    df = pd.read_csv(CITY_DATA[(city)])

    # converts the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extracts month, day and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day of week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour

    # creates trip collumn for most common overall trip
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']

    # filter by month unless user inputted all
    if month != 'all':
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        day = days.index(day)
        df = df[df['day of week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()


    print('The most common month is: ', list(df['month'].mode()))

    print('The most common day of the week is: ', list(df['day of week'].mode()))

    print('The most common start hour is: ', list(df['hour'].mode()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('The most common start station is: ', list(df['Start Station'].mode()))
    print('The most common end station is: ', list(df['End Station'].mode()))
    print('The most common combination of start and end station is: ', list(df['trip'].mode()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Sums total trip duration and then creates days, hours, minutes and seconds variables
    totaltravel = int(df['Trip Duration'].sum())
    tdays = totaltravel // 86400
    thours = (totaltravel - (tdays * 86400)) // 3600
    tminutes = (totaltravel - (tdays * 86400) - (thours * 3600)) // 60
    tseconds = (totaltravel - (tdays * 86400) - (thours * 3600)) % 60

    print('The total travel time for this time range is {} days, {} hours, {} minutes and {} seconds.'.\
          format(tdays, thours, tminutes, tseconds))
    print('The average travel time is {} seconds'.format(int(df['Trip Duration'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print(df['User Type'].value_counts(), '\n')

    # ensures data set has the gender column or skips
    if 'Gender' in df.columns:

        print(df['Gender'].value_counts())
    else:
        print('Unable to calculate gender counts, this city does not collect that information.')

    # ensures data set has birth year or skips
    if 'Birth Year' in df.columns:
        print(' The earliest birth year is: {}\n The most recent is: {} \n The most common birth year is: {}' .\
            format(df['Birth Year'].min(), df['Birth Year'].max() , list(df['Birth Year'].mode())))
    else:
        print('Unable to provide birth year data. This city does not collect that information.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Offers to display the raw data 5 lines at a time """

    rawdata = 'yes'
    lcount = 0
    llimit = len(df)
    print('\nThere are {} rows in this data frame.'.format(llimit))


    # Loop to keep querying if more data needs to be displayed
    while rawdata == 'yes':
        rawdata = input('\nWould you like to see 5 lines of the raw data? Enter yes or no.\n')
        if rawdata != 'yes':
            break
        # Checks to see if we've reached or exceeded the length of the data frame and ends the loop at the correct point
        if (lcount + 5) < llimit:
            print(df.iloc[lcount:(lcount + 5)])
            lcount = lcount + 5
        elif (lcount + 5) == llimit:
            print(df.iloc[lcount:(lcount + 5)])
            break
        else:
            print(df.iloc[lcount:llimit])
            break

def main():
    while True:
        city, month, day = get_filters()
        print('You chose {}, {}, {}'.format(city, month, day))
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
