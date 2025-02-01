import openpyxl
print(openpyxl.__version__)
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

df = pd.read_csv('28230.csv')

df.head(60)

print(df.head(100))

print(df.tail(100))

print(df['Speed(km/h)'])  # speed column

print(df[['Time', 'Speed(km/h)']])  

# Combine Date and Time into a single datetime column with specified format  
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%y %H:%M:%S')  

filtered_whole_time = df['Datetime']
filtered_whole_speed = df['Speed(km/h)']

# Step 1: Strip extra spaces from column names
df.columns = df.columns.str.strip()

# Step 4: Calculate start time, end time, and total journey time
start_time = df['Datetime'].min()
end_time = df['Datetime'].max()
print(f"Start time of whole journey: {start_time}")
print(f"End time of whole journey: {end_time}")

total_time = end_time - start_time  # Calculate the duration
print(f"Total journey time: {total_time}")


total_distance = df['Distance(km)'].max() - df['Distance(km)'].min()
print(f"Total journey distance: {total_distance:.2f} km")

# Step 6: Convert total_time to hours
total_time_hours = total_time.total_seconds() / 3600  # Convert seconds to hours
print(f"Total time in hours: {total_time_hours}")

max_speed = df['Speed(km/h)'].max()
print(f"Maximum Speed/MPS Achieved : {max_speed} km/h")

min_speed = df['Speed(km/h)'].min()
print(f"Minimum Speed: {min_speed} km/h")

avg_run_speed = df['Speed(km/h)'].mean()
print(f"Average running speed : {avg_run_speed} km/h")

avg_speed = total_distance / total_time_hours
print(f"Average Speed: {avg_speed:.2f} km/h")

#number of times maximum speed happened 
count_max_speed = (df['Speed(km/h)'] == max_speed).sum()
print(f"  {count_max_speed} ")

df.columns = df.columns.str.strip()

# Combine Date and Time into a single datetime column with specified format  
df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%y %H:%M:%S')  

import matplotlib.pyplot as plt
import pandas as pd

# Assuming df is already loaded and contains 'Datetime' and 'Speed(km/h)' columns
filtered_whole_time = df['Datetime']
filtered_whole_speed = df['Speed(km/h)']

# First plot: Speed vs Time (Bar Plot)
plt.figure(figsize=(12, 6))
plt.bar(filtered_whole_time, filtered_whole_speed, width=0.001)
plt.title("Speed VS Time (Whole Time)")
plt.xlabel('Time')
plt.ylabel('Speed (KM/H)')
plt.xticks(rotation=90)
plt.grid()
plt.tight_layout()

# Function to handle key press event (closing plot on 'q')
def handle_key_1(event):
    if event.key == 'q':
        plt.close()  # Close the current plot

# Attach the event listener for the first plot
plt.gcf().canvas.mpl_connect('key_press_event', handle_key_1)

# Show the first plot
plt.show()

# Data cleaning and processing
df['Datetime'] = pd.to_datetime(df['Datetime'], errors='coerce')
print(df['Datetime'].isna().sum())
print(df['Speed(km/h)'].isna().sum())

df = df.sort_values(by='Datetime')

df['Speed(km/h)'] = pd.to_numeric(df['Speed(km/h)'], errors='coerce')
print(df['Speed(km/h)'].isna().sum())

df = df.dropna(subset=['Datetime', 'Speed(km/h)'])

# Second plot: Speed vs Time (Line Plot)
plt.figure(figsize=(15, 6))
plt.plot(df['Datetime'], df['Speed(km/h)'], color='blue')
plt.title("Speed vs Time (Whole Time)")
plt.xlabel("Time")
plt.ylabel("Speed (km/h)")

# Function to handle key press event (closing plot on 'q')
def handle_key_2(event):
    if event.key == 'q':
        plt.close()  # Close the current plot

# Attach the event listener for the second plot
plt.gcf().canvas.mpl_connect('key_press_event', handle_key_2)

# Show the second plot
plt.show()

#plotting for first 3 hours
start_time = df['Datetime'].min()
end_time = start_time+pd.Timedelta(hours=3)
filtered_df = df[(df['Datetime']>=start_time)&(df['Datetime']<=end_time)]

plt.figure(figsize= (12,5))
plt.bar(filtered_df['Datetime'],filtered_df['Speed(km/h)'],width = 0.01)
plt.title('Speed VS Time (First 3 hours)')
plt.xlabel('Time')
plt.ylabel('Speed (km/h)')
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()


# Function to handle key press event (closing plot on 'q')
def handle_key_3(event):
    if event.key == 'q':
        plt.close()  # Close the current plot

# Attach the event listener for the second plot
plt.gcf().canvas.mpl_connect('key_press_event', handle_key_3)

# Show the Third plot
plt.show()

plt.figure(figsize= (15,6))
plt.plot(filtered_df['Datetime'],filtered_df['Speed(km/h)'],color = 'red',linewidth='2',marker='o',markersize='0.1')
plt.title('Speed VS Time (First 3 hours)')
plt.xlabel('TIme')
plt.ylabel('Speed (km/h)')
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()

# Function to handle key press event (closing plot on 'q')
def handle_key_4(event):
    if event.key == 'q':
        plt.close()  # Close the current plot

# Attach the event listener for the second plot
plt.gcf().canvas.mpl_connect('key_press_event', handle_key_4)

# Show the Fourth plot
plt.show()

# Assuming df['Datetime'] is in datetime format and ready to use
end_time = df['Datetime'].max()
start_time = end_time - pd.Timedelta(hours=3)

print(start_time)
print(end_time)
# Filter for the last 3 hours
filtered_df_last_3_hours = df[(df['Datetime'] >= start_time) & (df['Datetime'] <= end_time)]

plt.figure(figsize=(12,6))
plt.bar(filtered_df_last_3_hours['Datetime'],filtered_df_last_3_hours['Speed(km/h)'],width=0.01)
plt.title("Speed vs Time for last 3 hours")
plt.xlabel('Time')
plt.ylabel('Speed (km/h)')
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()

# Function to handle key press event (closing plot on 'q')
def handle_key_5(event):
    if event.key == 'q':
        plt.close()  # Close the current plot

# Attach the event listener for the second plot
plt.gcf().canvas.mpl_connect('key_press_event', handle_key_5)

# Show the Fifth plot
plt.show()

plt.figure(figsize=(12,6))
plt.plot(filtered_df_last_3_hours['Datetime'],filtered_df_last_3_hours['Speed(km/h)'],color='red',linewidth='1.5',marker='o',markersize='0.2')
plt.title("Speed vs Time for last 3 hours")
plt.xlabel('Time')
plt.ylabel('Speed (km/h)')
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()

def handle_key_6(event):
    if event.key == 'q':
        plt.close()  # Close the current plot

# Attach the event listener for the second plot
plt.gcf().canvas.mpl_connect('key_press_event', handle_key_6)

# Show the Sixth plot
plt.show()

#defining start time and end time of whole journey
start_time = df['Datetime'].min()
end_time = df['Datetime'].max()

# printing start_time and end_time of whole journey 
print(f"Start time of whole journey is : {start_time}")
print(f"End time of whole journey is : {end_time}")

start_time = df['Datetime'].min()
end_time = df['Datetime'].min()

# Find indices where speed is 0 (stops)
stops = df[df['Speed(km/h)'] == 0]['Datetime']

# Collect the time periods of interest
time_periods = []
for stop_time in stops:
    before = stop_time - pd.Timedelta(minutes=15)
    after = stop_time + pd.Timedelta(minutes=15)
    time_periods.append((before, after))

# Create an empty DataFrame to store filtered data
filtered_data = pd.DataFrame()

# Filter for data within 15 minutes before and after each stop
for start, end in time_periods:
    filtered_subset = df[(df['Datetime'] >= start) & (df['Datetime'] <= end)]
    filtered_data = pd.concat([filtered_data, filtered_subset])

# Check if there is any data to plot
if filtered_data.empty:
    print("No data available for the specified time periods.")
else:
    # Plotting
    plt.figure(figsize=(14.5, 6))
    plt.bar(filtered_data['Datetime'], 
            filtered_data['Speed(km/h)'], 
            width=0.0001)  # Adjust width as needed
    
    # Set plot titles and labels
    plt.title("Speed vs Time: 15 minutes Before and After Stops")
    plt.xlabel('Time')
    plt.ylabel('Speed(km/h)')
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Add grid for better readability
    plt.grid()

    # Adjust layout to prevent clipping of tick labels
    # plt.tight_layout()

    # Define key press event for closing plot with 'q'
    def handle_key_7(event):
        if event.key == 'q':
            plt.close()  # Close the current plot

    # Attach the event listener for the seventh plot
    plt.gcf().canvas.mpl_connect('key_press_event', handle_key_7)

    # Show the Seventh plot
    plt.show()

# Count the number of halts  
number_of_halts = len(stops)  

# Display only the number of halts  
print(number_of_halts)


start_time = df['Datetime'].min()
end_time = start_time + pd.Timedelta(hours=1)
#print(start_time)
#print(end_time)
filtered_1_hour = df[(df['Datetime'] >= start_time) & (df['Datetime'] <= end_time)]
#print(filtered_1_hour)

plt.figure(figsize=(15,6))
plt.plot(filtered_1_hour['Datetime'],filtered_1_hour['Speed(km/h)'],color='black',linewidth='1.5',marker='o',markersize='0.2')
plt.title(" First 1 hour Analysis ")
plt.xlabel('Time')
plt.ylabel('Speed(km/h)')
plt.xticks(rotation=90)
plt.grid()
plt.tight_layout()

# Define key press event for closing plot with 'q'
def handle_key_8(event):
        if event.key == 'q':
            plt.close()  # Close the current plot

    # Attach the event listener for the seventh plot
plt.gcf().canvas.mpl_connect('key_press_event', handle_key_8)

    # Show the Seventh plot
plt.show()


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

start_time = df['Datetime'].min()
end_time = start_time + pd.Timedelta(minutes=60)

start_time = df['Datetime'].min()
end_time = start_time + pd.Timedelta(minutes=60)

# Create figure and axis
plt.figure(figsize=(15, 6))

# Plot the speed data
plt.plot(filtered_1_hour['Datetime'], filtered_1_hour['Speed(km/h)'], color='black', linewidth=1.5, marker='o', markersize=0.2)

# Title and labels
plt.title("First 1 Hour Analysis")
plt.xlabel('Time')
plt.ylabel('Speed (km/h)')

# Set x-ticks to show every minute and format to show only time
tick_positions = pd.date_range(start=start_time, end=end_time, freq='1min')
plt.xticks(tick_positions, [t.strftime('%H:%M:%S') for t in tick_positions], rotation=90)

# Add grid and tight layout

plt.tight_layout()
plt.grid()
# Show the plot

def handle_key_9(event):
        if event.key == 'q':
            plt.close()  # Close the current plot

    # Attach the event listener for the seventh plot
plt.gcf().canvas.mpl_connect('key_press_event', handle_key_9)

    
plt.show()

count_speed = (df['Speed(km/h)'] >= 95.95).sum()
print(count_speed)


# In[47]:


# Calculate total distance covered
total_distance = df['Distance(km)'].max() - df['Distance(km)'].min()

# Print the result
print(f"Total distance covered during the journey: {total_distance:.2f} km")

print(max_speed)
mps_rows = df[df['Speed(km/h)']== max_speed]
#print(mps_rows)
#print(mps_rows['Distance(km)'].max())
#print(type(mps_rows['Distance(km)'].max()))
total_mps_distance = mps_rows['Distance(km)'].max() - mps_rows['Distance(km)'].min()


print(f"Total distance at achieved MPS: {total_mps_distance:2f} km")

mps_attained = 101
near_mps_threshold = 0.95 * mps_attained

# Filter rows where speed is greater than the near-MPS threshold and create a copy
near_mps_rows = df[df['Speed(km/h)'] > near_mps_threshold].copy()

#print(near_mps_rows)


#Distance at near achieved  MPS
if near_mps_rows.empty:
    print("No distance covered at near MPS.")
else:
    
    near_mps_rows['Segment'] = (near_mps_rows['Distance(km)'].diff() > 1).cumsum()

   
    segment_distances = (
        near_mps_rows.groupby('Segment')['Distance(km)']
        .agg(lambda x: x.max() - x.min())
    )

    
    total_distance_near_mps = segment_distances.sum()
    print(f"Distance at near achieved MPS: {total_distance_near_mps:.2f} km")


#Distance at near overall MPS

df.columns = df.columns.str.strip()


mps_attained = 130  # Maximum Permissible Speed
near_mps_threshold = 0.95 * mps_attained  # 95% of MPS


near_mps_rows = df[df['Speed(km/h)'] > near_mps_threshold].copy()


if near_mps_rows.empty:
    print("No distance covered at near MPS.")
else:
   
    near_mps_rows['Segment'] = (near_mps_rows['Distance(km)'].diff() > 1).cumsum()


    segment_distances = (
        near_mps_rows.groupby('Segment')['Distance(km)']
        .agg(lambda x: x.max() - x.min())
    )


    total_distance_near_mps = segment_distances.sum()


    print(f"Distance at near overall MPS: {total_distance_near_mps:.2f} km")

    # Given values
total_expected_halts = 12

# Calculate unscheduled halts
total_unscheduled_halts = number_of_halts - total_expected_halts
print(f"Total calculated Halts : {number_of_halts} ")

print(f"Total Unscheduled Halts: {total_unscheduled_halts}")

#------s1
speed_threshold = 2  # Speed change threshold in km/h


sudden_changes = []

# Step 5: Iterate through the dataset to detect sudden speed changes
for i in range(1, len(df)):
    current_speed = df['Speed(km/h)'].iloc[i]
    previous_speed = df['Speed(km/h)'].iloc[i - 1]
    time_of_change = df['Datetime'].iloc[i]
    
    # Calculate speed change
    speed_change = abs(current_speed - previous_speed)
    
    # Check if the speed change exceeds the threshold
    if speed_change >= speed_threshold:
        # Determine if it's a sudden increase or decrease
        if current_speed > previous_speed:
            change_type = "Sudden Increase"
        else:
            change_type = "Sudden Decrease"
        
        # Record the event
        sudden_changes.append({
            'Time': time_of_change.strftime('%H:%M:%S'),
            'Previous Speed': previous_speed,
            'Current Speed': current_speed,
            'Speed Change': speed_change,
            'Change Type': change_type
        })

# Step 6: Print the results
if sudden_changes:
    print("Sudden Speed Changes:")
    for change in sudden_changes:
        print(f"Time: {change['Time']}, Previous Speed: {change['Previous Speed']} km/h, Current Speed: {change['Current Speed']} km/h, Speed Change: {change['Speed Change']} km/h, Change Type: {change['Change Type']}")
else:
    print("No sudden speed changes detected.")  

#-------s2



speed_threshold = 2 

sudden_changes = []

for i in range(1, len(df)):
    current_speed = df['Speed(km/h)'].iloc[i]
    previous_speed = df['Speed(km/h)'].iloc[i - 1]
    time_of_change = df['Datetime'].iloc[i]
    
   
    speed_change = abs(current_speed - previous_speed)
    

    if speed_change >= speed_threshold:
      
        if current_speed > previous_speed:
            change_type = "Sudden Increase"
            marker_color = 'green'  
        else:
            change_type = "Sudden Decrease"
            marker_color = 'red'  
        
      
        sudden_changes.append({
            'Time': time_of_change,
            'Previous Speed': previous_speed,
            'Current Speed': current_speed,
            'Speed Change': speed_change,
            'Change Type': change_type,
            'Marker Color': marker_color
        })

if sudden_changes:
    print("Sudden Speed Changes:")
    for change in sudden_changes:
        print(f"Time: {change['Time'].strftime('%H:%M:%S')}, Previous Speed: {change['Previous Speed']} km/h, Current Speed: {change['Current Speed']} km/h, Speed Change: {change['Speed Change']} km/h, Change Type: {change['Change Type']}")
else:
    print("No sudden speed changes detected.")

#----plot-sudden

# Step 3: Define speed threshold for sudden changes
speed_threshold = 2  # Speed change threshold in km/h

# Step 4: Initialize a list to store sudden speed changes
sudden_changes = []

# Step 5: Iterate through the dataset to detect sudden speed changes
for i in range(1, len(df)):
    current_speed = df['Speed(km/h)'].iloc[i]
    previous_speed = df['Speed(km/h)'].iloc[i - 1]
    time_of_change = df['Datetime'].iloc[i]
    
    # Calculate speed change
    speed_change = abs(current_speed - previous_speed)
    
    # Check if the speed change exceeds the threshold
    if speed_change >= speed_threshold:
        # Determine if it's a sudden increase or decrease
        if current_speed > previous_speed:
            change_type = "Sudden Increase"
        else:
            change_type = "Sudden Decrease"
        
        # Record the event
        sudden_changes.append({
            'Time': time_of_change.strftime('%H:%M:%S'),
            'Previous Speed': previous_speed,
            'Current Speed': current_speed,
            'Speed Change': speed_change,
            'Change Type': change_type
        })

# Step 6: Print the results
if sudden_changes:
    print("Sudden Speed Changes:")
    for change in sudden_changes:
        print(f"Time: {change['Time']}, Previous Speed: {change['Previous Speed']} km/h, Current Speed: {change['Current Speed']} km/h, Speed Change: {change['Speed Change']} km/h, Change Type: {change['Change Type']}")
else:
    print("No sudden speed changes detected.")

# Step 7: Prepare data for the stacked bar graph
if sudden_changes:
    times = [change['Time'] for change in sudden_changes]
    previous_speeds = [change['Previous Speed'] for change in sudden_changes]
    current_speeds = [change['Current Speed'] for change in sudden_changes]
"""
    # Step 8: Plot the stacked bar graph
    plt.figure(figsize=(12, 6))

    # Plot previous speed as the bottom bar
    plt.bar(times, previous_speeds, label='Previous Speed', color='blue')

    # Plot current speed as the top bar (stacked on previous speed)
    plt.bar(times, current_speeds, bottom=previous_speeds, label='Current Speed', color='orange')

    # Add labels, title, and legend
    plt.xlabel('Time')
    plt.ylabel('Speed (km/h)')
    plt.title('Stacked Bar Graph of Sudden Speed Changes')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.legend()
    plt.grid(True)
    plt.tight_layout()  # Adjust layout to prevent overlapping
    # Define key press event for closing plot with 'q'
    def handle_key_10(event):
        if event.key == 'q':
            plt.close()  # Close the current plot

    # Attach the event listener for the seventh plot
    plt.gcf().canvas.mpl_connect('key_press_event', handle_key_10)

    # Show the tenth plot
    #plt.show()
else:
    print("No data to plot.")
"""

#------Graph Sudden increase
# Filter sudden_changes to include only sudden increases
sudden_increases = [change for change in sudden_changes if change['Change Type'] == "Sudden Increase"]
print(len(sudden_increases))

if sudden_increases:
   
    times = [change['Time'] for change in sudden_increases]
    previous_speeds = [change['Previous Speed'] for change in sudden_increases]
    current_speeds = [change['Current Speed'] for change in sudden_increases]

    
    plt.figure(figsize=(12, 6))  

    
    plt.plot(times,current_speeds,label='Current Speed',color='green',linewidth='2')
    plt.plot(times,previous_speeds,label='Previous Speed',color='red',linewidth='2')

    #plt.plot(previous_speeds,linewidth='1',marker='o',markersize='0.2')
    #plt.plot(previous_speeds,linewidth='1',marker='o',markersize='0.2')
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Speed (km/h)', fontsize=12)
    plt.title('Graph of Sudden Increases', fontsize=14)
    plt.xticks(rotation=90, fontsize=10) 
   # plt.yticks(fontsize=10)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6) 

 
    plt.tight_layout()


    # Define key press event for closing plot with 'q'
    def handle_key_11(event):
        if event.key == 'q':
            plt.close()  # Close the current plot

    # Attach the event listener for the seventh plot
    plt.gcf().canvas.mpl_connect('key_press_event', handle_key_11)

    # Show the tenth plot
    plt.show()
else:
    print("No sudden increases detected.")



# Filter sudden_changes to include only sudden increases
sudden_increases = [change for change in sudden_changes if change['Change Type'] == "Sudden Increase"]
print(len(sudden_increases))

if sudden_increases:
    # Extract data
    times = [change['Time'] for change in sudden_increases]
    previous_speeds = [change['Previous Speed'] for change in sudden_increases]
    current_speeds = [change['Current Speed'] for change in sudden_increases]

    # Create scatter plot
    plt.figure(figsize=(12, 6))  

    # Plot current speeds
    plt.scatter(times, current_speeds, label='Current Speed', color='green', s=20) 
    # Plot previous speeds
    plt.scatter(times, previous_speeds, label='Previous Speed', color='red', s=20)

    # Add labels and title
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Speed (km/h)', fontsize=12)
    plt.title('Scatter Plot of Sudden Increases', fontsize=14)
    plt.xticks(rotation=90, fontsize=10) 
    plt.legend(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6) 

    # Adjust layout
    plt.tight_layout()

    def handle_key_12(event):
        if event.key == 'q':
            plt.close()  # Close the current plot

    # Attach the event listener for the seventh plot
    plt.gcf().canvas.mpl_connect('key_press_event', handle_key_12)

    # Show the tenth plot
    plt.show()
else:
    print("No sudden increases detected.")


# Filter sudden_changes to include only sudden decreases
sudden_decreases = [change for change in sudden_changes if change['Change Type'] == "Sudden Decrease"]
print(len(sudden_decreases))
# Check if there are sudden increases
if sudden_decreases:
    # Extract data for the plot
    times = [change['Time'] for change in sudden_decreases]
    previous_speeds = [change['Previous Speed'] for change in sudden_decreases]
    current_speeds = [change['Current Speed'] for change in sudden_decreases]

    # Create the plot
    plt.figure(figsize=(12, 6))  # Adjusted figure size for better readability

    # Plot previous speed
    plt.plot(times, previous_speeds, label='Previous Speed', color='red', linewidth=2, marker='o', markersize=3)

    # Plot current speed
    plt.plot(times, current_speeds, label='Current Speed', color='green', linewidth=2, marker='o', markersize=3)


    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Speed (km/h)', fontsize=12)
    plt.title('Sudden Decrease in Speed', fontsize=14)
    plt.xticks(rotation=90, fontsize=10) 
   # plt.yticks(fontsize=10)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6) 

 
    plt.tight_layout()


    def handle_key_13(event):
        if event.key == 'q':
            plt.close()  # Close the current plot

    # Attach the event listener for the seventh plot
    plt.gcf().canvas.mpl_connect('key_press_event', handle_key_13)

    # Show the tenth plot
    plt.show()
else:
    print("No sudden decreases detected.")


#BFT and BPT

import pandas as pd

def analyze_brake_tests(filename):
    # Read the CSV file
    df = pd.read_csv(filename)
    
    # Initialize variables for Brake Feel Test
    brake_feel_max_speed = 15
    brake_feel_min_speed = 10
    brake_feel_time = None
    brake_feel_max_index = 0  # To store the index where max speed is found

    # Main loop for Brake Feel Test (to find max speed)
    for i in range(len(df) - 1):
        current_speed = df.loc[i, 'Speed(km/h)']
        next_speed = df.loc[i + 1, 'Speed(km/h)']
        current_time = df.loc[i, 'Time']
        
        # Find max speed
        if current_speed >= brake_feel_max_speed and next_speed < current_speed:
            brake_feel_max_speed = current_speed
            brake_feel_time = current_time
            brake_feel_max_index = i  # Store the index where max speed is found
            break
    
    # Find min speed for BFT (start from where max speed was found)
    for i in range(brake_feel_max_index, len(df) - 1):
        current_speed = df.loc[i, 'Speed(km/h)']
        next_speed = df.loc[i + 1, 'Speed(km/h)']
        
        # Find min speed
        if current_speed <= brake_feel_min_speed and next_speed > current_speed:
            brake_feel_min_speed = current_speed
            break
            
    # Initialize variables for Brake Power Test
    brake_power_max_speed = 60
    brake_power_min_speed = 31
    brake_power_time = None
    brake_power_max_index = 0  # To store the index where max speed is found

    # Main loop for Brake Power Test (to find max speed)
    for i in range(len(df) - 1):
        current_speed = df.loc[i, 'Speed(km/h)']
        next_speed = df.loc[i + 1, 'Speed(km/h)']
        current_time = df.loc[i, 'Time']
        
        # Find max speed
        if current_speed > brake_power_max_speed and next_speed < current_speed:
            brake_power_max_speed = current_speed
            brake_power_time = current_time
            brake_power_max_index = i  # Store the index where max speed is found
            break
    
    # Find min speed for BPT (start from where max speed was found)
    for i in range(brake_power_max_index, len(df) - 1):
        current_speed = df.loc[i, 'Speed(km/h)']
        next_speed = df.loc[i + 1, 'Speed(km/h)']
        
        # Find min speed
        if current_speed <= brake_power_min_speed and next_speed > current_speed:
            brake_power_min_speed = current_speed
            break
            
    # Output results
    print(f"\n\nBFT\nSpeed drop: max speed - min speed -> {brake_feel_max_speed} - {brake_feel_min_speed}\nTime: {brake_feel_time}")
    print(f"BPT\nSpeed drop: max speed - min speed -> {brake_power_max_speed} - {brake_power_min_speed}\nTime: {brake_power_time}")

# Example usage
filename = '28230.csv'  # Replace with the actual file path
analyze_brake_tests(filename)


import matplotlib
import matplotlib.pyplot as plt

# Print Matplotlib version
#print("Matplotlib Version : {}".format(matplotlib.__version__))

# Define colors and values for the speed ranges
colors = ['#4dab6d']
values = [140, 120, 100, 80, 60, 40, 20, 0]  # Speed ranges

# Define x-axis positions for the bars
x_axis_vals = [0, 0.44, 0.88, 1.32, 1.76, 2.2, 2.64]

# Create the polar chart
fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(projection="polar")

# Plot the bars for speed ranges
ax.bar(x=x_axis_vals, width=0.5, height=0.5, bottom=2,
       linewidth=3, edgecolor="white",
       color=colors, align="edge")

# Add labels for speed ranges
plt.annotate("140+ km/h", xy=(0.16, 2.1), rotation=-75, color="white", fontweight="bold")
plt.annotate("120 km/h", xy=(0.65, 2.08), rotation=-55, color="white", fontweight="bold")
plt.annotate("100 km/h", xy=(1.14, 2.1), rotation=-32, color="white", fontweight="bold")
plt.annotate("80 km/h", xy=(1.62, 2.2), color="white", fontweight="bold")
plt.annotate("60 km/h", xy=(2.08, 2.25), rotation=20, color="white", fontweight="bold")
plt.annotate("40 km/h", xy=(2.46, 2.25), rotation=45, color="white", fontweight="bold")
plt.annotate("20 km/h", xy=(3.0, 2.25), rotation=75, color="white", fontweight="bold")

# Add speed values to the chart
for loc, val in zip([0, 0.44, 0.88, 1.32, 1.76, 2.2, 2.64, 3.14], values):
    plt.annotate(val, xy=(loc, 2.5), ha="right" if val <= 60 else "left")

# Add a needle pointing to the current speed (e.g., 101 km/h)
current_speed = 101  # Replace with your actual speed value
needle_position = (current_speed / 120) * 1 # Scale the speed to the chart's x-axis
plt.annotate(str(current_speed), xytext=(0, 0), xy=(needle_position, 2.0),
             arrowprops=dict(arrowstyle="wedge, tail_width=0.5", color="black", shrinkA=0),
             bbox=dict(boxstyle="circle", facecolor="black", linewidth=2.0),
             fontsize=45, color="white", ha="center")

# Add a title
plt.title("Maximum Permissible Speed Achieved", loc="center", pad=20, fontsize=35, fontweight="bold")

# Hide the axis
ax.set_axis_off()

def handle_key_14(event):
        if event.key == 'q':
            plt.close()  # Close the current plot

    # Attach the event listener for the seventh plot
plt.gcf().canvas.mpl_connect('key_press_event', handle_key_14)

    # Show the tenth plot
plt.show()