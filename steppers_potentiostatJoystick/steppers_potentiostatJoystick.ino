#include <AccelStepper.h>

AccelStepper stepperX(AccelStepper::DRIVER, 2, 5);  // STEP, DIR
AccelStepper stepperY(AccelStepper::DRIVER, 3, 6);  // STEP, DIR

// These will be the enable pins in future but for now are LEDs
const int x_step = 11;
const int y_step = 10;

const int x_move = 9;
const int y_move = 8;

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

  pinMode(x_step, OUTPUT);
  pinMode(y_step, OUTPUT);

  pinMode(x_move, OUTPUT);
  pinMode(y_move, OUTPUT);

  blinking(6, x_step, 50);
  blinking(6, y_step, 50);

  blinking(1, x_move, 300);
  blinking(1, y_move, 300);

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
  
  // Analog Joystick read
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
    led_bright(x_move, 0);
    led_bright(y_move, 0);
    LED_OFF(x_step);
    LED_OFF(y_step);
    Serial.println("Stopping on Arduino end due to 'S'");
    Serial.println("DONE");
    return;
  }
  
  char axis = cmd.charAt(0);
  if (axis != 'X' && axis != 'Y') {
    Serial.println("Invalid Axis");
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
      blink(x_step, steps);
      Serial.println("DONE");
    } else if (axis == 'Y') {
      stepperY.move(steps);
      blink(y_step, steps);
      Serial.println("DONE");
    }
  }
  else {
    // Continuous speed command (e.g., X+300, Y-150)
    Serial.print("Continuous | ");
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
      led_bright(x_move, serialXSpeed);
      stepperX.setSpeed(speed);
    }
    if (axis == 'Y') {
      serialYSpeed = speed;
      led_bright(y_move, serialYSpeed);
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

void led_bright(int pin, int speed){
  int brightness = map(abs(speed), 0, maxSpeed, 0, 255);
  analogWrite(pin, brightness);
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