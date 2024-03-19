
# Face-Recognition-System-Crypto
A facial recognition system combined with password hashing for login, and image encryption for facial authentication 

At the following link you can view the presentation of the project in the Information Systems Security and Privacy exam and the Testing videos of our project.
[Link Presentation Project](https://www.canva.com/design/DAF_2Ut0Fuk/myb7aMiR7X2RX4GMqJR8yQ/edit?utm_content=DAF_2Ut0Fuk&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

## Description of the Project
The project is structured in 4 pages:

 - **Main page**: contains the page for create an user, check a user, to encrypt and decrypt the database of images, and view a list of login of all users;
 - **Create User**: to create an user with username and password, after registering, there will be two buttons: one for taking 300 photos to enrol the model by facial detection, the second for training the model;
 - **Check User**: the user's identity will be checked before actual facial recognition, if there is a match between the registered face and the user to be authenticated, the login will be successful, otherwise access will be denied;
 - **Encryption Page**: a page to perform an encryption or decryption of images folder. To do that before we indicate the username of user;
 - **Login List**: the access for this page is only for the administrator of application. In this page the admin can visualize who is perform the login and their result.

**Important**: the password of every user is hashed with **bcrypt** library in order to improve the level of security of the model.

### Architecture Model
In this project we use 2 model pre-trained: 

 - Model for facial detection **Haar**;
 - Model for facial identification **LBPH**
Sure, here are brief descriptions of Haar and LBPH models:

**Haar Models:**
Haar models are a type of feature-based object detection method. They utilize Haar-like features, which are rectangular regions at specific locations within an image. These features are used to describe the visual characteristics of objects. The Haar model works by comparing these features in different regions of an image to a set of trained patterns representing the object to be detected. This comparison allows the model to identify whether the object of interest is present in a given region of the image.

**LBPH (Local Binary Patterns Histograms) Models:**
LBPH models are commonly used for texture classification and facial recognition tasks. They operate by dividing an image into small regions and extracting local binary patterns from each region. Local binary patterns describe the texture of an image by comparing the intensity of a central pixel with its neighboring pixels. These binary patterns are then converted into histograms, which capture the frequency of occurrence of different patterns within each region. LBPH models use these histograms as feature vectors for training and classification purposes, making them particularly effective for tasks involving texture analysis and facial recognition.
