### API


Junction provides API to access information about the conference, schedule, and feedback. The API is for mobile clients to assist conference attendees. All the request and response format is `application/json`.

- Demo site: `http://junctiondemo.herokuapp.com/`


### Conference - List

- Endpoint: `/api/v1/conferences/`

- Allowed Method: `GET`.

- Returns all conferences. There is no pagination.

- Sample Response:

```

[ { "id": 5, "name": "PyCon India 2016", "slug": "2016", "description": "...", "start_date": "2016-09-23", "end_date": "2016-09-25", "status": "Proposal submission closed", "venue": "http://in.pycon.org/cfp/api/v1/venues/2/" },]

```

- `venue`  key holds URL of the venue details.

### Venue - List

- Endpoint: `/api/v1/venues/`

- Allowed Methods: `GET`

- List all the venues.

- Sample Response:

```

[ { "id": 1, "name": "Nihmans", "address": " Hosur Road, Lakkasandra, Behind Bus Stop, Bengaluru, Karnataka 560030", "latitude": "12.943112200000000", "longitudes": "77.5968643000000000" },  ]

```

### Venue - Detail

- Endpoint: `/api/v1/venues/<id>/`

- Allowed Method: `GET`

- Return specific venue details.

- Sample Response:

```

{ "id": 1, "name": "Nihmans", "address": " Hosur Road, Lakkasandra, Behind Bus Stop, Bengaluru, Karnataka 560030", "latitude": "12.943112200000000", "longitudes": "77.5968643000000000" }

```

### Room - List

- Endpoint: `/api/v1/rooms/`

- Allowed Method: `GET`

- List all rooms of all venues..

- Sample Response:

```

[ { "id": 4, "name": "Buffet Area", "venue": "http://in.pycon.org/cfp/api/v1/venues/1/", "note": "Left end of the ground floor" },..]

```

### Room - Venue specific

- Endpoint: `/api/v1/rooms/?venue=<id>`

- Display list of rooms in the venue.

- Allowed Method: `GET`

- Sample Response:

```

[ { "id": 4, "name": "Buffet Area", "venue": "http://in.pycon.org/cfp/api/v1/venues/1/", "note": "Left end of the ground floor" }, { "id": 3, "name": "Room 3", "venue": "http://in.pycon.org/cfp/api/v1/venues/1/", "note": "Ground Floor" }, { "id": 2, "name": "Room 2", "venue": "http://in.pycon.org/cfp/api/v1/venues/1/", "note": "Ground Floor" }, { "id": 1, "name": "Room 1", "venue": "http://in.pycon.org/cfp/api/v1/venues/1/", "note": "Ground Floor" } ]

```

### Schedule: List

- Endpoint: `/api/v1/schedules/`

- Allowed Methods: `GET`

- All the schedule items of all conferences.

- Sample Response:

```

{ "2015-10-04": { "08:30:00 - 09:15:00": [ { "conference": "http://in.pycon.org/cfp/api/v1/conferences/1/", "session": { "description": "" }, "room_id": 4, "end_time": "09:15:00", "event_date": "2015-10-04", "start_time": "08:30:00", "type": "Break", "id": 37, "name": "Registration & Breakfast" } ], "09:30:00 - 10:15:00": [ { "conference": "http://in.pycon.org/cfp/api/v1/conferences/1/", "session": { "description": "" }, "room_id": 1, "end_time": "10:15:00", "event_date": "2015-10-04", "start_time": "09:30:00", "type": "Talk", "id": 38, "name": "Keynote - Nicholas H.Tollervey" } ],

```

- Response data keys are conference day date and its schedule grouped by time.

- `2015-10-04` - Conference day date.

- `08:30:00 - 09:15:00` - Start of the session - End of the session.

- `session` dictionary contains details about the session.

- `type`: Type of the session like `break, lunch, talk, workshop` etc ...

- `room_id`: Place of the session. The Client should use API or cached data to fetch room name.

### Schedule: List of sessions for the conference

- Endpoint: `/api/v1/schedules/?conference=<conference_id>`

- Allowed Methods: `GET`

- All the schedule items of the conference.

- Sample Response:

```

{ "2015-10-04": { "08:30:00 - 09:15:00": [ { "conference": "http://in.pycon.org/cfp/api/v1/conferences/1/", "session": { "description": "" }, "room_id": 4, "end_time": "09:15:00", "event_date": "2015-10-04", "start_time": "08:30:00", "type": "Break", "id": 37, "name": "Registration & Breakfast" } ], "09:30:00 - 10:15:00": [ { "conference": "http://in.pycon.org/cfp/api/v1/conferences/1/", "session": { "description": "" }, "room_id": 1, "end_time": "10:15:00", "event_date": "2015-10-04", "start_time": "09:30:00", "type": "Talk", "id": 38, "name": "Keynote - Nicholas H.Tollervey" } ],

```

### Device - Register

- Endpoint: `/api/v1/devices/`

- Allowed Method: `POST`

- Junction accepts feedback via API. We support anonymous feedback, but the device registration is mandatory.  Registered device can only submit the feedback.

- Payload: `{'uuid': 'uuid-1'}`.

- Response: If UUID exists status code is `400`  else the status code is `201` with data.

### Feedback Questions - List

- Endpoint: `/api/v1/feedback_questions/?conference_id=<id>`

- Allowed Method: `GET`

- Fetch all feedback questions for the conference.

- Sample Response:

```{ "Workshop": { "text": [ { "schedule_item_type": "Workshop", "is_required": false, "type": "text", "id": 2, "title": "Any other feedback for workshop ?" } ], "choice": [ { "title": "Does the speaker have experience on the subject?", "schedule_item_type": "Workshop", "allowed_choices": [ { "id": 15, "value": 2, "title": "Good" }, { "id": 14, "value": 1, "title": "Ok" }, { "id": 13, "value": 0, "title": "Bad" } ], "is_required": true, "type": "choice", "id": 5 }, { "title": "How hands on was the workshop ?", "schedule_item_type": "Workshop", "allowed_choices": [ { "id": 6, "value": 2, "title": "Good" }, { "id": 5, "value": 1, "title": "Ok" }, { "id": 4, "value": 0, "title": "Bad" } ], "is_required": true, "type": "choice", "id": 2 }, { "title": "How was the content ?", "schedule_item_type": "Workshop", "allowed_choices": [ { "id": 3, "value": 2, "title": "Good" }, { "id": 2, "value": 1, "title": "Ok" }, { "id": 1, "value": 0, "title": "Bad" } ], "is_required": true, "type": "choice", "id": 1 } ] }, "Talk": { "text": [ { "schedule_item_type": "Talk", "is_required": false, "type": "text", "id": 1, "title": "Any other feedback for the talk ?" } ], "choice": [ { "title": "Does the speaker have experience on the subject?", "schedule_item_type": "Talk", "allowed_choices": [ { "id": 18, "value": 2, "title": "Good" }, { "id": 17, "value": 1, "title": "Ok" }, { "id": 16, "value": 0, "title": "Bad" } ], "is_required": true, "type": "choice", "id": 6 }, { "title": "How was the presentation ?", "schedule_item_type": "Talk", "allowed_choices": [ { "id": 12, "value": 2, "title": "Good" }, { "id": 11, "value": 1, "title": "Ok" }, { "id": 10, "value": 0, "title": "Bad" } ], "is_required": true, "type": "choice", "id": 4 }, { "title": "How was the content ?", "schedule_item_type": "Talk", "allowed_choices": [ { "id": 9, "value": 2, "title": "Good" }, { "id": 8, "value": 1, "title": "Ok" }, { "id": 7, "value": 0, "title": "Bad" } ], "is_required": true, "type": "choice", "id": 3 } ] } }

```

- Response data keys are session types. `Workshop` and `Talk` session type questions are values of the respective key. Each of the session types contains two keys, `text` and `choice`. `text` dictionary contains text type questions and `choice` dictionary contains choice based questions. Both the question type has some common fields. `id` is the unique identifier of the question. `title` is the displayable text of the question. `is_required` is the boolean field, `true` means feedback should have an answer for the item. `choice` questions have `allowed_choices`, which contains allowed values. Each item is a dictionary containing `id`, `title`, `value`. Use `title` to display the answer.

### Feedback submission

- Endpoint: `/api/v1/feedback`

- Allowed Methods: `POST`.

- Header: 'Token: <registered_device_uuid>`.

- Sample Payload:

```{'text': [{'text': 'Ok', 'id': 1}], 'schedule_item_id': 1, 'choices': [{'id': 1, 'value_id': 1}]}

```

- `schedule_item_id` is the `id` of the session accepting feedback. The payload contains `text` and `choices` answers.

- When request succeeds, the status code is `200` and when the request fails, the status code is `400` or `403`. When the input data is incorrect code is `400` and `403` when device token is missing.

- Sample success response: 201

```

{'text': [{'text': 'Ok', 'id': 1}], 'schedule_item_id': 1, 'choices': [{'id': 1, 'value_id': 1}]}

```

- Sample failure response: 400

```

{'choices': [{u'non_field_errors': [u"The multiple choice value isn't associated with question"]}]}

```

- Sample failure response: 403

```

{u'detail': u'Authentication credentials were not provided.'}

```
