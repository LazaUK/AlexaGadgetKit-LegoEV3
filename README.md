# Alexa Gadget Kit: Integration of Lego EV3 Brick with Amazon Echo
## Pre-requisites:
- You should have access to SmartEdge Agile device from [AVNET](https://www.avnet.com/wps/portal/us/solutions/iot/building-blocks/smartedge-agile) and Octonion;
- You should train the model in [Brainium portal](https://www.brainium.com/) and deploy them to SmartEdge Agile device;
- You should also have smartphone or Raspberry Pi with Brainium Gateway app installed to enable data streaming from device over to the portal





## High-Level Architecture
This is high-level architecture with all the main blocks of the target solution.
![ha-architecture](Brainium_Schematics.png)
Training motion recognition and sync into Brainium portal is one of the pre-requisites. To learn more about that process, please refer to the Brainium [documentation](https://www.brainium.com/gesture-control)

Parts below will describe how to enable MQTT client to retrieve data, upload it into Azure IoT Hub and the use scripting within Azure Stream Analytics to detect anomalies.
## MQTT Client
Provided [Python script](brainium_mqtt_git.py) above allows the use MQTT protocol for the interaction with both Brainium API (to subscribe to the motion events) and also to upload then some of the details into Azure IoT Hub's endpoint for the further processing.

You should have Azure IoT Hub installed in your Azure subscription to retrieve its connection details. In the similar way, you need to check your profile settings in the Brainium portal to get API connection secrets. All these details are required to set the values for the following variables in Python file:
- CONNECTION_STRING
- MQTT_PASSWORD
- USER_ID
- DEVICE_ID

> Don't forget to download [SSL certificate](https://brainium.blob.core.windows.net/public/docs/cacert.crt) as advised in Brainium API documentation and save it to the same directory where you would keep provided Python file.

You may also need to install 2 additional libraries for Python:
> Paho MQTT client+server package
```
pip install paho-mqtt
```
> Azure IoT Hub client package
```
pip install azure-iothub-device-client
```
If successful, after running the script you should get confirmation on successful connection to the Brainium API MQTT endpoint. And once trained gesture is recognised on the SmartEdge device, MQTT should be able to retrieve a message in the [format like this](DataStream_Brainium.json) from Brainium portal and then upload new messsages in the [format like that](DataStream_AzureIoT.json) into Azure IoT Hub's secure endpoint.
## Azure Stream Analytics
Please, setup new instance of ASA, add your IoT Hub as an input (in this code called "MyStream") and PowerBI as an output (in this code - "MyBI") to define data flow.

Then copy-paste the following [SQL script](ASA_SmartEdge.sql) into ASA's query section. It would learn from the last 120 patterns of the motions in 2 min windows and provide you with it's scoring and indication of the possible anomalies. Again, as an example here we look at both peaks and drops. Don't forget to **start** your Stream Analytics job when ready.
```
WITH AnomalyDetectionStep AS
(
    SELECT
        EVENTENQUEUEDUTCTIME AS time,
        CAST(probability AS float) AS probability,
        AnomalyDetection_SpikeAndDip(probability, 95, 120, 'spikesanddips')
            OVER(LIMIT DURATION(second, 120)) AS SpikeAndDipScores
    FROM MyStream
)
SELECT
    time,
    probability,
    50 as midValue,
    CAST(GetRecordPropertyValue(SpikeAndDipScores, 'Score') AS float) AS
    SpikeAndDipScore,
    CAST(GetRecordPropertyValue(SpikeAndDipScores, 'IsAnomaly') AS bigint) AS
    IsSpikeAndDipAnomaly
INTO MyBI
FROM AnomalyDetectionStep
```
For the provided scenario, drops can be characterised as unintended gestures from the quality control staff if the probability guess at the edge is relatively low comparing to the previous examples.

Another scenario which can be enabled here using **_AnomalyDetection_ChangePoint_** function, which would detect increase in the number of defects identified and thus trigger an alarm, indicating significant drop in the production output's quality, highlighting potential issue with the monitored equipment.
## PowerBI Dashboard
Once you get data in PowerBI, you can create a new report and publish it in a dashboard.
![pbi-dashboard](PowerBI_Dashboard.png)
This results shows the motions detected overtime, and detect anomalies in the peaks and drops.
## Working model - Demo
You can find short demo of working solution here on [YouTube](https://youtu.be/Gui9sqyglFw)

