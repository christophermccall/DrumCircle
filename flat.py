# attempt 2
import requests
from env import flat_key
# API Key and Headers

headers = {
    'Authorization': f'Bearer {flat_key}',
    'Content-Type': 'application/json'
}

# Score data in JSON
score_data = {
  "title": "Test Score2",
  "privacy": "public",
  "builderData": {
    "scoreData": {
      "fifths": 7,
      "nbBeats": 2,
      "beatType": 4,
      "instruments": [
        {
          "group": "strings",
          "instrument": "hq-violin"
        }
      ]
    },
    "layoutData": {
      "notesSpacingCoeff": 2,
      "lengthUnit": "cm",
      "pageHeight": 29.7,
      "pageWidth": 21,
      "pageMarginTop": 1.5,
      "pageMarginBottom": 1.5,
      "pageMarginLeft": 2.5,
      "pageMarginRight": 2.5
    }
  }
}

#     },
#     "parts": [{
#         "id": "snare",
#         "measures": [
#             {"index": 0, "voices": [{"notes": [{"pitch": {"step": "C", "octave": 5}, "duration": 1, "type": "quarter"} for _ in range(4)]}]},
#             {"index": 1, "voices": [{"notes": [{"pitch": {"step": "C", "octave": 5}, "duration": 1, "type": "quarter"} for _ in range(4)]}]},
#             {"index": 2, "voices": [{"notes": [{"pitch": {"step": "C", "octave": 5}, "duration": 1, "type": "quarter"} for _ in range(4)]}]},
#             {"index": 3, "voices": [{"notes": [{"pitch": {"step": "C", "octave": 5}, "duration": 1, "type": "quarter"} for _ in range(4)]}]}
#         ]
#     }]
#
# }

# URL for the Flat API endpoint to create scores
url = 'https://api.flat.io/v2/scores'
score_url = None

# Create the score
response = requests.post(url, headers=headers, json=score_data)
if response.status_code == 200:
    print("Score created successfully.")
    score_url = response.json()['htmlUrl']
    print(score_url)
    # for item in score_url:
    #     print("Score URL:", item)
else:
    print("Failed to create score:", response.status_code, response.text)




#Assuming score_url is retrieved from the score creation step
export_url = f'{score_url}/exports/pdf'
pdf_response = requests.post(export_url, headers=headers)

if pdf_response.status_code == 200:
    with open('snare_drum_score.pdf', 'wb') as f:
        f.write(pdf_response.content)
    print("PDF exported and saved successfully.")
else:
    print("Failed to export PDF:", pdf_response.status_code, pdf_response.text)

















# attemp1




# import flat_api
# from flat_api.models.score_creation_builder_data import ScoreCreationBuilderData
# from flat_api.models.score_creation import ScoreCreation
#
# from pprint import pprint
# import flat_api
# from flat_api.api import account_api, score_api
#
# configuration = flat_api.Configuration(
#     access_token='2139f26ac12d7b0f3f13d37669f80572f4d67ca63a65880f22f6057cb7c0368559d165e534c4b428d3078621082718ca2fb30aa0bd69993de14f7fd8510b40e0',
#
# )
#
# # Enter a context with an instance of the API client
# with flat_api.ApiClient(configuration) as api_client:
#     # Create an instance of the API class
#     api_instance = account_api.AccountApi(api_client)
#     score_instance = score_api.ScoreApi(api_client
#                                     score_data )
#     new_score = ScoreCreation()
#
#     try:
#         # Get current user account
#         api_response = score_instance.create_score(new_score)
#         pprint(api_response)
#     except flat_api.ApiException as e:
#         print("Exception when calling AccountApi->get_authenticated_user: %s\n" % e)