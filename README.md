# TravelBuddy - Android Application

## Author & Subject

**Hilla Heimberg & Omri Marom**  

TravelBuddy - Android Studio & Kotlin & Python & AWS

## Explanation of the App

This is an Android application called "TravelBuddy," which stores all the information you need when traveling abroad in one accessible place. 📱 This Android application, written in Kotlin, combines a backend part that deals with storage in Amazon's cloud service, AWS.
This application won the "Audience Favorite" award during the project presentations in the course. 🏆 

## Design And Architecture Description

The application code is divided into front and back. 
- **The front part**- written in Kotlin within the Android Studio environment. 
Its architecture follows the MVVM pattern, which stands for Model, View, and ViewModel. The ViewModel connects the view (responsible for the UI components) and the model (handling the logical part of data storage and updates).

- **The backend part**- written in Python with storage using Amazon's cloud service- AWS, retrieves and updates data through network calls from the model to the database. We also implemented a cache that stores information locally, allowing us to retrieve data without network calls if it hasn't been updated, thereby saving on network usage.

## Screenshots

![Screenshot 1](/logoFragment.jpg)

![Screenshot 2](/menuFragment.jpg)

![Screenshot 3](/TravelBuddyOpt.gif)

![Screenshot 4](/winning.jpg)

![Screenshot 5](/Winning2.jpg)

## Notes

HAVE A GOOD DAY :D
