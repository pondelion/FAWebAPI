import os

from fastapi_cloudauth.cognito import Cognito, CognitoCurrentUser


auth = Cognito(
    region=os.environ["AWS_DEFAULT_REGION"],
    userPoolId=os.environ["AWS_COGNITO_USERPOOL_ID"],
    client_id=os.environ["AWS_COGNITO_CLIENT_ID"],
)


get_current_user = CognitoCurrentUser(
    region=os.environ["AWS_DEFAULT_REGION"],
    userPoolId=os.environ["AWS_COGNITO_USERPOOL_ID"],
    client_id=os.environ["AWS_COGNITO_CLIENT_ID"],
)
