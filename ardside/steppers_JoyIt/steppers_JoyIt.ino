#include <AccelStepper.h>

// Stepper Pins
AccelStepper stepperX(AccelStepper::DRIVER, 2, 5);  // STEP, DIR
AccelStepper stepperY(AccelStepper::DRIVER, 3, 6);  // STEP, DIR

const int x_EN = 9;
const int y_EN = 8;

// Analog Pins of the Arduino: 'measuring' a voltage given by the potentiostats on the joystick
const int joyUp = 14;
const int joyDown = 15;
const int joyLeft = 16;
const int joyRight = 17;

String inputString = "";
bool stringComplete = false;

const int maxSpeed = 2500;

// overall moveSpeed for the joystick
int moveSpeed = 300;

float currentSpeed = 300;

// variable movement speeds 
int serialXSpeed = 0;
int serialYSpeed = 0;

void setup() {
  // Serial communication initialisation
  Serial.begin(115200);
  inputString.reserve(20);

  // initialise joystick pins (these are simple switches)
  pinMode(joyUp, INPUT_PULLUP);
  pinMode(joyDown, INPUT_PULLUP);
  pinMode(joyLeft, INPUT_PULLUP);
  pinMode(joyRight, INPUT_PULLUP);

  
  pinMode(x_EN, OUTPUT);
  digitalWrite(x_EN, LOW);

  pinMode(y_EN, OUTPUT);
  digitalWrite(y_EN, LOW);
  
  stepperX.setMaxSpeed(maxSpeed);
  stepperY.setMaxSpeed(maxSpeed);

  Serial.println("Hello");
}

void loop() {
  // --- Add non-blocking serial reading code ---
  while (Serial.available() > 0) {
    char inChar = (char)Serial.read();
    // Check if end-of-line is reached
    if (inChar == '\n' || inChar == '\r') {
      // If there is any data in "inputString" before encountering the newline,
      // then mark the command as complete.
      if (inputString.length() > 0) {
         stringComplete = true;
      }
    } else {
      inputString += inChar;
    }
  }
  
  // --- Process any complete command ---
  if (stringComplete) {
    handleCommand(inputString);
    inputString = "";
    stringComplete = false;
  }
  
  bool joystickActive = (digitalRead(joyUp) == LOW || digitalRead(joyDown) == LOW || digitalRead(joyLeft) == LOW || digitalRead(joyRight) == LOW );
  
  if (joystickActive) {
    serialXSpeed = 0;
    serialYSpeed = 0;
    if (digitalRead(joyUp) == LOW){
      stepperY.setSpeed(moveSpeed);
      stepperY.runSpeed();
    }
    else if (digitalRead(joyDown) == LOW){
      stepperY.setSpeed((-moveSpeed));
      stepperY.runSpeed();
    }
    if (digitalRead(joyRight) == LOW){
      stepperX.setSpeed(moveSpeed);
      stepperX.runSpeed();
    }
    else if (digitalRead(joyLeft) == LOW){
      stepperX.setSpeed(-moveSpeed);
      stepperX.runSpeed();
    }
  } else {
    // Joystick centered: allow serial control (speeds updated on handleCommand)
    stepperX.setSpeed(serialXSpeed);
    stepperY.setSpeed(serialYSpeed);
    stepperX.runSpeed();
    stepperY.runSpeed();
  }
  // Always run the motors

}

void handleCommand(String cmd) {
  //Serial.println("handleCommand invoked");
  stepperX.run();
  stepperY.run();

  cmd.trim();  // Remove excess whitespace
  
  if (cmd.length() == 0) return;  // Ignore empty commands

  // Stop command
  if (cmd.equalsIgnoreCase("S")) {
    serialXSpeed = 0;
    serialYSpeed = 0;
    stepperX.stop();  // Optionally stop or set speed to zero
    stepperY.stop();
    Serial.println("Stopping on Arduino end due to 'S'");
    Serial.println("DONE");
    return;
  }
  
  char axis = cmd.charAt(0);
  if (axis != 'X' && axis != 'Y' && axis != 'V') {
    Serial.println("Invalid Axis");
    // Invalid axis command – ignore
    return;
  }

  if (axis == 'V') {
    int newSpeed = cmd.substring(1).toInt();  // Handles +/-
    moveSpeed = constrain(abs(newSpeed), 0, maxSpeed);  // Cap to safe range
    Serial.println("Updated Movement Speed to " + String(moveSpeed));
    return;
  }

  
  String param = cmd.substring(1);
  if (param.length() == 0) return;  // No parameter provided
  
  // Position move command, prefix 'm' (e.g., Xm+100, Ym-50)
  if (param.charAt(0) == 'm') {
    String stepsStr = param.substring(1);  // Remove 'm'
    int steps = stepsStr.toInt();
    //Serial.println("m was detected");
    Serial.println("Axis: " + String(axis) + " | Steps: " + String(steps));
    // Move relative steps
    if (axis == 'X') {
      stepperX.setMaxSpeed(moveSpeed * 10);
      stepperX.setAcceleration(moveSpeed * 1000);
      stepperX.moveTo(stepperX.currentPosition() + steps);
      stepperX.runToPosition();
      Serial.println("DONE");
    }
    else if (axis == 'Y') {
      stepperY.setMaxSpeed(moveSpeed * 10);       // units: steps per second
      stepperY.setAcceleration(moveSpeed * 1000);
      stepperY.moveTo(stepperY.currentPosition() + steps);
      stepperY.runToPosition();
      Serial.println("DONE");
    }
  }
  else {
    // Continuous speed command (e.g., X+300, Y-150)
    char dir = param.charAt(0);
    String speedStr = param.substring(1);
    int speed = speedStr.toInt();

    Serial.println("Dir: "+String(dir) +" | Speed: "+speedStr);
    
    if (dir == '-') speed = -speed;
    else if (dir != '+') { // Invalid direction, ignore
      Serial.println("Invalid Direction");
      return;
    }
    
    if (axis == 'X') {
      serialXSpeed = speed;
      stepperX.setSpeed(speed);
    }
    if (axis == 'Y') {
      serialYSpeed = speed;
      stepperY.setSpeed(speed);
    }
  }
}

