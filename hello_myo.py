import myo
from myo.lowlevel import pose_t, stream_emg
from myo.six import print_
import random
import win32api, win32con

myo.init()

SHOW_OUTPUT_CHANCE = 0.01
r"""
There can be a lot of output from certain data like acceleration and orientation.
This parameter controls the percent of times that data is shown.
"""

class Listener(myo.DeviceListener):
    orientation_yee = [0,0,0,0]
    is_debug = False

    def __init__(self):
        self.e_pressed = False

    def left_click(self):
        win32api.SetCursorPos((x,y))

        current_position = GetCursorPos()
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, current_position[0], current_position[0])
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, current_position[0], current_position[0])

    def Right_click(self):
        win32api.SetCursorPos((x,y))

        current_position = GetCursorPos()
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, current_position[0], current_position[0])
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTTUP, x, y, current_position[0], current_position[0])


    def on_wave_in(self):
        self.e_pressed = True

        #Set 2&3 Hardwarescan code, as documented on http://en.wikipedia.org/wiki/Scancode
        #Alternative ScanCode: 0x1E
        #Release Code: 0x9E
        win32api.keybd_event(0x45, 0x1C)


    def release_e(self):
        ''' releases the E key iff it is no t already depressed '''
        if self.e_pressed:
            self.e_pressed = False

        #Set 2&3 Hardwarescan code, as documented on http://en.wikipedia.org/wiki/Scancode
        #Alternative ScanCode: 0x1E
        #Release Code: 0x9E
        win32api.keybd_event(0x45, 0x1C)

    def on_connect(self, myo, timestamp):
        if is_debug: print_("Connected to Myo")

        myo.vibrate('short')
        myo.request_rssi()

    def on_rssi(self, myo, timestamp, rssi):
        if is_debug: print_("RSSI:", rssi)

    def on_event(self, event):
        r""" Called before any of the event callbacks. """

    def on_event_finished(self, event):
        r""" Called after the respective event callbacks have been
        invoked. This method is *always* triggered, even if one of
        the callbacks requested the stop of the Hub. """

    def on_pair(self, myo, timestamp):
        if is_debug:
            print_('Paired')
            print_("If you don't see any responses to your movements, try re-running the program or making sure the Myo works with Myo Connect (from Thalmic Labs).")
            #print_("Double tap enables EMG.")
            #print_("Spreading fingers disables EMG.\n")

    def on_disconnect(self, myo, timestamp):
        if is_debug: print_('on_disconnect')


    def on_pose(self, myo, timestamp, pose):
        if is_debug: print_('on_pose', pose)

        arm_boundary = 0.45
        global orientation_yee

        if pose == pose_t.double_tap:
            if is_debug: print_("double_tap")
            #myo.set_stream_emg(stream_emg.enabled)

        elif pose == pose_t.fist:
            if is_debug: print_("fist")

        elif(pose == pose_t.fingers_spread) and (orientation_yee[0] < arm_boundary):
            print_("Left Click")
            self.left_click()

        elif(pose == pose_t.fingers_spread) and (orientation_yee[0] > arm_boundary):
            print_("Right Click")
            self.right_click()

        elif pose == pose_t.wave_in:
            self.on_wave_in()

        '''
        elif pose == pose_t.rest:
            self.release_e()
        '''
        else:
            self.release_e()

    def on_orientation_data(self, myo, timestamp, orientation):
        global orientation_yee
        orientation_yee = orientation
        show_output('orientation', orientation)

    def on_accelerometor_data(self, myo, timestamp, acceleration):
        if is_debug: show_output('acceleration', acceleration)

    def on_gyroscope_data(self, myo, timestamp, gyroscope):
        if is_debug: show_output('gyroscope', gyroscope)

    def on_unlock(self, myo, timestamp):
        if is_debug: print_('unlocked')

    def on_lock(self, myo, timestamp):
        if is_debug: print_('locked')

    def on_sync(self, myo, timestamp, arm, x_direction):
        if is_debug: print_('synced', arm, x_direction)

    def on_unsync(self, myo, timestamp):
        print_('unsynced')

    def on_emg(self, myo, timestamp, emg):
        if is_debug: show_output('emg', emg)


def show_output(message, data):
    if random.random() < SHOW_OUTPUT_CHANCE: 
        print_(message + ':' + str(data))


def main():
    hub = myo.Hub()
    hub.set_locking_policy(myo.locking_policy.none)
    hub.run(1000, Listener())

    # Listen to keyboard interrupts and stop the
    # hub in that case.
    try:
        while hub.running:
            myo.time.sleep(0.2)
    except KeyboardInterrupt:
        print_("Quitting ...")
        hub.stop(True)

if __name__ == '__main__':
    main()
