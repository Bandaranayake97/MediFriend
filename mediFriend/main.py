from fastapi import Request
from fastapi import FastAPI
from starlette.responses import JSONResponse
from db import get_dbfirstaid, get_dbdoctor, add_apoint, add_apointment

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/")
async def handle_request(request: Request):

    payload = await request.json()
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    queryText = payload['queryResult']['queryText']

    if intent == "FirstAid.get":
        return get_firstAid(parameters)
    if intent == "doctor.get":
        return get_doctor(parameters)
    if intent == "doctor.Apointment":
        return insert_doctor(output_contexts, queryText)
    if intent == "Apointment.add":
        return apointmentAdd(parameters)


def get_firstAid(parameters: dict):

    disease = parameters.get("disease")
    fristaid = get_dbfirstaid(disease)

    if fristaid:
        fulfillment_text = f"{disease} first aid is {fristaid['First_aid']}."
    else:
        fulfillment_text = f"No fisr-aid for {disease}"
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def get_doctor(parameters: dict):
    print("in to get doctor")
    doctor = parameters.get("doctors")
    result_string = str(doctor[0])
    print(result_string)
    doctorDetails = get_dbdoctor(result_string)
    print(doctorDetails)
    if doctor:
        fulfillment_text = f"{result_string} doctor name is {doctorDetails['Doctor_Name']} and doctor contact number is {doctorDetails['Contact_Number']} and availble day {doctorDetails['Date']}. Are you want add apointmet. then mention yes or no."

    else:
        fulfillment_text = f"No doctor for {doctor}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def insert_doctor(output_contexts: dict, queryText: dict):
    # print(output_contexts["parameters"]["doctors"])

    if queryText=="yes":
        doctor = output_contexts[0]["parameters"]["doctors"]
        doctorDetails = add_apoint(doctor)
        print(doctorDetails)
        if doctorDetails:
            fulfillment_text = f"succesfull your apointment. you add apointment for {doctor} doctor name is {doctorDetails['Doctor_Name']}  and availble day {doctorDetails['Date']}  ."

        else:
            fulfillment_text = f"cant put appointment"
    else:
        fulfillment_text = f"Hi! we are able to provide, 1. doctors details 2.get first-aid 3.add appointment for doctor How can I help you?"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def apointmentAdd(parameters: dict):
    disease = parameters.get("disease")
    print(disease)
    number = add_apointment(disease)

    if number:
        fulfillment_text = f"succesfull your appointment. Your number is {number} and do not forget number ."

    else:
        fulfillment_text = f"you cant put appointment"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })
