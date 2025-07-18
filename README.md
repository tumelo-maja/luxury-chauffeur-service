# luxury-chauffeur-service


**Authors:** Tumelo Maja (GitHub username: tumelo-maja)

Luxury Chauffeur Service is an applicatiuon

**The application is aimed at helping users to:** 
  - Book for a chauffeur service


**Target audience:** 
  - Business individuals looking for chauffeur services
  - Wedding planner for weddings events
  - Tourist wanting to travel around the city in style

**Application Mockup:** 
  

## Features 

### Existing Features

- 

### Features Left to Implement

- 

## Project planning
In this section, we provide all tasks related to project planning for development of the application. User stories and business goals are presented in this section

### Key business goals
Primary goal: provide luxury chauffeur service for private and business use

Other goals:
- I


### User stories

- **USER STORY: User Registration and Profile Creation (must-have)**

    - As a **New Client**, I can **register an account and create a profile** so that **I can manage my details.**

  **Acceptance Criteria:**
    - User can register an account with their email and password.
    - User receives a confirmation email upon successful registration.
    - User is redirected to the profile creation page after registration.

- **USER STORY: View Profile Details (must-have)**

    - As a **Client**, I can **view my profile information** so that **I can see the details I provided during registration.**

  **Acceptance Criteria:**
    - Given the user is logged in, they can view their profile details.
    - User can view emergency contact details saved on their profile.
    - User can view their preferred name and title saved on their profile.

- **USER STORY: Update Profile Details (must-have)**

    - As a **Client**, I can **edit and update my profile details** so that **I can make changes to my information when I need to.**

  **Acceptance Criteria:**
    - Given the user is logged in, they can edit their profile details.
    - User can upload or update their profile avatar.
    - User can update their home address and emergency contact details.
    - User is shown confirmation when changes are saved.

- **USER STORY: Delete Account (must-have)**

    - As a **Client**, I can **delete my account** so that **I can remove my information from the platform.**

  **Acceptance Criteria:**
    - Given the user is logged in, they can choose to delete their account.
    - User is prompted to confirm their decision before account deletion.
    - After deleting the account, the user is logged out and their account is removed from the platform.

- **USER STORY: Request a Trip (must-have)**

    - As a **Client**, I can **create a trip request** so that **I can book a chauffeur for my trip.**

  **Acceptance Criteria:**
    - User can input pickup location and destination for the trip.
    - User can choose the type of vehicle they want for their trip (3 vehicle types).
    - Trip status is shown to user, 'pending', 'confirmed', 'canceled','modified'

- **USER STORY: Edit a Trip (must-have)**

    - As a **Client**, I can **edit a trip request** so that **I can make changes to my trip.**

  **Acceptance Criteria:**
    - User can change booking details (location, date, driver etc.).
    - After editing, trip status changes to 'pending' if it was previously confirmed.

- **USER STORY: Cancel a Trip (must-have)**

    - As a **Client**, I can **cancel a trip request** so that **I can it will be removed from my upcoming trips.**

  **Acceptance Criteria:**
    - User can delete a trip.
    - Confirmation is required for trip deletion.
    - deleted trips will not appear in the display panel.

- **USER STORY: Confirm a Trip (must-have)**

    - As a **Coordinator**, I can **confirm trip requests** so that **I can allocate drivers to requested trips.**

  **Acceptance Criteria:**
    - Given a new trip request, the coordinator can view the trip details (pickup location, client, preferred driver if specified).
    - Coordinator can assign a driver and confirm the trip.
    - Driver gets the trip assignment
    - User is notified once the trip is confirmed.

- **USER STORY: View allocated trips (must-have)**

    - As a **Driver**, I can **see trips that have been allocated to me** so that **I can prepare for the trip.**

  **Acceptance Criteria:**
    - Given the trip is assigned, the driver can view the trip details (client, pickup location, car type).
    - Driver receives a notification confirming the trip allocation.

- **USER STORY: Admin Dashboard (must-have)**

    - As an **Administrator**, I can **view and manage all trips, users, and feedback** so that **I can monitor the service.**

  **Acceptance Criteria:**
    - Given user is logged in with admin role, they can see a dashboard with a list of all trips, users (clients, drivers, coordinators), and their statuses.
    - Admin user can modify or delete trips and users.

- **USER STORY: Home Page (must-have)**

    - As an **client**, I can **view the home page** so that **I can get an overview the services offered on the website.**

  **Acceptance Criteria:**
    - home page should display a welcoming message with a brief overview of the service.
    - user-friendly and intuitive navigation
    - home page is responsive for desktop and mobile views.

- **USER STORY: Chauffeurs Page (must-have)**

    - As an **client**, I can **view the profiles of the drivers** so that **I can choose the driver I want to for my coming trip.**

  **Acceptance Criteria:**
    - chauffeur page should display a profiles of drivers.
    - Each profile card has a 'book now' link
    - Basic driver info is displayed including their avatar

- **USER STORY: View Available Drivers (should-have)**

    - As a **Client**, I can **view available drivers** so that **I can choose the most suitable driver for my trip.**

  **Acceptance Criteria:**
    - User can see a list of available drivers in their city or branch.
    - Driver profiles display information including name, image, experience, and availability.
    - User can filter drivers based on location and availability.

- **USER STORY: End Trip and Provide Feedback (should-have)**

    - As a **Driver**, I can **end a trip and provide feedback** so that **the trip is closed and I can submit feedback about the trip.**

  **Acceptance Criteria:**
    - Driver can mark the trip as completed once the trip ends.
    - Driver can submit feedback about the client and rate the client (out of 5).

- **USER STORY: View Trip History (should-have)**

    - As a **Client**, I can **view my trip history** so that **I can keep track of my past trips.**

  **Acceptance Criteria:**
    - Client can see a list of all completed, ongoing, and canceled trips.
    - Client can filter trips by date and trip status.
    - Client can view trip details (date, driver name etc.).

- **USER STORY: Social Login Integration (could-have)**

    - As a **Client**, I can **sign up and log in using my social media accounts** so that **I can quickly access the app without needing to create a new account manually.**

  **Acceptance Criteria:**
    - User can register using Google (GitHub, Twitter, Facebook, or LinkedIn could be included ).
    - User can log in using their existing Google or Facebook account.
    - User is redirected to the profile creation page if logging in for the first time.
    - User email is used to link between email/password login and social account logins - must be unique.

- **USER STORY: Driver Registration (could-have)**

    - As a **Potential Driver**, I can **register to become a driver** so that **I can be considered to join the service as a driver.**

  **Acceptance Criteria:**
    - User can register as a driver by completing an application if they meet the requirements.
    - Once submitted, 'pending approval' status is displayed on the account. can be approved by admin or coordinator
    - If approved, driver is notified and can complete their profile by adding more details including their availability.
    - If not approved, driver is notified and the profile will have a status of rejected.

- **USER STORY: Submit Client Feedback and Rating (could-have)**

    - As a **Client**, I can **submit feedback and rate the driver** so that **I can provide feedback on the service I received.**

  **Acceptance Criteria:**
    - Client can rate the driver (1 to 5 stars) at the end of the trip.
    - Client can leave a feedback about the driver’s service.
    - Client's feedback is saved and visible to the driver and coordinator.
    - Only ratings are visible to other service users

- **USER STORY: Real-Time Chat for active trips**

    - As a **Client**, I can **chat with the Driver in real-time** during confirmed or ongoing trips so that **I can communicate easily with the driver for any trip-related updates.**

  **Acceptance Criteria:**
    - Client and driver can send and receive messages during an ongoing or upcoming trip.
    - Both can view the entire chat history for the current trip.
    - Chat update automatically without having to refresh the page.
    - Both can see an indicator on the trip when a new message is received.
    - history chat can be viewed for past trips but no new message can be added

### Flow/ERD charts


## Technologies



## Testing 
### Feature Testing

### Code validation


### Bugs


## Deployment


## Credits

- close list when clicking outside element - https://stackoverflow.com/questions/152975/how-do-i-detect-a-click-outside-an-element/54633092
- sort strings JS - https://medium.com/nerd-for-tech/basics-of-javascript-string-localecompare-method-b2aa50207706
-  Install tailwind - https://www.youtube.com/watch?v=REnumA4TNu4
- Render templates to modals - https://www.youtube.com/watch?v=3dyQigrEj8A

- datetime flatpicker - https://www.youtube.com/watch?v=h7KpTZaYM34

- date format filters - https://docs.djangoproject.com/en/5.2/ref/templates/builtins/#date

- https://stackoverflow.com/questions/45961459/multiple-authentication-backends-configured-and-therefore-must-provide-the-back - multiple backends error
- Tutorial Autocomplete google maps: https://www.youtube.com/watch?v=0jMOK-QFDro

- Tutorial for creating image carousel - https://www.youtube.com/watch?v=bW8X-tt5AZQ

- Generate logo with AI - https://wix.com/

- Convert logo to Favicon - https://favicraft.com/convert

- Image by <a href="https://pixabay.com/users/peggy_marco-1553824/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=1029584">Peggy und Marco Lachmann-Anke</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=1029584">Pixabay</a>

- https://alpinejs.dev/directives/bind - for toggle functionality

- https://randomkeygen.com/ - generate secret key 

- Css clip path generator - https://bennettfeely.com/clippy/
##  Run history
- `.gitignore` and venv setup
- package installations: 
`.\.venv\Scripts\activate`
`pip3 install Django~=4.2.1 dj-database-url~=0.5 psycopg2~=2.9`
`pip3 freeze --local > requirements.txt`
`django-admin startproject chauffeur .`
`python manage.py migrate`
`python manage.py runserver`

Google cloud:
- create project
- Enable APIs: Places API and Maps JavaScript API
- Billing account required 


