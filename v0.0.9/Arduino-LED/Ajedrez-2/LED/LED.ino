const int Verde_1 = 2;
const int Verde_2 = 3;
const int Rojo_1 = 4;
const int Rojo_2 = 5;

int i=0;
int h=0;
int reset(){
  digitalWrite(Verde_1,LOW);
  digitalWrite(Verde_2,LOW);
  digitalWrite(Rojo_1,LOW);
  digitalWrite(Rojo_2,LOW);
  Serial.println("Reset");
  h=1;   
}
int win(int Verde,int Rojo)
{
  while (i <= 3){
    digitalWrite(Verde, HIGH);
    digitalWrite(Rojo, HIGH);
    delay(500);
    digitalWrite(Verde, LOW);
    digitalWrite(Rojo, LOW);
    delay(500);
    i++;
  }
  i=0;
}
int option_a()
{
  if (h==1)
      {
        Serial.println("h == 1");
        digitalWrite(Verde_1,LOW);
        digitalWrite(Rojo_1,LOW);
        digitalWrite(Verde_2,HIGH);
        h=2;
      }
  else if (h==2)
      {
        Serial.println("h == 2");
        digitalWrite(Verde_2,LOW);
        digitalWrite(Rojo_2,LOW);
        digitalWrite(Verde_1,HIGH);
        h=1;
      }
  else{ Serial.println("Error");}
}
void setup()
{
  Serial.begin(9600);          
  pinMode(Verde_1, OUTPUT);
  pinMode(Verde_2, OUTPUT);
  pinMode(Rojo_1, OUTPUT);
  pinMode(Rojo_2, OUTPUT);
}
 
void loop()
{
  if (Serial.available()>0)
  {
    char option = Serial.read();
    if(option == 's'){digitalWrite(Verde_1,HIGH);h=1;}
    if(option == 'r'){reset();}
    if(option == 'a'){option_a();}  //La 'a' indica que la jugada es acertada, entonces le toca mover al siguiente
    if (option=='b')                //La 'b' indica que la jugada está mal hecha, por lo que el led rojo del que ha movido se enciende
    {
      if (h==1)
      {
        digitalWrite(Verde_1,LOW);
        digitalWrite(Rojo_1,HIGH);
      }
     else if (h==2)
      {
        digitalWrite(Verde_2,LOW);
        digitalWrite(Rojo_2,HIGH);
      }
     else{ Serial.println("Error");}
    }
    if (option == 'c')
    {
      if (h==1){reset(); win(2, 4);}
      if (h==2){reset(); win(3, 5);}
    }
  }
}
