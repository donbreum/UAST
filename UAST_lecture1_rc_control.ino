#include <TimerOne.h>

#define MOTOR_PIN 9
#define SERVO_PIN 10 // we either use pin for servo
#define LED_PIN 10   // or for visualizing LED with RC signal

// Servo and ESC RC signal, else we will use timer for visualizing LED
// uncomment to use pin 10 for LED instead of servo
#define USE_SERVO_AND_ESC 

bool armed = false; // used to check if we have armed to UAV
 
void setup(){
  Serial.begin(115200);
  Serial.print("Setup....");

   // set a timer of length 10000 microseconds (or 0.02 sec - or 50Hz)
  Timer1.initialize(20000);
  // initially duty is set 0
  Timer1.pwm(MOTOR_PIN, 0); 

#ifdef USE_SERVO_AND_ESC
  // initially duty is set to middle point (1,5 ms for this value)
  Timer1.pwm(SERVO_PIN, 75);
#else
  Timer1.pwm(LED_PIN,500);
  // used for visualizing with builtin LED
  pinMode(LED_BUILTIN, INPUT); 
#endif

  Serial.println("Setup done!");
}
 
void loop(){
     // send data only when you receive data:
    while(Serial.available()) {
      String data= Serial.readString();// read the incoming data as string
      select_action(data);
    }
}

void select_action(String data){
  
  int data_size = data.length();
  String action_number = data.substring(0,1);
  String value_for_motors = data.substring(1,data_size);
  Serial.print("Action chosen: ");
  Serial.println(action_number);
  
  switch (action_number.toInt()) {
    case 1:
      if(armed)
        set_motor_speed(value_for_motors.toInt()); // set duty from 0 - 100%, uses pin 9
      else
        Serial.println("You need to arm the UAV before applying throttle");
      break;
    case 2: // arm 
      arm(true);
      break;
    case 3: // disarm
      arm(false);
      break;
    case 4: // calibrate esc
      calibrate_esc();
      break;
    case 5: // set servo position, uses pin 10
      set_servo_position(value_for_motors.toInt());
      break;
    default:
      Serial.println("Wrong action command, use first number to specify action followed by the desired value\n"
      "Actions:\n"
      "1=Set duty cycle between 0 to 100%(e.g. type \"1100\" for 100%) \n"
      "2=Arm (no need to specify value)\n"
      "3=Disarm (no need to specify value)"
      "4=Calibrate ESC (no need to specify value)\n"
      "5=Set servo positition (from -100 to 100%)");
  }
}

void set_motor_speed(int duty){
  int clamped_value = clamp_value(duty, 0,90);
  if(clamped_value > 10){ // need at least 10% of throttle before spinning)
     int duty_corrected_value = 60+(clamped_value*0.4); // corrected value to match signal width
       
#ifdef USE_SERVO_AND_ESC
     set_onboard_led_value(duty);
#endif
     Timer1.pwm(MOTOR_PIN,duty_corrected_value);
     Serial.print("Duty set to: ");
     Serial.print(duty);
     Serial.println("%");
  }else{
    Timer1.pwm(MOTOR_PIN,0);
  }
}

#ifdef USE_SERVO_AND_ESC
void set_onboard_led_value(int duty){
  Timer1.pwm(LED_PIN,duty*10);
}
#endif

void set_servo_position(int pos){
  int clamped_position = clamp_value(pos, -90,90);
  int pos_corrected = 75 +(clamped_position*0.4); // corrected signal to match +- signal width
  Timer1.pwm(SERVO_PIN,pos_corrected);
  Serial.print("Servo position set to: ");
  Serial.print(clamped_position);
  Serial.println(" degree");
}

void arm(bool arm){
  armed = arm; // used both to arm and disarm
  if(arm)
    Serial.println("ARMED");
  else
    Serial.println("DISARMED");
}

void calibrate_esc(){
   // Set max trottle followed by minimum throttle. Same as swiping stick up and down to calibrate signal range
  Serial.print("Calibrating...");
  set_motor_speed(100);
  delay(100);
  set_motor_speed(11);
  Serial.println("Calibrating done");
}

int clamp_value(int value, int low_threshold,int high_threshold){
  if(value > high_threshold)// clamp to max 100%
    value = high_threshold;
  else if(value < low_threshold) // clamp to min -100%
    value = low_threshold;
}



