
# IDP Project - Travel Agency

This project represents the implementation of a travel agency system formed using microservices and deployed using Docker Swarm.

## System Arhitecture
1. Database

Used for persistent storing for the entire application. Details about users and trips are saved in the database.

2. Database adaptor

This is a proxy for the database, used for securely accessing the data stored and filtering the user accesses. 

3. Client Interface

This is the entry point for the users of the application.

4. Administration Service

This is the interface used by administrators of the travel agency to interact with the application.

5. Monitoring System

This service is used for monitoring the system statistics such as the load of every node, the number of clients online etc.

## Scheme

![Image description](./img/diagram.png?raw=true)
