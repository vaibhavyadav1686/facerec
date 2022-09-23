# FACEREC
A facial recognition portal based on facial_recognition library of Python.

We took part in the Goa Police Hackathon 2022. As part of thus we have developed a very basic facial recognition based portal.


## Problem Statement

### Facial Recognition

To build a face recognition based solution to establish the identity of the person based on matching with a
database of arrested persons, missing persons, tenants and unidentified dead bodies.

## Explanation of Problem Statement

We all know that Police is modernising their surveillance and security techniques rapidly, thus there is a new
necessity to integrate technology to reduce the manual work and paperwork and bridge the gap between
authorities and technology. A facial recognition software will help identify criminals and victims easily. This will
largely reduce the time consumed while going through tons of files. This will also reduce the need of big storages
for files and the need of Stationary Resources. Hence, there is a need to develop a necessary database integrated
with an interactive platform to help the police with effective investigations.

## Proposed Solution to Problem Statement

An interactive website would be developed which would allow police officers to compare an input media with
pre-existing records of arrested persons, missing persons, tenants and unidentified dead bodies. Our website will
be an internal website with access only to concerned police officials. The system would already be trained by the
neural network to recognize faces in the images and videos existing in the database. A convolutional neural
network would be used as it is a good artificial neural network for analysing images and videos. The database
would be internal and we are not using Open Source databases as it is not expandable according to policing
requirements and might be misleading since it is easy to fake one’s identity in this social world. An internal
database would allow the officials to add new records to the database and further help with the investigation of
future cases. This would also allow them to find relations between various records and help keep a track of
criminal groups and gangs.

## Features of Final Solution
Once a media file has to be used to identify a person, the website is opened. It asks the official to input a UserID
and Password (assigned by authorities). This allows for a secure login, following which a face authentication step
needs to be passed. This allows for a Multi-Factor Authentication and therefore increases security. Once website
is logged into, two options are displayed on the screen:
* Add new record - Here, two options are displayed:
  * Add new: To add a new record to the database. Officer enters Name, Date of Birth, Address,
Gender, multiple pictures of the person and criminal record.
  * Change existing record: Allows the addition of more crimes committed.
* Identification - Allows the official to check the database for identification. Based on whether a match is
found or not the following occurs:
  * If a match is found, the details of the person are fetched and displayed on the screen.
  * If no match is found, a “Try Again” option is given which increases the tolerance value thereby
allowing to display loosely matched records.
  * If still no match is found, a pop up box displays “No match found”. On clicking the “OK” button, the
page is redirected to the Identification page.

![Goa Police Hackathon](https://user-images.githubusercontent.com/111295749/192036222-495ecd92-29ee-4ead-a2fa-97737f65b3d0.jpg)
