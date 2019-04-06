"""
Overhead Message Board GUI

Max 3 lines of message, each line 20 chars
each char is 7x5 matrix
available symbols A-Z 0-9 - / ' &

required 3rd party library: wxpython

CS370
Wenbin Wu
"""

import wx

from alphabet import encodings


class MessageBoard(wx.Frame):
    """GUI simluation for a overhead message board"""

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.SetSize(x=75, y=160, width=1020, height=335)
        self.panel = wx.Panel(self)
        help_text = 'Type a message then press "Enter" to display the message, press "Esc" to clear the message.'
        self.sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel, label=help_text)

        # line 1
        self.line1 = wx.TextCtrl(self.panel, id=0, value='', size=(1020, 94), style=wx.TE_MULTILINE)
        self.line1.SetDefaultStyle(wx.TextAttr(wx.WHITE, wx.BLACK))
        font = self.line1.GetFont()
        font.SetPointSize(34)
        self.line1.SetFont(font)
        self.line1.SetBackgroundColour('Black')
        self.line1.Bind(wx.EVT_KEY_DOWN, self.key_pressed)
        self.sizer.Add(self.line1, 0, wx.ALL | wx.EXPAND)

        # line 2
        self.line2 = wx.TextCtrl(self.panel, id=1, value='', size=(1020, 94), style=wx.TE_MULTILINE)
        self.line2.SetDefaultStyle(wx.TextAttr(wx.WHITE, wx.BLACK))
        font = self.line2.GetFont()
        font.SetPointSize(34)
        self.line2.SetFont(font)
        self.line2.SetBackgroundColour('Black')
        self.line2.Bind(wx.EVT_KEY_DOWN, self.key_pressed)
        self.sizer.Add(self.line2, 1, wx.ALL | wx.EXPAND)

        # line 3
        self.line3 = wx.TextCtrl(self.panel, id=2, value='', size=(1020, 94), style=wx.TE_MULTILINE)
        self.line3.SetDefaultStyle(wx.TextAttr(wx.WHITE, wx.BLACK))
        font = self.line3.GetFont()
        font.SetPointSize(34)
        self.line3.SetFont(font)
        self.line3.SetBackgroundColour('Black')
        self.line3.Bind(wx.EVT_KEY_DOWN, self.key_pressed)
        self.sizer.Add(self.line3, 2, wx.ALL | wx.EXPAND)

        self.sizer.Fit(self.panel)
        self.panel.SetSizer(self.sizer)

    def key_pressed(self, event):
        """handler for key press event"""

        text_ctrls = [self.line1, self.line2, self.line3]
        text_ctrl_id = event.GetEventObject().GetId()
        target_text_ctrl = text_ctrls[text_ctrl_id]

        key = chr(event.KeyCode)

        if event.KeyCode == 13:  # enter key pressed
            self.display_msg(target_text_ctrl)
        elif event.KeyCode == 27:  # escape key pressed
            target_text_ctrl.Clear()
            font = target_text_ctrl.GetFont()
            font.SetPointSize(34)
            target_text_ctrl.SetFont(font)
        elif event.KeyCode == 8:  # backspace pressed
            text = target_text_ctrl.GetValue()[:-1]
            target_text_ctrl.Clear()
            target_text_ctrl.WriteText(text)
        elif event.ShiftDown() and event.KeyCode == 55:  # & char pressed
            target_text_ctrl.AppendText('&')
        elif event.ShiftDown():  # only shift key down then do nothing
            return
        else:
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

        # change the color of encoded message to yellow
        for i in range(len(encoded_msg)):
            if encoded_msg[i] == '▇':
                target_text_ctrl.SetStyle(i, i + 1, wx.TextAttr('YELLOW', 'BLACK'))
            else:
                target_text_ctrl.SetStyle(i, i + 1, wx.TextAttr('BLACK', 'BLACK'))


if __name__ == '__main__':
    app = wx.App()
    gui = MessageBoard(None, title='Overhead Message Board').Show()
    app.MainLoop()
