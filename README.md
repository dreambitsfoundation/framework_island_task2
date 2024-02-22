# Framework Island - Task 2

## Event Management Application.

This is a Django application which implements two models `Event` and `EventRegistration` to cater a CRUD interface to manage event and registrations/bookings.

### Main objectives

1. Event CRUD using DRF.
2. EventRegistration CRUD using DRF
3. User CRUD using DRF.
3. User Authentication using JWT - Only authenticated users can access both the interfaces.

### Design

#### Requirement Analysis

As per the requirement

1. Facilitate CRUD operations for Event model using DRF.
2. Facilitate CRUD operations for Event Management model using DRF.
3. Implement JWT authentication.

Note: Unit tests will be added for each Models and View.

#### Consideations

Following are the considerations that I have made before beginning the development:

1. An admin user can access the system through Django Admin and also rest APIs.
2. Events can be created and modified only by an Admin User.
3. User of any type can register for an event.
4. Any EventRegistration/booking once created can only be cancelled by setting a flag `is_active = False`.
5. EventRegistration once created can only be cancelled by an admin user or the specific record owner.
6. Any user can only view their own EventRegistration records active/cancelled both.
7. Every Event record has a `capacity` field that sets the max active EventRegistration records allowed for this event, before any new EventRegistration we must confirm that the total number of EventRegistration records associated with the current event having `is_active` flag set should be less than the value of `capacity`.

#### Database Design

1. In this project `Event` table has been employed as the parent table.
2. Then there is `EventRegistration` table which represents the bookings.
3. EventRegistration table has a foreignkey relation with the Event through the `event_id` field.

#### Application

** Program Setup **

1. We'll be registering both `Event` and `EventRegistration` table in the Django Admin.
2. CRUD operations for `Event` and `EventRegistration` model both can also be done with REST API.
3. Admin users will be allowed to make any changes through Django admin, also those which may not be permitted by Rest API logic.
4. We'll be extending `ModelViewSet` class of DRF to create API views.

** User Authentication and View security decissions **

1. As decided in the pre-development considerations, all views will be protected by JWT autentication logic.
2. Any un-aunthenticated user should be given a 401 status on calling any API.
3. There are some endpoint such as all endpoints for Event and some of EventRegistration which is only applicable to AdminUser or a user instance that has the flag is_staff set.


** Storage **

1. Since the requirement is very straight forward, we'll be using SQlite file database storage.
2. All the image files associated with the inventory form will be saved in the defined directory within the project.

## Installation guidlines

1. Clone this repository into your local system.
2. `cd` into root directory and create a Virtual Environment `python -m venv venv`
3. Activate the virtual environment
   Windows: `venv/Scripts/activate`
   MacOS/Linux: `source venv/bin/activate`
4. Install all dependecies: `pip install -r requirements.txt`
5. Migrate all the models. `python manage.py migrate`
6. Run all the tests `python manage.py test`
7. Create a superuser `python manage.py createsuperuser`
8. Run the development server `python manage.py runserver`

## My local setup

1. OS: Windows 11
2. Python: 3.7.9 (it's fine to use the latest version 3.12.x)

## Play around/User Guide

1. First goto `localhost:8000/admin/`
2. Enter your superuser `username` and `password` to login to Django admin. Now you will be able to access all the pages on the application.
3. Postman file is provided in the project for reference to API documentation.

## What is not done?

Following are the items which can be considered as a scope of development in future
1. Set a tenure for every Event's lifetime, using `start_datetime` and `end_datetime` field and any new Event Registration/booking will only be allowed within the date time range between `start_datetime` and `end_datetime`.
