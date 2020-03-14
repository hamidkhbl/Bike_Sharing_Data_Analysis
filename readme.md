# Bike sharing data analysis
### `by Hamid Khodabandehloo`
Make sure to install the following packages:

`conda install -c conda-forge gmaps`

`conda install -c conda-forge pyproj`

To see the google map figures you need store your gmaps API key on a file named `auth`.


## Dataset
The required dataset will be download from [here](https://s3.amazonaws.com/baywheels-data/index.html) by running the code. All the 12 files for each month will be merged.  


## Summary of Findings
I introduced 9 research questions. Here are the short answers for the questions:
1. **Is there any relationship between the day of the week and trip duration, distance and speed?** 
    - Trip duration is considerably higher at weekends.
    - The number of trips is lower at weekends.
    - People tend to ride faster during weekdays comparing to weekdays.
    - Trip distance is slightly smaller at the weekends.
2. **How are the stations distributed geographically?**
    - In San Francisco, most of the stations are located at the center and west side of the city.
    - In Oakland, stations are scattered from south to north with a high-density downtown. 
    - The city center hosts the most station in San Jose.
3. **What time in a day do people use bikes more frequently?**
    - From 7 am to 9 am, and from 4 pm to 6 pm is the most crowded hours. Usage during these hours is considerably higher for subscribers comparing to casual users.
4. **How did bike usage change in different months?**
    - The number of trips is higher in March, April and October. January, February, November and December are the most rainest months in this region. May, July, Jun and August are the hottest months with direct sun. It seems people select a bike when the weather is not too rainy or too sunny.
5. **How different users (Subscribers or casual customers) use bikes?**
    - Subscribers use bikes more during peak hours and weekdays. Most probably, their purpose is to commute to work. Casual customer usage is not showing a significant difference in different hours and days.
6. **How subscribers' and casual users' trips are distributed in each city?**
    - In San Francisco, 26.08% of trips are done by casual customers. This number for Oakland and San Jose is 20.10% and 12.30%, respectively.
7. **Are there any suspicious activities?**
    - There are some trips with surprising speed. The standard speed for a bike is 18 to 30 km/h. However, there are some trips with a very high speed, which is suspicious. For example, speed for a journey was more than 70 km/h, which is highly questionable. After investigating the trip, I realized that the bike was moved from San Francisco to San Jose, and there is no travel history for the bike after that. Trips with a very high duration also investigated. Most probably, the bike was idle for the time, or the user has finished the trip, but the application did not consider the journey as ended.
8. **Is there any travel between cities?** 
    - There is 116 travel between cities in 2019. 
    - Seventy-three of them are from San Fransisco to Oakland.
    - Thirty-eight trips took place from Oakland to San Francisco.
    - Three trips from San Jose to San Francisco.
    - Only one trip from San Jose to Oakland.
    - One trip From San Francisco to San Jose.
9. **How much gas have been saved by the Ford GoBike system?**
    - The bike-sharing system saved about half a million litter gas.

> 
