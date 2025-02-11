import json
import base64
import os
import boto3

#Environment variables AWS setup
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")

#Environment variables API values
PRECIPITATION_PROBABILITY_THRESHOLD = int(os.environ.get('PRECIPITATION_PROBABILITY', 10))
WIND_SPEED_THRESHOLD = int(os.environ.get('WIND_SPEED', 10))
WIND_GUST_THRESHOLD = int(os.environ.get('WIND_GUST', 10))
RAIN_INTENSITY_THRESHOLD = int(os.environ.get('RAIN_INTENSITY', 10))

#Seting up sns client
sns_client = boto3.client("sns")

#Seting up lambda function
def lambda_handler(event, context):
    if "Records" not in event:
        print("No records found in the event")
        
        return {
            "statusCode":400,
            "body":json.dumps("No records found in the event")
        }
    
    for record in event["Records"]:

        payload = base64.b64decode(record["kinesis"]["data"]).decode("utf-8")
        data = json.dumps(payload)

        precipitation_probability = data['data']['values'].get('precipitationProbability', 0)
        wind_speed = data['data']['values'].get('windSpeed', 0)
        wind_gust = data['data']['values'].get('windGust', 0)
        rain_intensity = data['data']['values'].get('rainIntensity', 0)

        if (precipitation_probability >= PRECIPITATION_PROBABILITY_THRESHOLD or
            wind_speed >= WIND_SPEED_THRESHOLD or
            wind_gust >= WIND_GUST_THRESHOLD or 
            rain_intensity >= RAIN_INTENSITY_THRESHOLD):

            message = (
                f"Probabilidade de chuva: {precipitation_probability}%\n"
                f"Velocidade do vento: {wind_speed}%\n"
                f"Rajada de vento: {wind_gust}%\n"
                f"Intensidade da chuava: {rain_intensity}%\n"
            )

            reponse = sns_client.publish(
                TopicArn = SNS_TOPIC_ARN,
                Message = message,
                Subject = "Alerta Meteorologico",
            )

            print(f"SNS response: {reponse}")

        return{
            "statusCode" : 200,
            "body" : json.dumps("Mensagem enviada ao SNS com sucesso.")
        }