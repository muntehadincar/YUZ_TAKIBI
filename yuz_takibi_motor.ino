#include <Stepper.h>

const int stepsPerRevolution = 2048; // Step motorun adım sayısı

Stepper myStepper(stepsPerRevolution,8,10,9,11); //Pin numaralarını ayarladık.

void setup() {
  Serial.begin(9600);
  myStepper.setSpeed(10); // Motorun hızı
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == 'L') {
      myStepper.step(stepsPerRevolution / 8); // Saat yönünde belirli bir adım ilerledi.
    } else if (command == 'R') {
      myStepper.step(-stepsPerRevolution /8); // Saat yönünün tersine belirli bir adım ilerledi. 
    }
  }
}
