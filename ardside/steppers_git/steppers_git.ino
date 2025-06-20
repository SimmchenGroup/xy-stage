#include <AccelStepper.h>

AccelStepper stepperX(AccelStepper::DRIVER, 2, 5);  // STEP, DIR
AccelStepper stepperY(AccelStepper::DRIVER, 3, 6);  // STEP, DIR

// These will be the enable pins in future but for now are LEDs
const int x_pink = 8;
const int y_yell = 9;

// Analog Pins of the Arduino: 'measuring' a voltage given by the potentiostats on the joystick
const int joyXPin = A0;
const int joyYPin = A1;

const int deadzone = 50;  // Analog deadzone: e.g. if the voltage is 5% either side of neutral 
const int maxSpeed = 800;

String inputString = "";
bool stringComplete = false;

int serialXSpeed = 0;
int serialYSpeed = 0;

void setup() {
  // Serial communication initialisation
  Serial.begin(115200);
  inputString.reserve(20);

  pinMode(x_pink, OUTPUT);
  pinMode(y_yell, OUTPUT);

  blinking(5, x_pink, 50);
  blinking(6, y_yell, 50);

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
  
  // Joystick read
  int joyX = analogRead(joyXPin);
  int joyY = analogRead(joyYPin);
  int xOffset = joyX - 512;
  int yOffset = joyY - 512;
  
  bool joystickActive = abs(xOffset) > deadzone || abs(yOffset) > deadzone;
  
  if (joystickActive) {
    // Override: joystick in control
    int xSpeed = map(xOffset, -512, 512, -maxSpeed, maxSpeed);
    int ySpeed = map(yOffset, -512, 512, -maxSpeed, maxSpeed);
    stepperX.setSpeed(xSpeed);
    stepperY.setSpeed(ySpeed);
  } else {
    // Joystick centered: allow serial control (speeds updated on handleCommand)
    stepperX.setSpeed(serialXSpeed);
    stepperY.setSpeed(serialYSpeed);
  }
  
  // Always run the motors
  stepperX.runSpeed();
  stepperY.runSpeed();
}

void handleCommand(String cmd) {
  //Serial.println("handleCommand invoked");
  cmd.trim();  // Remove excess whitespace
  
  if (cmd.length() == 0) return;  // Ignore empty commands

  // Stop command
  if (cmd.equalsIgnoreCase("S")) {
    serialXSpeed = 0;
    serialYSpeed = 0;
    stepperX.stop();  // Optionally stop or set speed to zero
    stepperY.stop();
    Serial.println("Stopping on Arduino end due to 'S'");
    return;
  }
  
  char axis = cmd.charAt(0);
  if (axis != 'X' && axis != 'Y') {
    // Invalid axis command – ignore
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
      stepperX.move(steps);
      blink(x_pink, steps);
      //Serial.println("Moving in X");
    } else {
      stepperY.move(steps);
      blink(y_yell, steps);
      //Serial.println("Moving in Y");
    }
  }
  else {
    // Continuous speed command (e.g., X+300, Y-150)
    Serial.println("Continuous Speed?");
    char dir = param.charAt(0);
    String speedStr = param.substring(1);
    int speed = speedStr.toInt();
    
    if (dir == '-') speed = -speed;
    else if (dir != '+') { // Invalid direction, ignore
      return;
    }
    
    if (axis == 'X') {
      serialXSpeed = speed;
      stepperX.setSpeed(speed);
    } else {
      serialYSpeed = speed;
      stepperY.setSpeed(speed);
    }
  }
}

// Some LED functions for testing
void LED_ON(int pin) {
  digitalWrite(pin, HIGH);
}
void LED_OFF(int pin) {
  digitalWrite(pin, LOW);
}
void blink(int pin, int delaytime) {
  LED_ON(pin);
  delay(abs(delaytime));
  LED_OFF(pin);
  delay(abs(delaytime));
}
void blinking(int cycles, int pin, int speed) {
  for (int i = 0; i < cycles; i++) {  // Using < cycles ensures the LED blinks "cycles" times
    blink(pin, speed);
  }
}