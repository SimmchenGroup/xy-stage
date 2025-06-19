#include <AccelStepper.h>

AccelStepper stepperX(AccelStepper::DRIVER, 2, 5);  // STEP, DIR
AccelStepper stepperY(AccelStepper::DRIVER, 3, 6);  // STEP, DIR

// Analog Pins of the Arduino: 'measuring' a voltage given by the potentiostats on the joystick
const int joyXPin = A0;
const int joyYPin = A1;

const int deadzone = 50;  // Analog deadzone aka if the voltage is 5% either side of neutral 
const int maxSpeed = 800;

String inputString = "";
bool stringComplete = false;

int serialXSpeed = 0;
int serialYSpeed = 0;

void setup() {
  // Serial communication initialisation
  Serial.begin(115200);
  inputString.reserve(20);

  stepperX.setMaxSpeed(maxSpeed);
  stepperY.setMaxSpeed(maxSpeed);
}

void loop() {
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
    // Joystick centered: allow serial control
    if (stringComplete) {
      handleCommand(inputString);
      inputString = "";
      stringComplete = false;
    }
    stepperX.setSpeed(serialXSpeed);
    stepperY.setSpeed(serialYSpeed);
  }

  // Always run motors
  stepperX.runSpeed();
  stepperY.runSpeed();
}

void handleCommand(String cmd) {
  cmd.trim();  // Remove whitespace

  if (cmd.length() == 0) return;  // Ignore empty

  // Stop command
  if (cmd.equalsIgnoreCase("S")) {
    serialXSpeed = 0;
    serialYSpeed = 0;
    stepperX.stop();  // If using AccelStepper stop or zero speed
    stepperY.stop();
    return;
  }

  char axis = cmd.charAt(0);
  if (axis != 'X' && axis != 'Y') {
    // Invalid axis command
    return;
  }

  String param = cmd.substring(1);

  if (param.length() == 0) return;  // No param, ignore

  // Position move command, prefix 'm' (e.g., Xm+100, Ym-50)
  if (param.charAt(0) == 'm') {
    String stepsStr = param.substring(1);  // Remove 'm'
    int steps = stepsStr.toInt();

    // Move relative steps
    if (axis == 'X') {
      stepperX.move(steps);
    } else {
      stepperY.move(steps);
    }

  } else {
    // Continuous speed command (e.g., X+300, Y-150)
    // Parse direction and speed
    char dir = param.charAt(0);
    String speedStr = param.substring(1);
    int speed = speedStr.toInt();

    if (dir == '-') speed = -speed;
    else if (dir != '+') {
      // Invalid direction char, ignore command
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
