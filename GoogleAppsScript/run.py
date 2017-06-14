import google_execution

send_info = google_execution.main('getSendInfo') 
form_link = send_info['formUrl']
respondents = send_info['respondents']

