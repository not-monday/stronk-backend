# ERROR CODES
UNEXPECTED_ERROR_CODE = "UNEXPECTED_ERROR"
UNAUTHORIZED_ERROR_CODE = "UNAUTHORIZED_ERROR"
BAD_REQUEST_ERROR_CODE = "BAD_REQUEST_ERROR"
CONFLICT_ERROR_CODE = "RESOURCE_CONFLICT_ERROR"
NOT_FOUND_ERROR_CODE = "NOT_FOUND_ERROR"

# ERROR MESSAGES
INVALID_WORKOUT_START_TIME = "Workout cannot be scheduled in the past."
UNEXPECTED_ERROR_MSG = "An unexpected error has occured."
EXERCISE_NOT_FOUND_MSG = "Exercise not found."
PROGRAM_NOT_FOUND_MSG = "Program not found."
USER_NOT_FOUND_MSG = "User not found."
WORKOUT_NOT_FOUND_MSG = "Workout not found."
WORKOUT_EXERCISE_NOT_FOUND_MSG = "Workout exercise not found."
WEIGHT_NOT_FOUND_MSG = "Weight not found."
UNAUTHORIZED_ACTION_OR_RESOURCE_MSG = "User does not have access to this resource or action."

DATABASE_ERROR_MSG = "Database Error"

# ERROR BODY RESPONSE
ERROR_RESPONSE_BODY = {
    'code': -1,
    'message': ""
}

DELETED_USER_ID = "deleted"
DEV_USER_ID = "user_id_1"
