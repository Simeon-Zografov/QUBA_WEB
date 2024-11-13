import json
from mitmproxy import http, ctx


def load(loader):
    ctx.options.add_option(
        "test_name", str, "", "Name of the test case to determine response modification"
    )


def response(flow: http.HTTPFlow) -> None:
    test_name = ctx.options.test_name
    # Target the specific request URL
    if 'https://cms-qaclm.raseel.city/graphql' in flow.request.url:
        # Decode the JSON body of the response
        body = flow.response.text
        json_data = json.loads(body)
        print("Original Response JSON:", json_data)

        # Check and modify the JSON data
        if test_name == "home_page_test_29":
            if 'data' in json_data and 'events' in json_data['data'] and 'data' in json_data['data']['events']:
                json_data['data']['events']['data'] = []  # Set the events data to an empty list

        # Encode the modified JSON back to the response
        modified_body = json.dumps(json_data)
        print("Modified Response JSON:", modified_body)
        flow.response.text = modified_body  # Update the response with the modified JSON
