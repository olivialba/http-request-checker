import dearpygui.dearpygui as dpg
from request.request_class import RequestInfo
from requests.exceptions import MissingSchema


USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
HEADER = 'header'
COOKIE = 'cookie'

headers_items = [['header_name_one', 'header_info_one']]
cookies_items = [['cookie_name_one', 'cookie_info_one']]



######### GUI #########

# Add space in GUI
def space(height: int):
    dpg.add_spacer(height=height)



####### REQUEST #######

# Update Headers and Cookies
def add_input_row(sender, app_dat, userdata):
    if userdata == HEADER: items = headers_items
    elif userdata == COOKIE: items = cookies_items
    else: return
    
    count = len(items) + 1
    tag_name = f'{userdata}_name_{count}'
    tag_info = f'{userdata}_info_{count}'
    with dpg.group(indent=15, horizontal=True, before=f'add_{userdata}_space'):
        dpg.add_input_text(hint='..', tag=tag_name, width=100)
        dpg.add_input_text(hint='...', tag=tag_info, width=-1)
    items.append([tag_name, tag_info])

# Get Request info (headers and cookies)
def get_request_info_from(tag_list: list):
    dict = {}
    for item in tag_list:
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
    dpg.set_value('response_text', f'{response.response.text}')
    dpg.set_value('response_content_type', f'Type: {response.content_type}')

# Send Request
def send_request():
    request_url = dpg.get_value('request_url').strip()
    request_type = dpg.get_value('request_type').strip()
    if not request_url.startswith('http') or (request_type != 'GET' and request_type != 'POST'): return
    
    try:
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
    
