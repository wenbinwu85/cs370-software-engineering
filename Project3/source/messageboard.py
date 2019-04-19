"""
Overhead Message Board GUI

CS370 Spring 2019
Wenbin Wu
"""

import wx
from alphabet import encodings


class MessageBoard(wx.Frame):
    """GUI simluation for a overhead message board"""
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.SetSize(x=75, y=160, width=1080, height=380)
        self.panel = wx.Panel(self)
        help_text = 'Type a message, press "Enter" to display it, press "Esc" key or the "Clear" button to clear.'
        self.sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel, label=help_text)

        # Message line 1
        self.line1 = wx.TextCtrl(self.panel, id=0, size=(1020, 94), style=wx.TE_MULTILINE)
        self.line1.SetDefaultStyle(wx.TextAttr(wx.WHITE, wx.BLACK))
        self.font = self.line1.GetFont()
        self.font.SetPointSize(34)
        self.line1.SetFont(self.font)
        self.line1.SetBackgroundColour('Black')
        self.line1.Bind(wx.EVT_KEY_DOWN, self.key_pressed)

        # Message line 2
        self.line2 = wx.TextCtrl(self.panel, id=1, size=(1020, 94), style=wx.TE_MULTILINE)
        self.line2.SetDefaultStyle(wx.TextAttr(wx.WHITE, wx.BLACK))
        self.line2.SetFont(self.font)
        self.line2.SetBackgroundColour('Black')
        self.line2.Bind(wx.EVT_KEY_DOWN, self.key_pressed)

        # Message line 3
        self.line3 = wx.TextCtrl(self.panel, id=2, size=(1020, 94), style=wx.TE_MULTILINE)
        self.line3.SetDefaultStyle(wx.TextAttr(wx.WHITE, wx.BLACK))
        self.line3.SetFont(self.font)
        self.line3.SetBackgroundColour('Black')
        self.line3.Bind(wx.EVT_KEY_DOWN, self.key_pressed)

        # arrow button
        self.arrow_button = wx.Button(self.panel, id=-1, label='Arrow')
        self.arrow_button.Bind(wx.EVT_BUTTON, self.arrow_button_pressed)

        # clear button
        self.clear_button = wx.Button(self.panel, id=-1, label='Clear')
        self.clear_button.Bind(wx.EVT_BUTTON, self.clear_board)

        # buttons container
        self.buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons_sizer.Add(self.clear_button)
        self.buttons_sizer.Add(self.arrow_button)

        self.sizer.Add(self.line1, 0, wx.ALL | wx.EXPAND)
        self.sizer.Add(self.line2, 1, wx.ALL | wx.EXPAND)
        self.sizer.Add(self.line3, 2, wx.ALL | wx.EXPAND)
        self.sizer.Add(self.buttons_sizer, 3, wx.CENTER)
        self.sizer.Fit(self.panel)
        self.panel.SetSizer(self.sizer)

        self.CreateStatusBar()
        self.SetStatusText('CS370 Spring 2019 Wenbin Wu')
        self.Show()

    def clear_board(self, event):
        """clears the message board when pressing esc key or the clear button"""
        self.line1.Clear()
        self.line2.Clear()
        self.line3.Clear()
        self.line1.SetFont(self.font)
        self.line2.SetFont(self.font)
        self.line3.SetFont(self.font)

    def arrow_button_pressed(self, event):
        """handler for arrow button"""
        self.clear_board(wx.EVT_BUTTON)
        self.line2.WriteText('> > > > > > > > > > >')
        self.display_msg(self.line2)

    def key_pressed(self, event):
        """handler for key press events"""
        text_ctrls = [self.line1, self.line2, self.line3]
        text_ctrl_id = event.GetEventObject().GetId()
        next_ctrl_id = (text_ctrl_id + 1) % 3
        target_text_ctrl = text_ctrls[text_ctrl_id]
        next_text_ctrl = text_ctrls[next_ctrl_id]

        if event.KeyCode == 13:  # enter key pressed
            self.display_msg(target_text_ctrl)
            next_text_ctrl.SetFocus()
        elif event.KeyCode == 27:  # escape key pressed
            self.clear_board(wx.EVT_BUTTON)
        elif event.KeyCode == 8:  # backspace pressed
            text = target_text_ctrl.GetValue()[:-1]
            target_text_ctrl.Clear()
            target_text_ctrl.WriteText(text)
        elif event.ShiftDown() and event.KeyCode == 55:  # insert & on key combo shift + 7
            target_text_ctrl.AppendText('&')
        elif event.ShiftDown() or event.CmdDown() or event.AltDown() or event.ControlDown(): 
            # if modifier keys down then do nothing  
            return
        else:
            key = chr(event.KeyCode)
            target_text_ctrl.AppendText(key)

    def encode_message(self, message):
        """convert the message into dot matrix encoding text"""
        encoding_list = [encodings[letter] for letter in message]
        encoded_msg = ''
        for i in range(7):
            # add a single empty colum in from of the message
            encoded_msg += '█'
            for j in encoding_list:
                encoded_msg += ''.join(j[i])
                # add a single empty column between each symbol
                encoded_msg += ('█')
            encoded_msg += '\n'
        return encoded_msg

    def display_msg(self, target_text_ctrl):
        """prints the encoded message to the display"""
        encoded_msg = self.encode_message(target_text_ctrl.GetValue())
        font = target_text_ctrl.GetFont()
        font.SetPointSize(8)
        target_text_ctrl.SetFont(font)
        target_text_ctrl.Clear()
        target_text_ctrl.WriteText(encoded_msg)

        # change the color of encoded characters to yellow
        for i in range(len(encoded_msg)):
            if encoded_msg[i] == '▇':
                target_text_ctrl.SetStyle(i, i + 1, wx.TextAttr('YELLOW', 'BLACK'))
            else:
                target_text_ctrl.SetStyle(i, i + 1, wx.TextAttr('BLACK', 'BLACK'))


if __name__ == '__main__':
    app = wx.App()
    gui = MessageBoard(None, title='Overhead Message Board')
    app.MainLoop()
