import dearpygui.dearpygui as dpg
from requests.exceptions import MissingSchema
from src.request_class import RequestInfo


USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
HEADER = 'header'
COOKIE = 'cookie'

headers_items = [0]
cookies_items = [0]



######### GUI #########

# Add new row for Headers or Cookies
def add_input_row(sender, app_data, userdata):
    if userdata == HEADER: items_list = headers_items
    elif userdata == COOKIE: items_list = cookies_items
    else: return
    
    count = items_list[0] + 1
    tag_row = f'row_{userdata}_{count}'
    tag_name = f'{userdata}_name_{count}'
    tag_info = f'{userdata}_info_{count}'
    with dpg.group(indent=15, horizontal=True, before=f'add_{userdata}_space', tag=tag_row):
        dpg.add_button(label="-", callback=delete_input_row, user_data=(tag_row, tag_name, items_list))
        dpg.add_input_text(hint='..', tag=tag_name, width=100)
        dpg.add_input_text(hint='...', tag=tag_info, width=-1)
    items_list.append([tag_name, tag_info])
    items_list[0] = count

# Delete row for Headers or Cookies
def delete_input_row(sender, app_data, userdata):
    tag_row, tag_name, items_list = userdata
    dpg.delete_item(tag_row)
    for item in items_list:
        if item == items_list[0]: 
            continue
        if item[0] == tag_name:
            items_list.remove(item)
            return

# Add space in GUI
def space(height: int):
    dpg.add_spacer(height=height)



####### REQUEST #######

# Get Request info (headers and cookies)
def get_request_info_from(items_list: list):
    dict = {}
    for item in items_list:
        if item == items_list[0]: 
            continue
        detail = dpg.get_value(item[1]).strip()
        if detail != '': dict[dpg.get_value(item[0])] = detail
    return dict

# Display response
def response_request(response: RequestInfo):
    # Url
    dpg.set_value('response_url', f'URL: {response.url}')
    # Response Status and Reason
    dpg.set_value('response_status_code', f'{response.status_code}')
    dpg.set_value('response_reason', f'{response.reason}')
    dpg.configure_item('response_status_code', color=response.color)
    dpg.configure_item('response_reason', color=response.color)
    # Other Info
    dpg.set_value('response_time', f'Elapsed: {response.response_time}s')
    dpg.set_value('response_content_type', f'Type: {response.content_type}')
    dpg.set_value('response_text', f'{response.response.text}')

# Send Request
def send_request():
    request_url = dpg.get_value('request_url').strip()
    request_type = dpg.get_value('request_type').strip()
    if not request_url.startswith('http') or (request_type != 'GET' and request_type != 'POST'): return
    
    try:
        empty_response()
        dpg.disable_item('send_request_button')
        response = RequestInfo(
                            url=request_url,
                            type=request_type,
                            header=get_request_info_from(headers_items),
                            cookies=get_request_info_from(cookies_items),
                            )
    except MissingSchema:
        dpg.set_value('response_url', f'URL: Invalid Url')
        return
    finally:
        dpg.enable_item('send_request_button')
    
    response_request(response)

def empty_response():
    # Url
    dpg.set_value('response_url', 'URL:')
    # Response Status and Reason
    dpg.set_value('response_status_code', '')
    dpg.set_value('response_reason', '')

    # Other Info
    dpg.set_value('response_time', 'Elapsed: ')
    dpg.set_value('response_text', '')
    dpg.set_value('response_content_type', 'Type: ')
