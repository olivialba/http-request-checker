import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
from src.utils import *


dpg.create_context()
dpg.create_viewport(title='Request Tester', height=500, width=920)


# MAIN WINDOW
with dpg.window(tag="main_window"):
    with dpg.table(header_row=False, borders_innerH=True, borders_innerV=True, 
                   borders_outerH=True, borders_outerV=True):
        dpg.add_table_column(width_fixed=True, init_width_or_weight=400)
        dpg.add_table_column()
        with dpg.table_row():
            with dpg.group():
                with dpg.group(indent=10):
                    
                    # REQUEST
                    space(10)
                    with dpg.group(horizontal=True):
                        dpg.add_text("URL: ")
                        dpg.add_input_text(hint='Input Request URL', tag='request_url', width=-1)
                    space(10)
                    dpg.add_radio_button(['GET', 'POST'], default_value='GET', tag='request_type')

                    # HEADER
                    space(20)
                    dpg.add_text("Header:")
                        # Add to Header
                    dpg.add_spacer(height=2, tag='add_header_space')
                    dpg.add_button(indent=15, label='+ Header', callback=add_input_row, user_data=HEADER)
                    
                    # COOKIE
                    space(20)
                    dpg.add_text("Header > Cookies:")
                        # Add to Header > Cookie
                    dpg.add_spacer(height=2, tag='add_cookie_space')
                    dpg.add_button(indent=15, label='+ Cookie', callback=add_input_row, user_data=COOKIE)

                space(20)
                dpg.add_button(label='Send Request', tag='send_request_button',callback=send_request, width=-1, height=30)
                space(10)
                
                # Add first row to Header and Cookies:
                add_input_row(None, None, HEADER)
                dpg.configure_item('header_name_1', default_value='User-Agent')
                dpg.configure_item('header_info_1', default_value=USER_AGENT)
                add_input_row(None, None, COOKIE)
            
            # RESPONSE
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