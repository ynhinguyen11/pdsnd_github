import time
import pandas as pd
import numpy as np
import sys as sys


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('-'*40)
    print('\nHello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("\nDo you want to analyze data from Chicago, New York City, or Washington? \n").lower()
    # Check if city is valid
    while CITY_DATA.get(city) is None:
        # Check if user want to continue
        contyn = input("Sorry. I can't find your city. Do you want to continue? Y/N \n").lower()
        if contyn != "y" and contyn != "yes":
            # Reference sys.exit() for stopping code: https://pythonguides.com/python-exit-command/#:~:text=exit()%20commands.-,Python%20quit()%20function,be%20used%20in%20the%20interpreter.
            sys.exit()
        else:
            city = input("Do you want to analyze data from Chicago, New York City, or Washington? \n").lower()

    # Get user filter type for data (month, day, both, or none)
    filter_type = {"month": {"january", "february", "march", "april",
                            "may", "june", "all"},
                  "day": ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"],
                  "both": ["january", "february", "march", "april",
                            "may", "june", "all", "monday", "tuesday",
                           "wednesday", "thursday", "friday", "saturday", "sunday"],
                  "none": ":"}
    filter_input = input("\nWould you like to filter {}'s data by month, day, both, or not at all? Type \"none\" for no time filter.\n"
                         .format(city.title())).lower()
    # Check if filter type is valid
    while filter_type.get(filter_input) is None:
        # Check if user want to continue
        contyn = input("Sorry. I don't understand. Do you want to continue? Y/N \n").lower()
        if contyn != "y" and contyn != "yes":
            sys.exit()
        else:
            filter_input = input("Would you like to filter {}'s data by month, day, both, or not at all? Type \"none\" for no time filter.\n"
                                 .format(city.title())).lower()

    # Get user input for month (all, january, february, ... , june)
    if filter_input == "both" or filter_input == "month":
        month = input("\nWhich month - January, February, March, April, May, June, or all?\n").lower()
        while month not in filter_type[filter_input]:
            # Check if user want to continue
            contyn = input("Sorry. I can't find the month you want. Do you want to continue? Y/N \n").lower()
            if contyn != "y" and contyn != "yes":
                sys.exit()
            else:
                month = input("Which month - January, February, March, April, May, June, or all?\n").lower()
    else:
        month = 0

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    if filter_input == "both" or filter_input == "day":
        day = input("\nWhich day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all?\n").lower()
        while day not in filter_type[filter_input]:
            # Check if user want to continue
            contyn = input("Sorry. I can't find the day you want. Do you want to continue? Y/N \n").lower()
            if contyn != "y" and contyn != "yes":
                sys.exit()
            else:
                day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday, or all?\n").lower()
    else:
        day = 0

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

    # Date time conversion and filter concept
    # Source: https://towardsdatascience.com/working-with-datetime-in-pandas-dataframe-663f7af6c587 & practice #3 solution
    df = pd.read_csv(CITY_DATA[city])
    # Convert start and end time from str to date time type
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # Created month and weekday column for filtering
    df["months"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.weekday_name
    df = df.set_index(["months","day_of_week"], drop=False)
    # Created Start & End Station concat column for easier calculation
    df['start_end_stations'] = df['Start Station'] + " to " + df['End Station']
    #Convert month name to number
    months_dic = {"january": 1,
                 "february": 2,
                 "march": 3,
                 "april": 4,
                 "may": 5,
                 "june": 6}
    if month != 0 and month != "all":
        month_num = months_dic.get(month.lower())
    # Sort data to avoid UnsortedIndexError due to multi-index during day sort
    # Source: https://pandas.pydata.org/pandas-docs/stable/user_guide/advanced.html#sorting-a-multiindex
    df = df.sort_index()
    # Filter data based on month and weekday
    if month == 0 and (day != 0 and day != "all"):
        # Source: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html last example
        df = df.loc[(1,day.title()):(6,day.title()),:]
    elif (month != 0 and month != "all") and day == 0:
        df = df.loc[(month_num, "Monday"):(month_num, "Sunday"),:]
    elif (month == 0 or month == "all") and (day == 0 or day == "all"):
        df = df.dropna(subset=['Start Time'])
    else:
        df = df.loc[month_num,day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    # Reference Dan Allan comment to get mode https://stackoverflow.com/questions/21082671/find-and-select-the-most-frequent-data-of-column-in-pandas-dataframe
    # Reference: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.mode.html
    # Reference pandas series example to change number to month name: https://www.studytonight.com/python-howtos/how-to-get-month-name-from-month-number-in-python
    # Used .value_count() to confirm code gives correct number
    print("Most common month: " + df['Start Time'].dt.month_name().mode()[0])

    # Display the most common day of week
    print("Most common day of week: " + df.day_of_week.mode()[0])

    # Display the most common start hour
    print("Most common start hour: " + str(df['Start Time'].dt.hour.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print("Most common start station: " + df['Start Station'].mode()[0])

    # Display most commonly used end station
    print("Most common end station: " + df['End Station'].mode()[0])

    # Display most frequent combination of start station and end station trip
    print("Most common start to end station trip: " + (df['Start Station'] + " to " + df['End Station']).mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating most popular trip duration in {} on {} from {}...\n'.format(df['Start Time'].dt.month_name().mode()[0],
                                                                                    df.day_of_week.mode()[0],
                                                                                    (df['Start Station'] + " to " + df['End Station']).mode()[0]))
    start_time = time.time()

    # Display total travel time
    # Create new dataframe with most common stations combo, month, weekday, and hour filtered out to calculate trip duration
    duration_df = df.loc[(df['months'] == df['months'].mode()[0]) &
                 (df['start_end_stations'] == (df['Start Station'] + " to " + df['End Station']).mode()[0]) &
                 (df['day_of_week'] == df.day_of_week.mode()[0]),:]
    # Display only max and min total travel time if there are multiple travel time to calculate
    if duration_df['Start Time'].count() > 1:
        print("There are more than one trip to calculate total travel time so only the maximum and minimum total travel time will be calculated.")
        print("\nTotal travel time (min): " + str(duration_df['Trip Duration'].min()) +
              "\nTotal travel time (max): " + str(duration_df['Trip Duration'].max()))
    elif duration_df['Start Time'].count() == 0:
        print("No data for trip in {} on {}.".format(df['Start Time'].dt.month_name().mode()[0],df.day_of_week.mode()[0]))
    else:
        print("Total travel time: " + str(df['Trip Duration'][0]))

    # Display mean travel time
    if duration_df['Start Time'].count() > 0:
        print("Average travel time: " + str(df['Trip Duration'].mean()))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    # Create dataframe to hold user type count
    # Reference for count: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.value_counts.html#pandas.DataFrame.value_counts
    # Reference #8 & #4 for sorting and changing value count to dataframe: https://re-thought.com/pandas-value_counts/
    user_type_df = df['User Type'].value_counts().to_frame()
    for user_type in user_type_df.index:
        print(user_type + " Counts: " + str(user_type_df.loc[user_type,'User Type']))
    # Display counts of gender
    # Check if Gender column exists
    if 'Gender' in df.columns.values:
        # Create dataframe to hold gender count
        gender_df = df['Gender'].value_counts(dropna=False).sort_index(ascending=False).to_frame()
        for gender_type in gender_df.index:
            # Reference Sven Marnach comment on how to check for string: https://stackoverflow.com/questions/4843173/how-to-check-if-type-of-a-variable-is-string
            if isinstance(gender_type, str):
                print(gender_type + " counts: " + str(gender_df.loc[gender_type,'Gender']))
            else:
                print("Gender Omitted Counts: " + str(gender_df.loc[gender_type,'Gender']))
    else:
        print("No gender data available.")
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns.values:
        print("The earliest birth year: " + str(int(df['Birth Year'].min())))
        print("The most recent birth year: " + str(int(df['Birth Year'].max())))
        # Create string of birth year in case more than one common year
        year_str = ""
        for year in df['Birth Year'].mode():
            if year == df['Birth Year'].mode()[0]:
                year_str = str(int(year))
            elif year == df['Birth Year'].mode()[df['Birth Year'].mode().last_valid_index()]:
                year_str = year_str + " & " + str(int(year))
            else:
                year_str = year_str + ", " + str(int(year))
        print("The most common birth year: " + year_str)
    else:
        print("No birth year data available.")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Ask and display 5 individual bikeshare user's data if prompted."""
    # Ask if user want to see raw data
    data_disp = input('\nWould you like to view individual trip data? Enter yes or no.\n').lower()
    # Check if answer is valid
    while data_disp != "yes" and data_disp != "y" and data_disp != "no" and data_disp != "n":
        # Check if user want to continue
        contyn = input("Sorry. I don't understand. Do you want to continue? Y/N \n").lower()
        if contyn != "y" and contyn != "yes":
            sys.exit()
        else:
            data_disp = input('\nWould you like to view individual trip data? Enter yes or no.\n').lower()
    # Check if user wants to continue
    if data_disp != "y" and data_disp != "yes":
        return
    # Create loop to show data in group of 5
    l = 0
    for u in np.arange(5, df['Start Time'].count() + 5, 5):
        x = 5
        # Check if data range is greater than count
        if u > df['Start Time'].count():
            u = df['Start Time'].count() + 1
            x = u%5
        # Create loop to display data
        for i in np.arange(0, x):
            if 'Gender' in df.columns.values:
                print("\n{Id: " + str(df[l:u].loc[:,'Unnamed: 0'][i]) +
                      "\n Birth Year: " + str(df[l:u].loc[:,'Birth Year'][i]) +
                      "\n Gender: " +  str(df[l:u].loc[:,'Gender'][i]) +
                      "\n Start Time: " + str(df[l:u].loc[:,'Start Time'][i]) +
                      "\n End Time: " + str(df[l:u].loc[:,'End Time'][i]) +
                      "\n Trip Duration: " + str((df[l:u].loc[:,'Trip Duration'][i])) +
                      "\n Start Station: " +  str(df[l:u].loc[:,'Start Station'][i]) +
                      "\n End Station: " +  str(df[l:u].loc[:,'End Station'][i]) + "}")
            else:
                print("\n{Id: " + str(df[l:u].loc[:,'Unnamed: 0'][i]) +
                      "\n Birth Year: NaN" +
                      "\n Gender: NaN" +
                      "\n Start Time: " + str(df[l:u].loc[:,'Start Time'][i]) +
                      "\n End Time: " + str(df[l:u].loc[:,'End Time'][i]) +
                      "\n Trip Duration: " + str((df[l:u].loc[:,'Trip Duration'][i])) +
                      "\n Start Station: " +  str(df[l:u].loc[:,'Start Station'][i]) +
                      "\n End Station: " +  str(df[l:u].loc[:,'End Station'][i]) + "}")
        l = u
        # Check if last data group
        if u == df['Start Time'].count() + 1:
            print("\nNo more data to show ...")
            return
        # Ask if user want to see raw data
        data_disp = input('\nWould you like to view individual trip data? Enter yes or no.\n').lower()
        # Check if answer is valid
        while data_disp != "yes" and data_disp != "y" and data_disp != "no" and data_disp != "n":
            # Check if user want to continue
            contyn = input("Sorry. I don't understand. Do you want to continue? Y/N \n").lower()
            if contyn != "y" and contyn != "yes":
                sys.exit()
            else:
                data_disp = input('\nWould you like to view individual trip data? Enter yes or no.\n').lower()
        if data_disp != "y" and data_disp != "yes":
            return
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)


        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes' and restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
