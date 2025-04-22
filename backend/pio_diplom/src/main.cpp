#include <WiFi.h>
#include <ESPmDNS.h>
#include <WiFiUdp.h>
#include <ArduinoOTA.h>
#include <ArduinoHttpClient.h>
#include <ArduinoJson.h>

const char* ssid = "GalaxyS20";
const char* password = "itqw5934";
WiFiClient wifi;



int GasPin1 = 34;float val3;JsonDocument doc4; String postData4;

void setup() {
  Serial.begin(115200);
  Serial.println("Booting");
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.waitForConnectResult() != WL_CONNECTED) {
	Serial.println("Connection Failed! Rebooting...");
	delay(5000);
	ESP.restart();
  }

	pinMode(GasPin1, INPUT);

   ArduinoOTA
	.onStart([]() {
  	String type;
  	if (ArduinoOTA.getCommand() == U_FLASH)
    	type = "sketch";
  	else // U_SPIFFS
    	type = "filesystem";

  	// NOTE: if updating SPIFFS this would be the place to unmount SPIFFS using SPIFFS.end()
  	Serial.println("Start updating " + type);
	})
	.onEnd([]() {
  	Serial.println("\nEnd");
	})
	.onProgress([](unsigned int progress, unsigned int total) {
  	Serial.printf("Progress: %u%%\r", (progress / (total / 100)));
	})
	.onError([](ota_error_t error) {
  	Serial.printf("Error[%u]: ", error);
  	if (error == OTA_AUTH_ERROR) Serial.println("Auth Failed");
  	else if (error == OTA_BEGIN_ERROR) Serial.println("Begin Failed");
  	else if (error == OTA_CONNECT_ERROR) Serial.println("Connect Failed");
  	else if (error == OTA_RECEIVE_ERROR) Serial.println("Receive Failed");
  	else if (error == OTA_END_ERROR) Serial.println("End Failed");
	});
                                                                                                                                                     	 
  ArduinoOTA.begin();
                                                                                                                                              	 
  Serial.println("Ready");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

}
                                                                                                                                              	 
void loop() {
  ArduinoOTA.handle();
  String mac = WiFi.macAddress();
  HttpClient client = HttpClient(wifi, "192.168.39.9", 8000);
  String contentType = "application/json";
  
  val3 = analogRead(GasPin1);doc4["mac_address"] = mac; doc4["sensor_type"] = "Углекислый газ"; doc4["output_data"] = val3;serializeJson(doc4, postData4);
client.post("/data_records/send_data", contentType, postData4);client.stop();delay(1000);
  
  delay(1000);
}