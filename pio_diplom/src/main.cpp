#include <WiFi.h>
#include <ESPmDNS.h>
#include <WiFiUdp.h>
#include <ArduinoOTA.h>
#include <ArduinoHttpClient.h>
#include <ArduinoJson.h>

const char* ssid = "GalaxyS20";
const char* password = "itqw5934";
WiFiClient wifi;



#include <DHT.h>
#define DHTPIN 17
#define DHTTYPE DHT11
DHT dht2(DHTPIN, DHTTYPE);JsonDocument doc2; String postData2;

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

	dht2.begin();

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
  
  float f = dht2.readHumidity(); doc2["mac_address"] = mac; doc2["sensor_type"] = "Влажность"; doc2["output_data"] = f;serializeJson(doc2, postData2);
client.post("/data_records/send_data", contentType, postData2);client.stop();delay(1000);
  
  delay(1000);
}