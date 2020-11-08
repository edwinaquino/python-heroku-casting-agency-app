# THIS ARRAY IS USED FOR KEEPING CONSISTENT ERROR MESSAGE
assertions_message_arr = {
    "test_401_delete_actor": "Doesnt have valid JSON body",
    "authorization_header_missing": "Authorization header is expected",
    "no_name_provided": "no name provided.",
    "actors_not_in_db": "no actors found in database.",
    "invalid_body": "request does not contain a valid JSON body.",
    "movie_not_found": "Movie not found in database.",
    "permission_not_found": "Permission not found",
    "actor_not_found": "Actor not found",
    "movies_not_found": "Movies not found",
    "permission_no_found_403": "'Permission were not found.'",
    "not_found404": "Not Found",
    "Unprocessable_entity": "Unprocessable entity",
    "missin_bearer": "Authorization missing the Bearer.",
    "token_not_found": "Token was not found.",
    "auth_missing_token": "Authorization header is missing bearer token.",
    "auth_mal_malformed": "Authorization is malformed.",
    "expired_token": "Token already expired.",
    "incorrect_audience":
    "Incorrect claims. Please, check the provided audience.",
    "no_validate_token": "Unable to validate authentication token.",
}
# USAGE: assertions_message_arr['permission_no_found_403']
