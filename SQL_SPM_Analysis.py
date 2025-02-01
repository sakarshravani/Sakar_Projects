import mysql.connector

# Establishing the connection
conn = mysql.connector.connect(
    host="localhost",    # Database host
    user="root",         # MySQL username
    password="root",     # MySQL password
    database="SakarSPM"  # The database you're working with
)


cursor = conn.cursor()


query1= "SELECT NumberOfStops FROM TrainDetails WHERE ID = %s"

cursor.execute(query1, (12939,))

result = cursor.fetchone()

if result:
    print(f"Number of Stops for train ID 12939: {result[0]}")
else:
    print("No data found !")

query2="select FifthStop from TrainPath where id=%s"
cursor.execute(query2,(12939,))

result1 = cursor.fetchone()

if result1:
    print(f"Fifth Stop for train ID 12939: {result1[0]}")
else:
    print("No data found !")


query3 = "select sec1_sr,sec1_km from TrainSRKM where id = %s"
cursor.execute(query3,(12939,))

result2 = cursor.fetchone()

if result2:
    sec1_sr, sec1_km = result2 #unpacking the tuple value stored in result2 
    print(f"Section 1 speed restriction is {sec1_sr} and Section 1 km is {sec1_km} for train ID 12939")

else:
    print("No data found !")


query3 = "select tp.*, td.TrainType from TrainPath tp join TrainDetails td on tp.id = td.id where tp.id =%s  "
cursor.execute(query3,(12939,))

result3 = cursor.fetchone()

if result3 :
    (ID, FirstStop, SecondStop, ThirdStop, FourthStop,FifthStop,TrainType ) = result3

    print(f"Train ID: {ID}")
    print(f"First Stop: {FirstStop}")
    print(f"Second Stop: {SecondStop}")
    print(f"Third Stop: {ThirdStop}")
    print(f"Fourth Stop: {FourthStop}")
    print(f"Fifth Stop: {FifthStop}")
    print(f"Train Type: {TrainType}")

else:
    print("No data found !")

#calculating the total distance of the train
query4 = "select sec1_km,sec2_km,sec3_km,sec4_km,sec5_km from TrainSRKM where id = %s"
cursor.execute(query4,(12939,))

result4 = cursor.fetchone()

if result4:
    total_distance = sum(int(distance) for distance in result4 if distance is not None)
    print(f"Total Distance of train is {total_distance} km.")
else:
    print("No data found !")

 

#distance between 3rd stop and 5th stop
query5 = "SELECT sec3_km, sec5_km FROM TrainSRKM WHERE id = %s"
cursor.execute(query5, (12939,))
result5 = cursor.fetchone()

if result5:
             
            sec3_km = float(result5[0]) if result5[0] is not None else 0
            sec5_km = float(result5[1]) if result5[1] is not None else 0
           

           
            distance_3rd_to_5th = sec5_km - sec3_km

            print(f"Distance between 3rd stop and 5th stop is :{distance_3rd_to_5th}")
else:
     print("No data found !")
            

#KOP to mrj average psr
query6= """
            SELECT 
                sec2_sr, sec3_sr, sec4_sr
            FROM 
                TrainSRKM
            WHERE 
                ID = %s
        """
cursor.execute(query6, (12939,))
result = cursor.fetchone()

if result:
            # Extract passenger counts for the relevant sections
            passenger_counts = [result[0], result[1], result[2]]

            # Filter out None values
            valid_passenger_counts = [count for count in passenger_counts if count is not None]
            
            # Calculate average passenger count
            if valid_passenger_counts:
                average_passenger_count = sum(valid_passenger_counts) / len(valid_passenger_counts)
                print(f"Average PSR Count for KOP to MRJ (Train ID {12939}): {average_passenger_count:.2f}")
            else:
                print("No valid PSR data found for the given sections.")
else:
            print("No data found !")
            

query7 = """
            SELECT 
                FirstStop, SecondStop, ThirdStop, FourthStop, FifthStop
            FROM 
                TrainPath
            WHERE 
                ID = %s
        """
cursor.execute(query7, (12939,))
result7 = cursor.fetchone()         
            
if result7:
        stops = list(result7)  # Convert tuple to list
        print(f"Stops for train ID {12939}: {stops}")

        # Check if MRJ is in the list of stops
        if "MRJ" in stops:
            mrj_index = stops.index("MRJ")  # Find the position of MRJ
            print(f"MRJ is at position {mrj_index + 1} in the route.")
            print(f"Number of stops before MRJ: {mrj_index}")
        else:
            print("MRJ is not in the list of stops.")
else:
        print(f"Train ID {12939,} not found in TrainPath.")  


#calculating Max and min sr throughout the journey 
query8 = """
        SELECT 
            sec1_sr, sec2_sr, sec3_sr, sec4_sr, sec5_sr
        FROM 
            TrainSRKM
        WHERE 
            ID = %s
    """
cursor.execute(query8, (12939,))
result8 = cursor.fetchone()

if result8:
      max_sr = max(result8)
      min_sr = min(result8)
      print(f"Max SR for train ID {12939}: {max_sr}")
      print(f"Min SR for train ID {12939}: {min_sr}")
else:
      print(f"Train ID {12939,} not found in TrainSRKM.")
      

cursor.close()
conn.close()


#Based on the distance/kms for all the signals and stops per train, need to check if the loco made speed reductions when it was neither approaching a stop or a signal, entailing unnecessary reductions.
import pandas as pd
import mysql.connector

# Load the Excel file
df = pd.read_csv('28230.csv')

# Establishing a database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="SakarSPM"
)

cursor = conn.cursor()

# Fetch sectional speed restrictions and distances from the TrainSRKM2 table
cursor.execute("SELECT sec1_sr, sec1_km, sec2_sr, sec2_km, sec3_sr, sec3_km, "
               "sec4_sr, sec4_km, sec5_sr, sec5_km, sec6_sr, sec6_km, "
               "sec7_sr, sec7_km, sec8_sr, sec8_km, sec9_sr, sec9_km, "
               "sec10_sr, sec10_km, sec11_sr, sec11_km "
               "FROM TrainSRKM2 WHERE ID = 17630")

sections = cursor.fetchone()

# Close the cursor and connection
cursor.close()
conn.close()

# Parse the database results into sectional restrictions and distances
section_data = [(sections[i], sections[i + 1]) for i in range(0, len(sections), 2)]

# Calculate the total distance covered in the Excel file
total_distance = df['Distance(km)'].max() - df['Distance(km)'].min()
print(f"Total distance covered during the journey: {total_distance:.2f} km\n")

# Initialize variables to track the current distance
current_distance = df['Distance(km)'].min()

# Iterate through each section's restriction and distance
for idx, (speed_restriction, section_distance) in enumerate(section_data):
    if section_distance == 0:
        continue  # Skip if the section distance is 0

    # Define the section range based on cumulative distance
    start_distance = current_distance
    end_distance = current_distance + section_distance

    # Filter the data for the current section
    section_df = df[(df['Distance(km)'] >= start_distance) & (df['Distance(km)'] < end_distance)]

    # Check if section_df is empty (no data points in this section)
    if section_df.empty:
        print(f"Section {idx + 1} (Distance: {section_distance} km) - No Data Available")
    else:
        # Determine if overspeed detected
        max_speed = section_df['Speed(km/h)'].max()
        if max_speed > speed_restriction:
            print(f"Section {idx + 1} (Speed Restriction: {speed_restriction} km/h, Distance: {section_distance} km) - SR Overspeed Detected")
        else:
            print(f"Section {idx + 1} (Speed Restriction: {speed_restriction} km/h, Distance: {section_distance} km) - SR Overspeed Not Detected")

    # Update the current distance for the next section
    current_distance = end_distance
    #print(current_distance)
