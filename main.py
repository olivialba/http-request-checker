import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
from request_class import RequestInfo
from requests.exceptions import MissingSchema

dpg.create_context()
dpg.create_viewport(title='Request Tester', height=500, width=920)

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
HEADER = 'header'
COOKIE = 'cookie'

headers_items = [['header_name_one', 'header_info_one']]
cookies_items = [['cookie_name_one', 'cookie_info_one']]

# GUI
def space(height: int):
    dpg.add_spacer(height=height)

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

# REQUEST
def get_request_info_from(tag_list: list):
    dict = {}
    for item in tag_list:
        detail = dpg.get_value(item[1]).strip()
        if detail != '': dict[dpg.get_value(item[0])] = detail
    return dict

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
    

# MAIN WINDOW
with dpg.window(tag="main_window"):
    with dpg.table(header_row=False, borders_innerH=True, borders_innerV=True, 
                   borders_outerH=True, borders_outerV=True):
        dpg.add_table_column(width_fixed=True, init_width_or_weight=400)
        dpg.add_table_column()
        with dpg.table_row():
            with dpg.group():
                with dpg.group(indent=10):
                    
                    space(10)
                    with dpg.group(horizontal=True):
                        dpg.add_text("URL: ")
                        dpg.add_input_text(hint='Input Request URL', tag='request_url', width=-1)
                    space(10)
                    dpg.add_radio_button(['GET', 'POST'], default_value='GET', tag='request_type')

                    # HEADER
                    space(20)
                    dpg.add_text("Header:")
                    with dpg.group(indent=15, horizontal=True):
                        dpg.add_input_text(default_value='User-Agent', tag='header_name_one', width=100)
                        dpg.add_input_text(hint='...', default_value=USER_AGENT, tag='header_info_one', width=-1)
                        # Add to Header
                    dpg.add_spacer(height=2, tag='add_header_space')
                    dpg.add_button(indent=15, label='+ Header', callback=add_input_row, user_data=HEADER)
                    
                    # COOKIE
                    space(20)
                    dpg.add_text("Header > Cookies:")
                    with dpg.group(indent=15, horizontal=True):
                        dpg.add_input_text(default_value='cf_clearance', tag='cookie_name_one', width=100)
                        dpg.add_input_text(hint='...', tag='cookie_info_one', width=-1)
                        # Add to Header > Cookie
                    dpg.add_spacer(height=2, tag='add_cookie_space')
                    dpg.add_button(indent=15, label='+ Cookie', callback=add_input_row, user_data=COOKIE)

                space(20)
                dpg.add_button(label='Send Request', tag='send_request_button',callback=send_request, width=-1, height=30)
                space(10)
            
            # Response
            with dpg.group(indent=10):
                space(10)
                dpg.add_text("URL: ", tag='response_url')
                with dpg.group(horizontal=True):
                    dpg.add_text("Response Status: ")
                    dpg.add_text("", tag='response_status_code')
                with dpg.group(horizontal=True):
                    dpg.add_text("Reason: ")
                    dpg.add_text("", tag='response_reason')
                dpg.add_text("Elapsed: ", tag='response_time')
                space(5)
                
                dpg.add_text("Info")
                dpg.add_text("Type: ", indent=25, tag='response_content_type', wrap=300)
                with dpg.group(horizontal=True):
                    with dpg.tree_node(label="Text: ", indent=5):
                        dpg.add_text("", tag='response_text', wrap=350)
                
                
#demo.show_demo()

# Setup
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main_window", True)
dpg.start_dearpygui()
dpg.destroy_context()