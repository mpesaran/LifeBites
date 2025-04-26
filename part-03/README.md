# HBnB
hbnb is a web application that replicates the functionality of Airbnb, allowing users to manage and book various accommodations. This project is built using Flask and follows RESTful API principles.

## Features

- User registration and authentication
- Create, retrieve, update, and delete users
- Manage places, reviews, and amenities
- Input validation and error handling
- Well-documented API using Flask-RESTx

### Directories and Files:

- **app/**: Contains the core application code.
  - **`__init__.py`**: Initializes the application package.
  
  - **api/**: Houses the API endpoints, organized by version (v1/).
    - **v1/**: Contains version 1 of the API.
      - **`__init__.py`**: Initializes the v1 API module.
      - **users.py**: Manages user-related endpoints.
      - **places.py**: Manages place-related endpoints.
      - **reviews.py**: Manages review-related endpoints.
      - **amenities.py**: Manages amenity-related endpoints.
  
  - **models/**: Contains business logic classes for the application.
    - **`__init__.py`**: Initializes the models package.
    - **user.py**: Defines the User model.
    - **place.py**: Defines the Place model.
    - **review.py**: Defines the Review model.
    - **amenity.py**: Defines the Amenity model.
  
  - **services/**: Implements the Facade pattern which manages the interaction between layers.
    - **`__init__.py`**: Initializes the services package.
    - **facade.py**: Contains business logic to interface between models and persistence layers.

  - **persistence/**: Implements an in-memory repository. This will later be replaced by a database-backed solution using SQLAlchemy.
    - **`__init__.py`**: Initializes the persistence package.
    - **repository.py**: Contains the repository implementation.

- **run.py**: Entry point for running the Flask application.
  
- **config.py**: Configures environment variables and application settings.
  
- **requirements.txt**: Lists all Python packages needed for the project.
  
- **README.md**: This file contains a brief overview of the project and instructions.

## Installation

To install the necessary dependencies, run:

```bash
pip install -r requirements.txt
python run.py

```
## API Endpoints

### User Routes

- `POST /api/v1/users/` - Register a new user
- `GET /api/v1/users/` - Retrieve a list of users
- `GET /api/v1/users/<user_id>` - Get user details by ID
- `PUT /api/v1/users/<user_id>` - Update user details

### Place Routes

- `POST /api/v1/places/` - Create a new place


### Review Routes

- `POST /api/v1/reviews/` - Create a new review


### Amenity Routes

- `POST /api/v1/amenities/` - Create a new amenity

## Running Tests

To run the tests, use the following command:
 ```bash
 pytest filename
 ```

## Contributors
- [Anna Ly](https://github.com/aavly)
- [Crystal Carroll](https://github.com/Crystal-holberton)
- [John Nkpolukwu](https://github.com/Johnnsonkp)
- [Mahsa Pesaran](https://github.com/mpesaran)