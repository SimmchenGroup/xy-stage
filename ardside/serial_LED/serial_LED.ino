const int yellowPin = 8;  // LED for 'X' command
const int pinkPin = 9;    // LED for 'Y' command

String inputString = "";
bool commandReady = false;

void setup() {
  pinMode(yellowPin, OUTPUT);
  pinMode(pinkPin, OUTPUT);
  digitalWrite(yellowPin, LOW);
  digitalWrite(pinkPin, LOW);

  Serial.begin(115200);
  inputString.reserve(20);
}

void loop() {
  // Read incoming serial characters
  while (Serial.available()) {
    char inChar = (char)Serial.read();

    if (inChar == '\n' || inChar == '\r') {
      commandReady = true;
    } else {
      inputString += inChar;
    }
  }

  if (commandReady) {
    handleCommand(inputString);
    inputString = "";
    commandReady = false;
  }
}

void handleCommand(String cmd) {
  Serial.print(cmd);
  Serial.print("  ::  ");
  cmd.trim();

  if (cmd.length() < 3) return;

  char axis = cmd.charAt(0);
  char sign = cmd.charAt(1);
  int duration = cmd.substring(2).toInt();

  if (duration <= 0 || (axis != 'X' && axis != 'Y') || (sign != '+' && sign != '-')) return;

  String dirStr = (sign == '+') ? "positive" : "negative";
  Serial.print("Axis: ");
  Serial.print(axis);
  Serial.print(" | Direction: ");
  Serial.print(dirStr);
  Serial.print(" | Duration: ");
  Serial.print(duration);
  Serial.println(" ms");

  // Blink the relevant LED
  if (axis == 'X') {
    digitalWrite(yellowPin, HIGH);
    delay(duration);
    digitalWrite(yellowPin, LOW);
  } else if (axis == 'Y') {
    digitalWrite(pinkPin, HIGH);
    delay(duration);
    digitalWrite(pinkPin, LOW);
  }
}
