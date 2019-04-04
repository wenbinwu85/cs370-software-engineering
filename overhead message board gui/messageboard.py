"""
Dot matrix message board GUI

max 3 lines of message
each letter is 7x5 dot matrix
available symbols A-Z 0-9, -, /

required 3rd party library: wxpython
"""

import wx

from alphabet import encodings

class MessageBoard(wx.Frame):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

        self.SetDimensions(75, 160, 1200, 440)
        self.panel = wx.Panel(self)
        self.sizer = wx.StaticBoxSizer(wx.VERTICAL, self.panel, label='Dot Matrix Display')

        # line 1
        self.line1 = wx.TextCtrl(self.panel, 0, 'ABCDEFGHIJKLM', size=(1200, 120), style=wx.TE_MULTILINE)
        self.print_msg(self.line1)
        self.line1.SetFocus = True
        self.line1.Bind(wx.EVT_KEY_DOWN, self.key_clicked)
        self.sizer.Add(self.line1, 0, wx.ALL | wx.EXPAND)

        # line 2
        self.line2 = wx.TextCtrl(self.panel, 1, 'NOPQRSTUVWXYZ', size=(1200, 120), style=wx.TE_MULTILINE)
        self.print_msg(self.line2)
        self.line2.Bind(wx.EVT_KEY_DOWN, self.key_clicked)
        self.sizer.Add(self.line2, 1, wx.ALL | wx.EXPAND)

        # line 3
        self.line3 = wx.TextCtrl(self.panel, 2, '0123456789-/', size=(1200, 120), style=wx.TE_MULTILINE)
        self.print_msg(self.line3)
        self.line3.Bind(wx.EVT_KEY_DOWN, self.key_clicked)
        self.sizer.Add(self.line3, 2, wx.ALL | wx.EXPAND)

        self.sizer.Fit(self.panel)
        self.panel.SetSizer(self.sizer)

        self.CreateStatusBar()
        self.SetStatusText('Type a message then press "Enter" to display the message, press "Esc" to clear the message. Available symbols: A-Z, "/" and "-"')

    def key_clicked(self, event):
        text_ctrls = [self.line1, self.line2, self.line3]
        text_ctrl_id = event.GetEventObject().GetId()
        target_text_ctrl = text_ctrls[text_ctrl_id]

        keycode = event.GetKeyCode()
        key = chr(keycode)

        if key in encodings:
            target_text_ctrl.AppendText(key)
        elif keycode == 13:  # enter
            self.print_msg(target_text_ctrl)
        elif keycode == 27:  # escape
            target_text_ctrl.Clear()
        elif keycode == 8:  # backspace
            pass

    def encode_message(self, message):
        values = [encodings[letter] for letter in message]
        encoded_msg = []
        for i in range(7):
            encoded_msg.append('█')
            for j in values:
                encoded_msg.extend(j[i])
                # add a single column space between each char
                encoded_msg.append('█')
            encoded_msg.append('\n')
        encoded_msg = ''.join(encoded_msg)
        return encoded_msg

    def print_msg(self, target_text_ctrl):
        encoded_msg = self.encode_message(target_text_ctrl.GetValue())
        target_text_ctrl.Clear()
        target_text_ctrl.WriteText(encoded_msg)
        for i in range(len(encoded_msg)):
            if encoded_msg[i] == '▇':
                target_text_ctrl.SetStyle(i, i + 1, wx.TextAttr('YELLOW', 'BLACK'))


if __name__ == '__main__':
    app = wx.App()
    gui = MessageBoard(None, title='Overhead Message Board').Show()
    app.MainLoop()
