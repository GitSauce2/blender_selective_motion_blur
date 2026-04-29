import bpy

def MessengerError(message = "Message", title = "Title", icon = 'ERROR', error = True):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)
    
    print(message)
    
    if error:
        raise ExitSafe

class ExitSafe(Exception):
    pass