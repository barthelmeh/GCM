# Gesture Controlled Interface Manipulation
_Written for COSC428 26/06/2024_  
**Tom Barthelmeh**

This project uses MediaPipe Hands to recognise hand landmarks, and custom defined gestures to allow the user to control 
the mouse.

### Requirements
The package requirements are defined in _Requirements.txt_

### How to run
To run the code, clone the git repository and open a terminal at the root of that folder.
Then, run the following code:

To download the required packages, run:
```bash
pip install -r requirements.txt
```

To run the application:
```bash
python main.py
```


### How to use

The mouse can be controlled by the movement of the user's right hand.

Four gestures are defined on the position of the user's left hand:

**Left Click:** The user needs to place their forefinger and thumb together.  
**Right Click:** The user needs to place their middle finger and thumb together.  
**Double Left Click:** The user needs to place their pinky finger and thumb together.  
**Scrolling:** The user needs to place all their fingers and thumb together. Then, to scroll up or down the user moves their left hand up or down.  
