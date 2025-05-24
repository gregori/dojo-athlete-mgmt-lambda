*** Settings ***
Library    Boto3Library

*** Variables ***
${URL}  http://localhost:4566
${DATA}  {"key1": "value1", "key2": "value2"}

*** Test Cases ***
Lambda Test
    Create Session  Lambda  ${URL}
    POST    Lambda  /2015-03-31/functions/arn:aws:lambda:us-east-1:000000000000:function:dojo-athlete-mgmt-lambda/invocations data=${DATA}
    Should Be Equal As Strings  ${RESPONSE.status_code}  200